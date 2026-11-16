# Current state

**16 November 2026 | Stage 56 completed | KM6 Deluxe Rev. 1 / S905X4**

The device has booted AOSP Android 14 on real hardware using a **temporary RAM + host-backed NBD setup**. The original Android 11 installation has not been replaced. This is a bring-up result, not a flashable ROM.

## What was observed

| Test area | Result |
| --- | --- |
| Kernel | ARM64 Linux 6.18.55 executes on the KM6 |
| Android init | Native ARM64 `init` runs as PID 1 |
| Framework | `zygote64`, `system_server`, Binder services and SystemUI have run |
| Boot | Stage 52/53: natural `sys.boot_completed=1`. Stage 53: **94.52 s**, **219 Binder services** |
| Display | HDMI 1920×1080@60 via DRM/KMS; Panfrost/Mesa, AIDL Composer3 and SurfaceFlinger exercised |
| Home app | Leanback HOME starts, but `libhwui` RenderThread aborts during surface setup |
| Storage | Android images served from the Kubuntu host via NBD. Local eMMC not enumerated by Linux 6.18 |
| Recovery | Prior Android 11 installation still boots; latest audit checked **12/12** backup sets |

These results were described in the maintainer's local engineering reports. Full logs and the corresponding code are **not yet published in this GitHub tree**.

## Active blockers

**1. eMMC:** at 400 kHz, CMD0, CMD1 and CMD2 succeed. CMD3 `SET_RELATIVE_ADDR` with `arg=0x00010000` times out; reported `SD_EMMC_STATUS=0xa1ff2800`. Cause unproven. Do not interpret a driver-level timeout as proof of damaged flash. [Detailed notes](EMMC.md).

**2. UI:** the framework gets far enough for SystemUI and Leanback HOME, but `libhwui CanvasContext::setupPipelineSurface` hits a RenderThread `SIGABRT`. A stable visible home screen has not been verified. [Graphics log](GRAPHICS.md).

**3. Standalone install:** native storage and boot/rollback safety must work before a persistent install is considered. [Recovery notes](RECOVERY.md).

## Still untested on the Android 14 port

- MediaCodec/Codec2 hardware AVC/HEVC/AV1 playback.
- HDMI audio, optical SPDIF, analog audio and passthrough.
- Wi-Fi, full Ethernet operation, Bluetooth and original V01 voice remote.
- Standby/wake, HDMI-CEC and long-running media stability.
- Final SELinux enforcing policy, secure update path and DRM/licensed apps.

## What the test numbers mean

The Stage 56 local report lists **450 passed / 3 skipped** checks in its cumulative automated suite. A separate engineering checklist lists **230 PASS, 1 SKIP, 34 PARTIAL, 17 BLOCKED and 0 FAIL**. Those are different reporting systems. Neither is a count of independent physical test boots; neither is a product completion percentage.

The latest local checkpoint was reported as `2e06096`. It is **not a GitHub commit** here. Stage 57's proposed CMD2/CMD3 register instrumentation is still a plan, not a successful test.

More detail: [dated bring-up record](BRINGUP.md) · [tests](TESTING.md) · [roadmap](ROADMAP.md).
