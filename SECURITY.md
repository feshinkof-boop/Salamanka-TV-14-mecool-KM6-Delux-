# Security

No installable Salamanka firmware has been released. Unknown builds or files claiming to be official Salamanka releases should not be flashed.

Supply-chain auditing matters because of the published Videostrong/XCPE research, but it has **not** been proved that this exact KM6 Deluxe Rev. 1 unit is infected. The report and currently known indicators are documented in [the XCPE notes](security/XCPE-VIDEOSTRONG.md).

The included `tools/rom_audit.py` scans already extracted filesystem trees and reports known indicators, ELF architecture and coverage gaps. A zero-hit report is **not** a clean bill of health.

Please do not submit private exploit details or secrets in public issues. If enabled, use GitHub's private vulnerability reporting; otherwise share only a non-sensitive description with the maintainer until an appropriate private channel is agreed. Never post TEE/DRM keys, signing keys, seed phrases, home IPs or unique device identifiers.

A future release requires component provenance, SELinux enforcing, verified update/recovery, secure defaults and device-level validation. [Release requirements](docs/RELEASE-CRITERIA.md).
