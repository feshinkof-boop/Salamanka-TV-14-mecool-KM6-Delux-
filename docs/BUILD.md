# Build and physical bring-up provenance — November 2026

This project targets independent **AOSP Android TV 14 / native ARM64** on MECOOL KM6 Deluxe Rev1 (Amlogic S905X4/SC2), using a mainline-oriented **Linux 6.18.55** kernel baseline.

## From compilation to physical Android

1. AOSP sources synced and an S905X4-targeted product configured; Soong/Kati and an ARM64 kernel compiled.
2. Android images reported built locally: `system.img`, `system_ext.img`, `vendor.img`, `product.img`, `odm.img`, `super.img`, `vbmeta_system.img`. Original public image hashes and exact source revisions have not been provided here.
3. Compiler and image integration obstacles involved SELinux types, FCM/VINTF declarations, DMA-BUF and graphics HAL/device labels. See [FCM analysis](FCM-ANALYSIS.md) for the distinction between Android 14 FCM 8 and Android 15 level 202404.
4. Physical RAM boot experiments ran an AArch64 Android `init`, then `zygote64`, `system_server` and associated Binder services. GPU/HDMI progressed to DRM/KMS 1080p60 and AIDL Composer3/SurfaceFlinger.
5. Temporary **NBD-backed** Android boots on real hardware then reported natural `sys.boot_completed=1`. One Stage 53 run reported **94.52s**, **219 Binder services**, SystemUI and Leanback HOME activity before a launcher RenderThread SIGABRT.
6. Independent storage bring-up found a reproducible early eMMC MMC-command failure at **CMD3**, after CMD0/1/2 succeeded. Local eMMC remains inaccessible to the modern kernel; no persistent Android 14 device installation is claimed.

## What the public repository contains

Engineering status, milestones, historical sanitized bootloader/DTB analysis, XCPE research, acceptance plans, Python host-only ROM inspection and its synthetic GitHub Actions tests. The evolving kernel patches, full AOSP checkout, firmware images, NBD staging assets, build logs and physical device backup sets remain on the local development workstation—not automatically published here.

## Before sharing images or claiming a reproducible build

- Import the **actual, licensed** project source and pinned upstream revision manifests—not synthesized replacements.
- Publish sanitized original build evidence and image SHA-256 digests, partition layouts and compatibility results.
- Verify Linux eMMC access and preserve the known-good Android 11/recovery environment.
- Verify all ARM64-only userspace services, image startup, display, Codec2 hardware decode, audio, radio/remote support, SELinux enforcing and long-term stability.
- Pass signed/verified OTA and rollback gates with explicit approval before any dangerous device write.

**AOSP built, Android physically booted over NBD, but native storage and release validation remain unfinished.** [Full status](STATUS.md).
