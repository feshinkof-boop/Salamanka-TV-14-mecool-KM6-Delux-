# Bring-up record

Target: MECOOL KM6 Deluxe Rev. 1, Amlogic S905X4 (SC2/AH212)  
Latest completed local report: Stage 56, 16 November 2026  
Local checkpoint cited in the report: `2e06096` (not in this public Git repository)

This log is condensed from development reports. The corresponding kernel/AOSP changes and full logs are still on the development workstation. The word **reported** below means an outcome recorded in those reports, not a test independently rerun from the public GitHub tree.

## October — map the existing system before replacing it

The first work was on the device rather than Android 14: recording the stock/slimBOX boot chain, understanding A/B partitions and the dynamic partition layout, identifying which DTB is actually loaded, and preserving a recovery path.

The audit established that the then-installed U-Boot uses an internal multi-DTB. Modifying the legacy `_aml_dtb` store did not change the active DTB, which mattered to the USB-device debugging work. The existing Android 11 environment was rooted and accessible; Widevine L3 protected playback was observed after the transition away from stock firmware.

Historical reports: [boot-chain notes](../research/BOOTCHAIN.md), [October audit](../research/archived/OPERATION-SALAMANKA-AUDIT-2026-10-26.md). These are not current flashing instructions.

## Early November — build a native Android 14 system

AOSP Android 14 was synced and configured with an ARM64 product. The project compiled system, system_ext, vendor, product, ODM and super images locally. Linux 6.18.55 was built for the SC2 hardware.

This included repeated fixes and investigations in Soong/Kati, SELinux types and file contexts, DMA-BUF device naming, VINTF manifests, and the graphics HAL. An early FCM interpretation was corrected: [Android 14 uses FCM 8](FCM-ANALYSIS.md), whereas `202404` belongs to Android 15.

Passing a build was only the beginning of hardware bring-up.

## Physical kernel and Android bring-up

ADNL/RAM experiments ran Linux 6.18.55 on the KM6 without replacing its existing installation. Android 14 `init` subsequently executed as PID 1. The first rounds aborted in early initialization and policy/kernel integration. Later iterations reached `zygote64`, `system_server` and Binder service registration.

A separate graphics effort brought up Meson DRM/KMS, Panfrost/Mesa and Android's display composition path at 1920×1080/60 Hz on the physical device. See [graphics](GRAPHICS.md).

## Stages 52 and 53 — boot-complete through NBD

To avoid writing an unfinished Android build to the device's eMMC, the experimental system used a RAM boot and Android images served from the development PC through NBD (Network Block Device).

| Stage | Reported observation |
| --- | --- |
| 52 | Natural `sys.boot_completed=1` at 101.70 s; 219 Binder services |
| 53 | Natural `sys.boot_completed=1` at 94.52 s; SystemUI and Leanback HOME activity reached |
| 53, UI trace | `libhwui` RenderThread `SIGABRT` during `CanvasContext::setupPipelineSurface` |

Android's framework really executed on the KM6; however, the storage used by the experimental boot was supplied by the PC. This is neither a persistent Android 14 installation nor evidence of a stable launcher.

## Stages 54–56 — eMMC initialization

The focus shifted to accessing the KM6 internal eMMC with Linux 6.18. A corrected test DTB moved MMC initialization beyond an earlier `-EINVAL` failure.

Stages 55 and 56 captured more precise low-speed card-enumeration behavior:

```text
Clock: 400 kHz
CMD0: completed
CMD1: completed
CMD2: completed
CMD3: SET_RELATIVE_ADDR, argument 0x00010000
      response timeout
SD_EMMC_STATUS = 0xa1ff2800
```

No local `/dev/mmcblk*` device is available from this modern kernel. The observed boundary is CMD3; the underlying cause is not yet proven. See [eMMC investigation](EMMC.md).

The latest audit reported **12 verified backup sets**, and the existing Android 11 installation remained bootable. The Stage 54–56 diagnostics did not write persistent bootloader, GPT or eMMC contents.

## Next experiment

Stage 57 was proposed as a read-only comparison of MMC controller state around CMD2 and CMD3: configuration, command/argument, responses, clocks and interrupt/status registers. It is a **planned discriminator**, not another completed milestone.

The project also still needs a working graphical home screen, native storage, hardware video decoding, audio, input, network, power management, security and a documented release/recovery process.

[Current status](STATUS.md) · [Test evidence](TESTING.md) · [Release gates](RELEASE-CRITERIA.md).
