# Engineering status — 2026-11-12

**Legend:** DEVICE-PASS (tested on hardware); HOST-PASS (validated offline); BUILT (compiled, no runtime proof); BLOCKED; UNKNOWN; PLANNED.

## Chronology

- **2020 factory firmware:** Android TV 10, stock V4.20201026, 32-bit Android userspace. Originally had a working Widevine L1 path according to archived device evidence.
- **2026-10-20:** slimBOXtv ATV 11 installed. Later audit identified build **11.46** and kernel **5.4.125**. Root via Magisk 30.7, SELinux permissive, A/B slot `_a`; network-only ADB, Termux SSH. Earlier stock bootloader replaced by slimBOX bootloader. Widevine L1 lost, L3 protected playback proven working.
- **2026-10-25/26:** offline bootloader/DTB and startup investigations completed; **29/29 audit checks passed**. No persistent bootloader/env/logo/TEE/DTB write was performed during that audit. See `research/archived/`.
- **2026-11-02/03:** AOSP Android 14 and 64-bit kernel development progressed. Local sources synced, product lunch and Soong/Kati configuration passed. A previous build hit duplicate `km6_gpu_device` SELinux type / VINTF policy version inconsistencies and DMA-BUF heap naming, which were addressed in reported build iterations.
- **2026-11-03:** AOSP image builds reported success: `system.img`, `system_ext.img`, `vendor.img`, `product.img`, `odm.img`, `super.img`, `vbmeta_system.img`. Host checks reported a consistent dynamic partition structure, ELF64/AArch64 binaries and AVB test-key structure.
- **2026-11-11/12:** independent 4PDA and XCPE research incorporated; release security requirements elevated to P0.

**Correction (Nov 12):** Android 14 corresponds to FCM **8**; FCM **202404** is Android 15. The build's reported checkvintf failure at 202404 with declared HIDL Composer 2.4 requires inspection of the **actual** matrices and declarations. It is not proof AIDL Composer3 is universally mandatory for Android 14. [Investigation](FCM-ANALYSIS.md). Compositor runtime remains untested.

## Device-verified historic findings (from Oct 26 report)

- slimBOX 11.46 Android 11 boots, rooted and network reachable.
- Kernel 5.4.125, A/B partitions, active DTB `sc2_s905x4_ah212-4g`.
- Loaded DTB's USB `controller-type=0x03` means the proposed `_aml_dtb` store-only edit did **not** change the live DTB; no USB ADB gadget attachment was demonstrated.
- Widevine **L3 CDM provisioned and license/protected playback succeeded** (Media3/ExoPlayer; first frame 1,958ms; >60s). L1 provisioning failed with `keybox error 25` / `Bad Level 1 Root of Trust`, despite stock firmware historically exhibiting L1. A solution is **not** demonstrated.
- Embedded U-Boot multi-DTB source in BL33 determined by offline analysis. See archived report; do not infer the same bootloader is still installed without rechecking.

## Not yet established

- A bootable, stable Salamanka Android 14 on physical KM6.
- Working Android 14 native hardware acceleration for AV1/HEVC.
- HDMI/SPDIF/analog audio on 6.18-based Android build.
- Original remote V01 voice input.
- Network and wake behavior on Android 14.
- Preservation of Google certification / Widevine level.
- Whether the user's own device, stock images or imported blobs contain XCPE.

## Files currently NOT included in this public repository

The huge AOSP checkout, compiled images, kernel source fork, proprietary blobs, offline benchmark logs, and original backup/restore images remain on the local Kubuntu development workstation and were not made available to this connected GitHub session. **No source code, binary firmware, benchmark output or flashing artifact has been fabricated.**

The next trusted update should commit real locally available source and test evidence with SHA-256 manifest, license review and secret scanning.