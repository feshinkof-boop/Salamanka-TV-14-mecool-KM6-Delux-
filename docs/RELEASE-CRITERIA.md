# Release gates — Stage 56 assessment, 16 November 2026

This is a **physical Android 14 bring-up project, not a flashable ROM release**. All gates below require real evidence from KM6 Deluxe Rev1. An experimental RAM/NBD boot counts as meaningful bring-up but **not** a standalone installation.

| Gate | Acceptance criteria | Current state |
| --- | --- | --- |
| **A — architecture and boot** | ARM64-only Android 14 services; correct VINTF; clean cold boot, stable launcher and power cycle | **PARTIAL:** Android 14 services and boot_completed demonstrated; RenderThread crashes, runtime HAL audit incomplete |
| **B — local storage and recovery** | Native eMMC enumerate/RW, valid partition access, independent recovery and tested A/B rollback | **BLOCKED:** CMD3 timeout; 12/12 backups verified, prior Android 11 healthy |
| **C — display and video** | Stable SurfaceFlinger/Composer, proven actual screen output, hardware AVC/HEVC/AV1, HDR/AFR | **PARTIAL:** Panfrost/Mesa/1080p60/Composer shown in logs; final launcher and hardware codecs unverified |
| **D — audio** | HDMI, SPDIF, analog and formats supported by the board | **UNKNOWN** |
| **E — network, radio, remote** | Gigabit Ethernet, Wi-Fi, BT, original V01 voice, suspend/wake/CEC | **PARTIAL:** temporary NBD network path worked; full device functionality unknown |
| **F — stability** | 24h/72h repeated playback, input and power-cycle tests, no fatal crashes | **BLOCKED:** known launcher abort |
| **G — security** | SELinux enforcing, component provenance, no unreviewed OEM agents, verified updates and permissions | **BLOCKED:** recent physical testing permissive; complete security audit pending |
| **H — distribution** | Local source parity, complete build hashes, compatible license review and safe signed deployment instructions | **BLOCKED:** firmware/source checkout not yet publicly mirrored |

## Current evidence is not the release evidence

The latest reported test suite totals are **450 PASS / 3 SKIP**, while a separate acceptance matrix reports **230 PASS / 1 SKIP / 34 PARTIAL / 17 BLOCKED / 0 FAIL**. Neither proves all device drivers are ready. Raw detailed logs and the complete source tree are not presently on this repository.

Requirements for any eventual release include revision-specific hashes, build/boot logs, architecture proof of every mandatory service, hardware video evidence, audio/peripheral tests, device data protection, signed update verification, recovery from interrupted boots, sanitized network captures and a clear limitation list.

**No release image, flash link or inferred completion percentage should be published until the project passes these gates.**
