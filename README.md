# Salamanka TV 14

Android TV 14 for the **MECOOL KM6 Deluxe Rev. 1** (4/64 GB, Amlogic S905X4 / SC2-AH212).

The S905X4 is a 64-bit SoC, but the original KM6 Android environment was 32-bit. I started Salamanka to see how far the hardware can be taken with a native ARM64 Android 14 userspace and a newer Linux kernel, without turning it into a box that can no longer play video or use its original remote.

**Maintainer:** [@feshinkof-boop](https://github.com/feshinkof-boop)  
**Development target:** genuine ARM64-only AOSP, not a modified slimBOX image.  
**Release status:** **no installable firmware**.

## Latest state — 16 November 2026

Android 14 is running on the physical KM6 through a temporary RAM boot with system images served by the development computer over NBD. It reaches a natural `sys.boot_completed=1` and has run `zygote64`, `system_server`, SystemUI and Leanback HOME. The later boot experiment reported **219 Binder services**.

That does **not** mean the TV interface is usable. Leanback currently hits a `libhwui` RenderThread abort. Linux 6.18.55 also cannot enumerate the internal eMMC: CMD0–CMD2 complete but CMD3 times out. These are the two immediate investigations.

| Area | Known result | Open issue |
| --- | --- | --- |
| Android 14 / ARM64 | Physical `init`, Zygote, framework and boot-complete | Release configuration, stability |
| Display/GPU | Panfrost/Mesa, HDMI DRM/KMS 1080p60, Composer3/SurfaceFlinger exercised | HWUI launcher crash |
| Internal eMMC | MMC initialization begins | CMD3 response timeout |
| Media, audio and remote | Hardware capability exists on stock device | Android 14 HAL/driver tests still needed |
| Recovery | Existing Android 11 still boots; 12 backup sets verified | Independent Android 14 install/rollback not tested |

[Exact status](docs/STATUS.md) · [Bring-up history](docs/BRINGUP.md) · [eMMC notes](docs/EMMC.md) · [Graphics notes](docs/GRAPHICS.md)

## The work

The port started with an audit of the bootloader, partition layout and device trees. That led to AOSP product builds, Linux 6.18.55 bring-up, Android `init` and framework debugging, Panfrost/DRM integration, and finally physical Android test boots over NBD. The current problems are specific, reproducible failures rather than a missing Android build.

The development has reached **Stage 56** locally. The latest reported checkpoint is **`2e06096`** (a local commit, not a commit in this GitHub repo). See the [dated lab record](docs/BRINGUP.md) and [test notes](docs/TESTING.md); a stage count is not a completion percentage.

## What is here

This repository contains technical notes, older sanitized board investigations, community/security references, and a [read-only ROM inventory tool](tools/rom_audit.py) with synthetic tests.

**The active AOSP checkout, modified kernel, device/HAL sources, build images and full on-device logs have not yet been mirrored here.** Those remain on the local development machine. This repository is not currently a reproducible build or a firmware download.

Technical notes:
- [System design](docs/ARCHITECTURE.md) · [Build](docs/BUILD.md) · [Hardware matrix](docs/HARDWARE.md)
- [Recovery](docs/RECOVERY.md) · [Roadmap](docs/ROADMAP.md) · [Release checks](docs/RELEASE-CRITERIA.md)
- [XCPE supply-chain research](security/XCPE-VIDEOSTRONG.md) · [4PDA findings](research/4PDA-COMMUNITY.md)

[Русский статус](docs/STATUS-RU.md) · [Open issues](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues)

## Help and support

Testing advice and patches are welcome, especially for SC2 MMC initialization, Android graphics, Amlogic audio/VPU, V01 voice input and safe recovery. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before sharing logs or binaries.

[Support the project](SUPPORT.md) (English / Русский / 中文). Support is voluntary and does not promise a release.

This is an independent project, not affiliated with MECOOL, Amlogic or slimBOXtv.
