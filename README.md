# Salamanka TV 14 — MECOOL KM6 Deluxe Rev 1

**Independent AOSP Android TV 14 / native ARM64 firmware engineering project for the Amlogic S905X4 (SC2/AH212).**

> [!IMPORTANT]
> **Development-stage repository, NOT a flashable release.** The documented Android 14 images have compiled and passed selected host-side inspections, but no successful Android 14 device boot or complete hardware validation has been demonstrated. **Do not flash experimental images without a verified recovery path.**
>
> This repository was populated from available project records and research as of **2026-11-12**. It does **not** yet contain the complete local AOSP tree, compiled images, proprietary drivers, or source assets stored on the developer's Kubuntu machine. Do not mistake documentation for published firmware.

## Project commitments

- **Genuine ARM64-only Android 14 userspace:** no fallback to a 32-bit system or mandatory 32-bit vendor HALs.
- **KM6 Deluxe first-revision hardware:** hardware-specific configuration, not a generic S905X4 ROM.
- **Full functional goal:** accelerated 4K AVC/HEVC/AV1, graphics, HDMI + SPDIF + analog audio, gigabit Ethernet, Wi-Fi, Bluetooth, original V01 microphone remote, display HDR/AFR, correct power/wake, USB/storage.
- **Trustworthy firmware:** independent AOSP, component provenance, XCPE/Videostrong audit, least privilege, signed updates, and recovery.
- **Avoid unrecoverable bricks:** never equate a build PASS with flash readiness.

## Current verified state

| Area | Status | Evidence / qualification |
|---|---|---|
| AOSP Android TV 14 source/product | **BUILT** | Soong/Kati configured and images generated locally (Nov 2026) |
| Native AArch64 build artifacts | **HOST-VALIDATED** | ELF64/AArch64, ext4, dynamic super layout and test-key AVB checks reported passing |
| Images | **BUILT, NOT DEVICE-TESTED** | `system.img`, `system_ext.img`, `vendor.img`, `product.img`, `odm.img`, `super.img`, `vbmeta_system.img` |
| Linux 6.18.55 kernel | **BUILT** | S905X4 work including Meson DRM/HDMI and Panfrost integration |
| Graphics composition | **UNRESOLVED** | Earlier build used FCM 202404 (Android 15 level); Android 14 maps to FCM 8. See [correction](docs/FCM-ANALYSIS.md) |
| Media hardware decoder, HDMI/SPDIF/analog audio | **UNKNOWN** | No successful full device validation |
| Native ARM64-only runtime on KM6 | **UNPROVEN ON DEVICE** | Compile-time ELF checks are not boot evidence |
| Android 14 device deployment | **NOT DONE** | No confirmed Salamanka TV 14 flashing or successful boot |
| October 2026 device audit | **HISTORICALLY DEVICE-VERIFIED** | slimBOXtv 11.46, root, Widevine L3 playback, bootloader/DTB facts; NOT evidence for Salamanka 14 |
| XCPE infection on this exact unit | **UNKNOWN** | Needs partition and package forensics |

See [development status](docs/STATUS.md), [engineering backlog](docs/ROADMAP.md), [hardware capability matrix](docs/HARDWARE.md), [security research](security/XCPE-VIDEOSTRONG.md), and [release gates](docs/RELEASE-CRITERIA.md).

## Repository structure

- `docs/` — observed state, specification, architecture, build and hardware/test requirements.
- `security/` — XCPE findings, supply-chain trust model, scanning requirements and placeholders.
- `research/` — 4PDA community findings, primary sources and sanitized historical project records.
- `tests/` — acceptance matrix and read-only host-side examples.
- `tools/` — safe, read-only local source/build inventory utilities.
- `issues/` — prioritized, actionable engineering blockers.
- `.github/` — contribution and security reporting guidance.

## Real, tested host tooling

The repository now includes [`tools/rom_audit.py`](tools/rom_audit.py), a **read-only** offline inventory scanner for already-extracted partition files. It records SHA-256 file hashes, detects ELF32/ELF64 architecture, scans a bounded selection of XCPE indicators and decompressed APK/JAR content, and reports coverage gaps. [Documentation](docs/TOOLS.md) · [18 synthetic tests](tests/test_rom_audit.py) · [CI results](../../actions/workflows/docs-check.yml).

These tests validate the utility itself, **not** a firmware image or the actual KM6. A zero-hit scan does not prove a ROM is clean.

## Tracked engineering work

[11 actionable issues](../../issues) cover VINTF, real source import, firmware audit, AV1 decoding, V01 voice remote, analog/SPDIF/HDMI audio, boot recovery, connectivity, video timing, and secure release design. The [P0 blockers](issues/P0-BLOCKERS.md) remain release-blocking.

## Verified research correction

The original repository misidentified the Android 14 FCM level. Android 14 is level **8**, while **202404 belongs to Android 15**. See [FCM analysis](docs/FCM-ANALYSIS.md). A failed VINTF check does not establish a hardware compositor solution.

## Safety and provenance

**This public repository deliberately omits** device serial numbers, private LAN addresses, Wi-Fi credentials, TEE/DRM secrets, proprietary firmware binaries and unsigned device-flashing recipes. Archived investigations are historical and are **not** instructions to execute their flashing steps.

Many external reports are community observations; each document should distinguish confirmed hardware facts, independently confirmed external findings, hypotheses, and unimplemented goals.

## External research

- [4PDA MECOOL KM6/KM6 Deluxe thread](https://4pda.to/forum/index.php?showtopic=1007166)
- [slimBOXtv KM6 releases](https://slimboxtv.ru/mecool-km6/)
- [Google Threat Intelligence: XCPE](https://cloud.google.com/blog/topics/threat-intelligence/shutting-the-door-on-the-xcpe-botnet)
- [Synthient Videostrong IoCs](https://github.com/synthient/public-research/tree/main/2026/11/Videostrong)
- [Plume XCPE research](https://www.plume.com/resources/the-x-cpe-botnet)

## Support development / Поддержать проект / 支持开发

**[❤️ Support Salamanka TV 14 — English · Русский · 简体中文](SUPPORT.md)**

Voluntary contributions can help fund test devices, driver research, and development infrastructure. Verified public **TON** and **Bitcoin mainnet** receiving addresses are now listed in [SUPPORT.md](SUPPORT.md). **USDT on TRON/TRC20 and USDT on TON are not enabled yet.** Contributions never imply a flashable release or guaranteed development outcome.

## Licensing

No blanket license has been selected by the owner; see [project governance](docs/PROJECT-GOVERNANCE.md). Existing AOSP, kernel and third-party works retain their own licenses.
