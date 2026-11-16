# Engineering roadmap — updated 16 November 2026

Salamanka TV 14 has progressed from offline image builds to **physical ARM64 Android 14 execution and temporary RAM/NBD boots reaching `sys.boot_completed=1`**. This does not establish persistent storage, a stable launcher or full hardware support.

## P0: release blockers

| Priority | Required result | Current state |
| --- | --- | --- |
| **P0-01: Internal eMMC** | Reliable storage enumeration and native Android system/data access on KM6 Rev1 | **BLOCKED:** CMD0/1/2 pass; CMD3 times out (Stage 56). Do not guess or write partitions. |
| **P0-02: Android UI** | Stable boot, launcher rendering, navigation and clean restart/shutdown | **PARTIAL:** boot_complete, 219 Binder, SystemUI/Leanback activity; RenderThread abort and visible display acceptance remain. |
| **P0-03: Safe recovery/OTA** | Verified backups, clean A/B lifecycle, reproducible native recovery on exact revision | **PARTIAL:** 12/12 backups checked and existing Android 11 works; complete release recovery not proven. |
| **P0-04: Framework/Composer** | Valid Android 14 FCM/VINTF/64-bit services, functioning HWUI/SurfaceFlinger | **PARTIAL:** AIDL Composer3 and GPU/DRM path progressed on hardware; full UI not stable. |
| **P0-05: Hardware VPU** | Actual AVC/HEVC/AV1 4K decode via Android MediaCodec/Codec2 | **UNVERIFIED** |
| **P0-06: Audio** | HDMI, optical SPDIF, analog audio, sync and supported passthrough | **UNVERIFIED** |
| **P0-07: Remote and radios** | V01 microphone, input, Wi-Fi, Bluetooth, reliable wake | **UNVERIFIED** |
| **P0-08: Networking and power** | Normal Ethernet, sleep/wake, DHCP, HDMI-CEC, sustained transfers | **PARTIAL:** NBD transport demonstrably used, general consumer connectivity not validated |
| **P0-09: Release security** | SELinux enforcing, component provenance/SBOM, XCPE review, secure OTA and permissions | **BLOCKED:** temporary tests permissive; full audit still required |
| **P0-10: Sustained reliability** | No fatal UI/system crashes in multi-day use | **BLOCKED:** launcher RenderThread SIGABRT |

### Recommended engineering order

1. **Trace eMMC CMD3 at low speed using reversible, owner-approved diagnostics** and distinguish protocol/card state from controller/DTB issues; do not modify persistent storage.
2. **Reproduce and resolve HWUI/Leanback RenderThread abort**, capture actual on-screen result and cold-boot stability.
3. Complete proper Linux MMC storage bring-up, native partition read/write safety planning and recovery proving *before* any firmware deployment.
4. Restore strict SELinux/permissions, verify ARM64-only processes and valid HAL/VINTF declarations.
5. Reintroduce and test media hardware decoder, all audio paths, radio/remote/standby and HDMI features on the real board.
6. Finalize repeatable build evidence, binary provenance, security review and owner-approved safe release artifacts.

## P1: end-user quality

- AFR/HDR10/SDR, EDID, HDMI-CEC, audio-video synchronization and multi-receiver testing.
- Remote V01/V03 reliability, voice input, key mapping and standby behavior.
- Ethernet/Wi-Fi/Bluetooth throughput and reconnection; safe network services off by default.
- USB host and permitted storage accessories; **no microSD card is required or planned for the bring-up/recovery path**.
- Signed updates, user-mode security defaults, explicit privacy controls, multi-day soak tests.

## P2: optional capabilities, not release guarantees

Salamanka Media Engine, Remote Manager, Power Manager, Performance Manager, optional Network Suite, Android TV customization, Linux ARM64 experimentation and custom branding.

**No P2 feature cancels a P0 blocker.** See [full status](STATUS.md), [effort](PROGRESS.md) and [release gates](RELEASE-CRITERIA.md).
