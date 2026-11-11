"""Synthetic tests; never touch firmware, devices or networks."""
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path
from tools.rom_audit import elf_arch, find_indicators, load_baseline, main, scan


class TestRomAudit(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "root"
        self.root.mkdir()

    def put(self, name, content):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
        return p

    def test_empty_tree(self):
        self.assertEqual(scan(self.root)["status"], "NO_TRACKED_FINDINGS")

    def test_ascii_indicator(self):
        self.put("vendor/priv", b"host=szbboys.com")
        self.assertEqual(scan(self.root)["summary"]["ioc_paths"], ["vendor/priv"])

    def test_utf16_indicator(self):
        self.assertIn("x.cpe", find_indicators("x.cpe".encode("utf-16le")))

    def test_indicator_in_filename(self):
        self.put("oem/app/x.cpe", b"ok")
        self.assertEqual(scan(self.root)["summary"]["ioc_paths"], ["oem/app/x.cpe"])

    def test_elf_64(self):
        h = bytearray(20)
        h[:4] = b"\x7fELF"; h[4] = 2; h[5] = 1; h[18] = 183
        self.put("vendor/bin/hw/composer", h)
        self.assertEqual(scan(self.root)["files"][0]["architecture"], "ELF64:aarch64")

    def test_elf_32_policy(self):
        h = bytearray(20)
        h[:4] = b"\x7fELF"; h[4] = 1; h[5] = 1; h[18] = 40
        self.put("vendor/lib/bad.so", h)
        self.assertEqual(scan(self.root, require_arm64=True)["status"], "FINDINGS_OR_INCOMPLETE")
        self.assertEqual(scan(self.root)["status"], "NO_TRACKED_FINDINGS")

    def test_bad_elf_header(self):
        self.assertIsNone(elf_arch(b"bad"))

    def test_compressed_apk(self):
        p = self.root / "system/app/example.apk"
        p.parent.mkdir(parents=True)
        with zipfile.ZipFile(p, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("classes.dex", b"anyevonline.com")
        self.assertEqual(scan(self.root)["files"][0]["zip_indicators"][0]["member"], "classes.dex")

    def test_truncated_file_reports_gap(self):
        self.put("system/blob", b"a" * 200)
        self.assertTrue(scan(self.root, limit=64)["coverage_incomplete"])

    def test_corrupt_apk_reports_gap(self):
        self.put("system/app/a.apk", b"not a zip")
        self.assertTrue(scan(self.root)["coverage_incomplete"])

    def test_zip_budget_reports_gap(self):
        p = self.root / "vendor/a.zip"
        p.parent.mkdir(parents=True)
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("big", b"x" * 200)
        self.assertTrue(scan(self.root, limit=64)["coverage_incomplete"])

    def test_symlink_not_followed(self):
        self.put("system/a", b"ok")
        (self.root / "alias").symlink_to(self.root / "system")
        self.assertTrue(scan(self.root)["coverage_incomplete"])

    def test_baseline_match(self):
        p = self.put("vendor/legit", b"ok")
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(scan(self.root, baseline={"vendor/legit": digest})["status"], "NO_TRACKED_FINDINGS")

    def test_baseline_mismatch(self):
        self.put("vendor/legit", b"ok")
        self.assertEqual(scan(self.root, baseline={"vendor/legit": "0" * 64})["summary"]["baseline_failures"], ["vendor/legit"])

    def test_baseline_missing(self):
        self.assertTrue(scan(self.root, baseline={"missing": "0" * 64})["coverage_incomplete"])

    def test_bad_csv(self):
        p = Path(self.temp.name) / "baseline.csv"
        p.write_text("path,sha256\nx,not-a-sha\n")
        with self.assertRaises(ValueError):
            load_baseline(p)

    def test_cli_rejects_output_inside_root(self):
        self.assertEqual(main([str(self.root), "--report", str(self.root / "out.json")]), 2)

    def test_cli_findings_exit_nonzero(self):
        self.put("x.cpe", b"ok")
        self.assertEqual(main([str(self.root), "--report", str(Path(self.temp.name) / "out.json")]), 1)


if __name__ == "__main__":
    unittest.main()
