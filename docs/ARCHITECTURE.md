# Architecture and design decisions

## Non-negotiable user requirements

- Genuine **ARM64-only Android 14 userspace**. A 64-bit kernel + 32-bit Android is unacceptable. No permanent 32-bit-only HAL compatibility layer.
- Prioritize an unrecoverable brick avoidance over speed or maintaining current multiboot. Build/test offline autonomously; physical writes require explicit owner approval and verified recovery plan.
- Do not abandon the mainline-oriented Linux 6.18.55 work for convenience. An audited vendor/BSP path may be investigated as a separate reference.
- Build stability, hardware support and security before cosmetic customization.

## Kernel and framework tracks

**Track A — mainline-oriented:** Linux 6.18.x ARM64, Meson DRM/KMS, Panfrost Mali G31, GBM/gralloc, HDMI, regulator/clock/reset, video acceleration via verified codec stack. Determine correct Android 14 FCM 8 compatibility first; HIDL 2.4 is deprecated but not automatically illegal. AIDL Composer3 may be a better long-term design, only after evidence and hardware validation.

**Track B — audited Amlogic BSP reference:** inspect known-good hardware drivers, DTBs, firmware and HAL behavior without inheriting entire proprietary OS image; port or rewrite 64-bit services as necessary. No unvetted OEM packages, remote administration or network clients.

**Neither track is production-ready until device tests pass.** At present the status of video VPU, audio subsystem, HDMI-CEC, native voice remote and suspend/resume is unknown on Salamanka 14.

## Native 64-bit verification

Check every required userspace ELF architecture, Zygote mode, `ro.product.cpu.abilist`, HAL/VINTF declarations, binder interfaces, runtime service startup and linker dependencies. A `file` report on binaries alone does not demonstrate 64-bit-only runtime.

## Boot

Existing slimBOX boot chain: BL33/U-Boot's embedded multi-DTB selected the live kernel DTB. The legacy `_aml_dtb` partition was not used along the observed boot path. See `research/BOOTCHAIN.md`.

The secure release must publish an explicit partition list, boot/DTBO/vendor boot assumptions, A/B slot strategy, dynamic super group sizes, AVB signatures, rollback and recovery tests.

## Intellectual property, licenses and credentials

No Widevine keys, TEE provisioning assets, platform signing secrets or proprietary firmware dumps in public Git. Do not represent AOSP as equivalent to licensed Google TV or Netflix certification.