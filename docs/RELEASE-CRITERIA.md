# Conditions for an installable build

There is **no Salamanka TV 14 firmware release**. The existing Android 14 boot-complete result used the physical device with storage served from a PC. Passing that test does not justify flashing an image to internal storage.

The following must be demonstrated on **KM6 Deluxe Rev. 1**, with exact source revisions, logs and artifact hashes.

| Required result | Current evidence | Gate |
| --- | --- | --- |
| ARM64 Android 14 boot on the device | `init`, Zygote, system_server and `sys.boot_completed=1` on NBD | **Partial**: needs independent local boot |
| Stable usable UI | Composer3/SurfaceFlinger/display mode exercised | **Blocked**: HWUI RenderThread abort |
| Native eMMC reads and persistent images | MMC CMD0–CMD2 complete | **Blocked**: CMD3 timeout |
| Recoverable install / slot handling | 12 backup sets verified, Android 11 fallback boots | **Incomplete**: install/restore sequence not validated |
| Secure Android permissions | Temporary tests permissive | **Blocked**: SELinux enforcing, provenance and final signing |
| Media decode and playback | S905X4 hardware capability; graphics tests | **Not tested**: hardware Codec2/MediaCodec AVC, HEVC, AV1 |
| TV sound | Device exposes HDMI/SPDIF/analog on existing firmware | **Not tested** on Salamanka |
| Input, network and power | NBD test transport available | **Not tested** as complete TV services |
| Durability | Short physical bring-up runs | **Not tested**: 24–72 hour media/network/input soak |
| Reproducible public sources | Local development checkout exists | **Incomplete**: actual source and hashes not mirrored |

The next flashable image should include a source revision, build manifest, partitions and sizes, sha256 checksums, device revision, firmware/bootloader assumptions, precise limitations, recovery path and signing details appropriate for distribution.

Never describe a firmware image as safe, compatible, certified, Widevine L1, Android TV Play-certified or Netflix-approved without independent evidence and legal entitlement.

[Status](STATUS.md) · [Recovery](RECOVERY.md) · [Testing record](TESTING.md).
