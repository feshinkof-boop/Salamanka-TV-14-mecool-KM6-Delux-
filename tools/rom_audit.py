#!/usr/bin/env python3
"""Read-only offline inventory for *already extracted* Android filesystem trees.

No image mounts, root privileges, ADB, network access, binary execution, or
device writes. Known IOC hits are triage clues, not malware attribution.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

IOC = (
    "x.cpe", "com.oemservice", "com.abc.nexus",
    "com.android.system.ntp", "com.android.sso.auth.handler",
    "anyevonline.com", "szbboys.com", "yokatvonline.com",
    "intermedia-arts.tv",
)
ZIP_TYPES = {".apk", ".apex", ".jar", ".zip"}


def elf_arch(header: bytes) -> str | None:
    if len(header) < 20 or header[:4] != b"\x7fELF":
        return None
    bitness = {1: "ELF32", 2: "ELF64"}.get(header[4], "ELF-UNKNOWN")
    if header[5] not in (1, 2):
        return bitness + ":unknown-endianness"
    machine = int.from_bytes(header[18:20], "little" if header[5] == 1 else "big")
    return bitness + ":" + {183: "aarch64", 40: "arm", 62: "x86_64", 3: "x86"}.get(machine, f"machine-{machine}")


def find_indicators(data: bytes) -> list[str]:
    low = data.lower()
    return [term for term in IOC if term.encode() in low or term.encode("utf-16le") in low]


def hash_and_head(path: Path, limit: int) -> tuple[str, bytes, bool]:
    h = hashlib.sha256()
    head = bytearray()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
            if len(head) < limit:
                head.extend(chunk[:limit - len(head)])
    return h.hexdigest(), bytes(head), path.stat().st_size > limit


def inspect_zip(path: Path, budget: int) -> tuple[list[dict], list[str]]:
    """Bounded decompression; never extracts anything or trusts archive paths."""
    hits = []
    warnings = []
    try:
        with zipfile.ZipFile(path) as zf:
            members = zf.infolist()
            if len(members) > 2000:
                return hits, [f"archive-member-limit:{len(members)}"]
            consumed = 0
            for member in members:
                if member.is_dir():
                    continue
                if member.file_size > budget - consumed:
                    warnings.append(f"archive-budget:{member.filename}")
                    continue
                try:
                    with zf.open(member) as f:
                        content = f.read(budget - consumed + 1)
                except (OSError, RuntimeError, ValueError, EOFError, zipfile.BadZipFile) as exc:
                    warnings.append(f"unreadable-member:{member.filename}:{type(exc).__name__}")
                    continue
                consumed += len(content)
                if consumed > budget:
                    warnings.append(f"archive-budget-overflow:{member.filename}")
                    break
                indicators = find_indicators(content)
                if indicators:
                    hits.append({"member": member.filename, "indicators": indicators})
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        warnings.append(f"unreadable-archive:{type(exc).__name__}")
    return hits, warnings


def load_baseline(file: Path | None) -> dict[str, str]:
    if file is None:
        return {}
    records = {}
    with file.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            path, digest = row.get("path", "").strip(), row.get("sha256", "").lower().strip()
            if not path or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                raise ValueError(f"invalid baseline row: {path!r}")
            if path in records:
                raise ValueError(f"duplicate baseline path: {path}")
            records[path] = digest
    return records


def scan(root: Path, limit: int = 8 * 1024 * 1024,
         baseline: dict[str, str] | None = None, require_arm64: bool = False) -> dict:
    if root.is_symlink() or not root.is_dir():
        raise ValueError("scan root must be an existing non-symlink directory")
    root = root.resolve()
    baseline = baseline or {}
    files = []
    warnings = []
    seen = set()
    for basedir, dirs, filenames in os.walk(root, topdown=True, followlinks=False):
        base = Path(basedir)
        for dirname in list(dirs):
            child = base / dirname
            if child.is_symlink():
                warnings.append(f"symlink-dir-skipped:{child.relative_to(root).as_posix()}")
                dirs.remove(dirname)
        for name in sorted(filenames):
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                warnings.append(f"symlink-file-skipped:{rel}")
                continue
            try:
                sha, content, truncated = hash_and_head(path, limit)
            except OSError as exc:
                warnings.append(f"unreadable-file:{rel}:{type(exc).__name__}")
                continue
            if truncated:
                warnings.append(f"content-truncated:{rel}")
            indicators = sorted(set(find_indicators(content) + find_indicators(rel.encode("utf-8"))))
            zhits, zwarnings = (inspect_zip(path, limit) if path.suffix.lower() in ZIP_TYPES else ([], []))
            warnings.extend(f"{rel}:{w}" for w in zwarnings)
            state = "not-provided"
            if baseline:
                seen.add(rel)
                state = ("match" if baseline.get(rel) == sha else
                         "mismatch" if rel in baseline else "unlisted")
            files.append({"path": rel, "sha256": sha, "size": path.stat().st_size,
                          "architecture": elf_arch(content[:20]),
                          "indicators": indicators, "zip_indicators": zhits,
                          "baseline": state})
    warnings.extend(f"baseline-missing:{p}" for p in sorted(set(baseline) - seen))
    files.sort(key=lambda x: x["path"])
    ioc_paths = [f["path"] for f in files if f["indicators"] or f["zip_indicators"]]
    elf32 = [f["path"] for f in files if (f["architecture"] or "").startswith("ELF32")]
    mismatches = [f["path"] for f in files if f["baseline"] in ("mismatch", "unlisted")]
    flags = bool(ioc_paths or mismatches or warnings or (require_arm64 and elf32))
    return {
        "schema": "salamanka.offline-inventory.v1",
        "statement": "Static scan of extracted files only. No proof of malware absence or device compatibility.",
        "status": "FINDINGS_OR_INCOMPLETE" if flags else "NO_TRACKED_FINDINGS",
        "coverage_incomplete": bool(warnings),
        "summary": {"file_count": len(files), "ioc_paths": ioc_paths, "elf32_paths": elf32,
                    "baseline_failures": mismatches, "warning_count": len(warnings)},
        "warnings": sorted(warnings), "files": files,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", type=Path, help="already-extracted Android partition directory")
    p.add_argument("--report", type=Path, help="JSON output path OUTSIDE scanned root")
    p.add_argument("--baseline", type=Path, help="CSV containing path,sha256")
    p.add_argument("--strict-arm64", action="store_true", help="flag all ELF32 candidates")
    p.add_argument("--max-scan-mib", type=int, default=8, help="bound indicator scan and ZIP decompression")
    args = p.parse_args(argv)
    if not 1 <= args.max_scan_mib <= 64:
        p.error("--max-scan-mib must be between 1 and 64")
    try:
        root = args.root.resolve(strict=True)
        if args.report and (args.report.resolve() == root or root in args.report.resolve().parents):
            raise ValueError("report must be outside scan root")
        report = scan(root, args.max_scan_mib * 1024 * 1024,
                      load_baseline(args.baseline), args.strict_arm64)
        serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(serialized, encoding="utf-8")
        else:
            sys.stdout.write(serialized)
        return 1 if report["status"] == "FINDINGS_OR_INCOMPLETE" else 0
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
