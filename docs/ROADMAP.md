# Work list

This is the current order of work as of Stage 56 (16 November 2026). Work is organized by what prevents a useful Android 14 build, not by feature announcements.

## 1. Local storage: eMMC / CMD3

**Blocked.** Linux 6.18.55 gets through CMD0, CMD1 and CMD2 at 400 kHz, then times out on CMD3 (`SET_RELATIVE_ADDR`). The controller reports `SD_EMMC_STATUS=0xa1ff2800`; no internal block device appears.

Next: capture read-only controller state at CMD2 and CMD3 using board-specific register definitions and existing working-firmware references. Do not attempt persistent writes until reliable read-only enumeration is proven.

[Investigation](EMMC.md)

## 2. Stable graphics and home screen

**Blocked after substantial progress.** Panfrost/Mesa, HDMI 1080p60, Composer3 and SurfaceFlinger have been exercised. Android reaches SystemUI and Leanback HOME, but `libhwui` aborts from the RenderThread surface setup path.

Next: reproduce with exact logs and test a minimal graphics surface to separate allocator/fence/compositor problems from launcher behavior. Acceptance is a visible, stable Android TV home screen across repeated boots.

[Investigation](GRAPHICS.md)

## 3. Standalone boot and recovery

**Not ready.** Successful Android 14 boots so far require RAM plus host-supplied NBD storage. The known-good Android 11 installation must remain recoverable. Verify partition reads, chosen A/B strategy and rollback before any native installation.

[Recovery conditions](RECOVERY.md)

## 4. Android platform correctness and security

Physical experiments still use permissive SELinux. Confirm all required Android services and vendor HALs really are ARM64; resolve any remaining VINTF/FCM mismatches against the actual source revision; remove unreviewed privileged components and document their origins. A public build should use reproducible, reviewed source and signing material controlled by the maintainer.

[FCM background](FCM-ANALYSIS.md) · [Security](../SECURITY.md)

## 5. Hardware functions

None of the following should be marked working on Salamanka merely because it works on stock firmware:

| Area | Acceptance on the real Rev. 1 |
| --- | --- |
| Video decode | Android hardware AVC/HEVC/AV1 at supported resolutions, with decoder identity and dropped-frame data |
| Audio | HDMI, optical SPDIF and analog output; supported passthrough and sync |
| Network | Gigabit Ethernet and Wi-Fi stable during media and standby |
| Input | V01 voice microphone, key events, Bluetooth reconnect and third-party remotes |
| Display | HDR/SDR, AFR, EDID handling and HDMI-CEC under supported modes |
| Power | Repeated suspend/resume, no phantom wakes, clean shutdown |
| Storage | Safe eMMC operation, USB host/removable storage |

See [hardware details](HARDWARE.md) and [4PDA reports](../research/4PDA-COMMUNITY.md).

## 6. After basic TV functionality works

Possible additions: content-aware AFR/HDR controls and playback statistics, remote diagnostics/remapping, power and performance monitoring, optional network services, and Linux ARM64 use cases. These are proposals, not current build functionality.

[Design notes](FEATURES.md) · [Release criteria](RELEASE-CRITERIA.md).
