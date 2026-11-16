# Build notes

The active AOSP and kernel work is on the maintainer's Kubuntu workstation. **This GitHub repository is not yet a complete source checkout and cannot produce a Salamanka TV 14 image by itself.**

## Local work reported

- AOSP Android 14 sync and device-product configuration completed.
- Soong/Kati and system, system_ext, vendor, product, ODM, super and vbmeta_system image generation reported successful.
- Linux 6.18.55 ARM64 compiled for the S905X4 / SC2 target.
- Subsequent physical RAM/ADNL bring-up ran Android `init`, `zygote64`, `system_server` and later reached `sys.boot_completed=1` with host-backed NBD images.
- Real graphics integration progressed to Panfrost/Mesa, DRM/KMS, Composer3 and SurfaceFlinger; launcher remains unstable.
- Internal eMMC storage remains inaccessible under the new kernel, so this is not a standalone build.

The reported local Stage 56 checkpoint is `2e06096` and has **not been pushed here**. Do not confuse local build revisions with public GitHub commits or package a release based on these notes.

## When source can be published

Import the actual device/product tree, kernel changes, HAL source, build manifests and reproducible scripts with their history and upstream license notices. Exclude proprietary blobs that cannot legally be redistributed, private images, TEE/DRM keys, Wi-Fi credentials, personal network addresses and private signing material.

Accompany source imports with exact pinned AOSP revisions, sanitized build/test logs, SHA-256 image hashes and a list of unavoidable proprietary firmware dependencies. No dummy placeholder driver should be represented as a working HAL.

[FCM investigation](FCM-ANALYSIS.md) · [Release gates](RELEASE-CRITERIA.md).
