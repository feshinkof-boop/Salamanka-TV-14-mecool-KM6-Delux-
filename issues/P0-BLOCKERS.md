# Highest-priority unresolved blockers — 16 November 2026 (Stage 56)

1. **Linux 6.18 eMMC CMD3 timeout:** card initializes through CMD0/1/2 at low speed but CMD3 SET_RELATIVE_ADDR times out; no local `/dev/mmcblk*` or `super` access. Use safe read-only traces. Root cause still unknown.
2. **Leanback/HWUI RenderThread abort:** Android 14 reaches `sys.boot_completed=1`, with SystemUI/Leanback active, but `libhwui CanvasContext::setupPipelineSurface` aborts. No stable, visually confirmed launcher.
3. **Transition from NBD to local boot:** host-served Android images are a deliberate safe test method, not deployable firmware. Native image, partition/slot and rollback plan must be independently proven.
4. **SELinux/ABI/security:** physical test system remains permissive; audit every required ARM64 HAL, permissive denial and privilege boundary. Complete supply-chain investigation.
5. **Video codec hardware:** GPU acceleration does not prove AV1/HEVC/AVC VPU decoder support under Android 14.
6. **Audio routes:** HDMI, optical SPDIF, 3.5mm analog, passthrough and A/V sync.
7. **Radio and remote:** Rev1 Ethernet/radio drivers, V01 mic and HID behavior, Bluetooth/wake reliability, HDMI-CEC.
8. **Reliability:** long unattended playback, input, sleep and network soak, full cold boot, recovery and secure OTA.
9. **Real source publication:** original local kernel/AOSP/HAL modifications and hashed evidence are not yet mirrored in GitHub; do not invent them.

**What is already demonstrated:** genuine physical ARM64 Android bring-up, zygote/system_server, Composer3/SurfaceFlinger and HDMI DRM/KMS activity, natural Android boot-complete over RAM/NBD, and 12/12 verified backup sets. These are significant milestones, not promises of release readiness.

See [status](../docs/STATUS.md) and [engineering work](../docs/PROGRESS.md).
