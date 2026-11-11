# Build & artifact provenance

The available project record reports local AOSP Android TV 14 builds on Kubuntu using an ARM64 S905X4 device configuration with Linux 6.18.55 development.

## Reported build milestones

- Android 14 AOSP sync completed; device lunch available.
- Soong/Kati configuration succeeded after memory/swap and build parallelism tuning.
- Duplicate SELinux `km6_gpu_device`, VINTF sepolicy inconsistency and DMA-BUF naming issues were addressed in subsequent attempts.
- Build products reported: `system.img`, `system_ext.img`, `vendor.img`, `product.img`, `odm.img`, `super.img`, `vbmeta_system.img`.
- Host-side validation of partition structure, ext4 and ARM64 binaries reported successful.
- **Compiler success is not an Android 14 hardware boot.**

The exact `repo` manifest revisions, device source tree, kernel config and build logs were not accessible through this conversation's GitHub connection. Reproduce build instructions from the actual local checkout and link commit IDs in a later update; do not fabricate source or shell commands that assume unverified paths.

## Before publishing binaries

1. Publish relevant source and exact revisions, including manufacturer-blobs inventory and redistribution rights.
2. Keep Google/TEE/Widevine proprietary keys, tokens, unique calibration/identity records and private device backups out of Git.
3. Produce a versioned SHA-256 manifest and signed, build-specific metadata.
4. Verify `lunch`, Soong, VINTF, SELinux, ARM64-only HALs, AVB and image compatibility.
5. Complete recovery test and first device boot in controlled conditions.
6. Only then create a GitHub release.