# Architecture

**Target:** KM6 Deluxe Rev. 1 (S905X4 / SC2-AH212).  
**System:** AOSP Android TV 14, native ARM64 userspace.  
**Kernel work:** Linux 6.18.55, mainline-oriented where practical.

## Main constraints

The device has a 64-bit Cortex-A55 CPU, but original Android firmware used 32-bit userspace. Salamanka is not intended to ship a 32-bit Android system behind a 64-bit kernel. The final system must have 64-bit Android runtime and required HALs.

The original hardware software stack cannot be transplanted wholesale: Amlogic's older BSP has different kernel interfaces, graphics/media services, firmware and security assumptions. Any reused binary needs provenance, licensing review and a known purpose.

## Current experimental boot arrangement

```text
KM6 ROM / existing boot chain
          |
          +-- controlled RAM boot --> Linux 6.18.55 / Android 14
                                           |
                                system images over NBD
                                           |
                                 init / Zygote / framework
                                           |
                              SurfaceFlinger / Composer3
```

The host serves storage to avoid overwriting the working Android 11 installation. This arrangement has reached Android boot-complete on real hardware, but it does not prove a self-contained eMMC boot.

## Graphics and media are different jobs

Panfrost/Mesa supplies GPU-side graphics work, while DRM/KMS and Composer3/SF supply display integration. The S905X4 hardware video decoder (VPU) is a distinct pipeline requiring drivers and an Android media HAL; GPU operation **does not** prove AV1/HEVC decoding.

See [graphics](GRAPHICS.md).

## Storage and recovery

Linux 6.18 eMMC enumeration stops at CMD3. Until read-only block access and recovery are proven, moving Android to persistent storage is unsafe. Bootloader/TEE/partition writes are not an acceptable substitute for diagnosing the MMC controller.

See [eMMC](EMMC.md) and [recovery](RECOVERY.md).

## Security

Physical test boots have used permissive SELinux. Distribution requires enforcing policy, controlled privileged components, reviewed donor firmware, signing and rollback testing. A clean AOSP build is not automatically Google-certified or Widevine L1.

[Current status](STATUS.md) · [Security investigation](../security/XCPE-VIDEOSTRONG.md).
