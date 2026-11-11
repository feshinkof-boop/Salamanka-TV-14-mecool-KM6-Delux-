# Boot chain, DTB, USB gadget and Linux work

Historical audited device: slimBOXtv ATV 11.46; later firmware may differ.

## Confirmed from October 2026 local readbacks

- Amlogic SC2 S905X4 AH212 embedded U-Boot / BL33 2019.01, built Dec 15 2022. eMMC boot0/boot1 copies matched the installed slimBOX bootloader.
- GPT `bootloader` partition uses a distinct DBLK-marked store; it is **not** equivalent to running boot0/boot1 code.
- BL33 contained a **multi-DTB**; the active FDT was selected internally. `common_dtb_load` and legacy `_aml_dtb` store were not consulted on the observed path because `fdt addr` succeeded.
- The previous external `_aml_dtb` patch was inert; live USB `controller-type` remained `0x03`, and USB ADB was not attached. Do not repeat the store-patch experiment without new evidence.
- U-Boot environment contained CRC-valid copies. U-Boot `irkey` timer primitive supports an offline-built timed startup-animation approach; on-device visual calibration was pending.
- Rooted Android network-ADB and Termux SSH worked in the October audit. **No device IP, SSH credential or unique serial is published here.**
- Alternate mainline Linux ARM64 rescue and RAM-only experiments were prepared as offline artifacts, **not conclusively booted on the physical board**.
- A native ARM64 Linux side project and a Debian PRoot environment are separate from the Android 14 release target.

## Historic DRM finding

Stock's L1 provisioning path had been observed, but slimBOX 11.46 reported L3 and failed L1 root of trust; protected L3 video playback succeeded. No proof of recoverable L1 under Salamanka exists.

## Safety

This documentation is historical evidence, not a flashing guide. Do not blindly execute archived scripts, blindly transplant DTBs, change AVB/TEE or write boot0/boot1. A signed, reversible test and physical owner-approved recovery plan come first.