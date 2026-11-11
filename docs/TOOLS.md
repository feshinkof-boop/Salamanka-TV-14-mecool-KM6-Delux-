# Host-side inventory: design and usage

**The real local Android 14 images and AOSP checkout are not in this repository.** These tools support safe offline work on extracted donor/current ROM files. They do not attempt to flash or interact with the KM6.

## Prerequisites

Python 3.10+ (standard library only), and an **already extracted** directory holding Android partitions with subdirectories such as `system/`, `vendor/`, `oem/`, `odm/`.

```sh
python3 -m unittest discover -s tests -v
python3 tools/rom_audit.py /path/to/extracted/partitions \
  --strict-arm64 \
  --report /tmp/salamanka-audit.json
```

Optional SHA-256 baseline CSV:
```csv
path,sha256
vendor/bin/example,aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

```sh
python3 tools/rom_audit.py /path/to/extracted/partitions \
  --baseline /path/to/approved.csv \
  --strict-arm64 --report /tmp/salamanka-audit.json
```

The CSV example is **synthetic**. Add actual trusted hashes only after independent evidence and origin/license review.

## Scanner functions

- Recursively hash files (SHA-256) for repeatable inventories.
- Detect ELF32/ELF64 and machine architecture from ELF headers; `--strict-arm64` flags ELF32 candidates without falsely asserting runtime use.
- Check known XCPE package names and domain strings in file content and filenames (ASCII or UTF-16LE).
- Search bounded decompressed content in APK/JAR/APEX/ZIP entries; no archive member is extracted onto disk.
- Record limitations explicitly (unreadable files/archives, content over limit, skipped symlinks, baseline mismatches and missing files).
- Emit structured JSON: `NO_TRACKED_FINDINGS` or `FINDINGS_OR_INCOMPLETE`. Exit statuses 0, 1, and 2 respectively indicate no tracked findings, findings/incomplete coverage, or invalid input.

**Critical:** "NO_TRACKED_FINDINGS" is NOT "clean" and does not establish malware absence, permissions, runtime HAL compatibility, SELinux integrity, or image signing. This is a static triage tool with a small public IOC subset. No claims about a specific KM6 infection follow from a filename alone.

The test suite uses synthetic files only. These tests are not tests against the actual AOSP build.
