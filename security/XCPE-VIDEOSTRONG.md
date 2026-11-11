# XCPE / Videostrong security research — 2026-11

**Primary reports**
- Google Threat Intelligence (2026-11-02): https://cloud.google.com/blog/topics/threat-intelligence/shutting-the-door-on-the-xcpe-botnet
- Synthient: https://github.com/synthient/public-research/tree/main/2026/11/Videostrong
- Plume: https://www.plume.com/resources/the-x-cpe-botnet and https://cdn.plume.com/3d/92/f7c576bd4afabd79df4e7b39ca7f/xcpe-botnet-whitepaper-10-2026.pdf

## What is established

Google said it disrupted XCPE access to **over 1.3 million compromised Android-based devices**, mainly TV boxes, and assessed **with high confidence** that Videostrong intentionally developed/deployed/operated the framework for profit. It described preinstalled firmware components, modular remote command-and-control, proxy monetization, ad fraud and malware delivery. This is documented threat-intelligence attribution, not a criminal conviction.

Google reported barring Videostrong from future certified Android production/supply, severing its business relationship and taking legal action against botnet infrastructure. It **did not establish** universal revocation of every old MECOOL device certification or Widevine key.

## Firmware persistence

Variants used packages `x.cpe` or `com.oemservice`; in some cases a restoration copy on `/oem` could reinstall an instance after removal. `com.abc.nexus`, `com.android.system.ntp`, `com.android.sso.auth.handler` appear in reported stages. Installers had or obtained privileged rights, loaded DEX/APK/ELF components and contacted external C2.

A factory reset, `pm disable-user`, or `pm uninstall --user 0` does not prove eradication if source images or separate privileged components remain.

Historical infrastructure included `mcstb.anyevonline.com:8000` and MQTT on `mqtt.szbboys.com`. These are indicators for offline matching, **not hosts to browse, probe, connect to, or contact**. Published IOCs are not complete forever.

## What is *not* established

- The specific 4GB/64GB **KM6 Deluxe Rev1** device in this project has **not** been forensically proven infected. Synthient lists an observed `KM6` model string, not this precise retail revision. Some 4PDA Deluxe owners report finding a suspect package; this does not identify our firmware hash or persistence.
- No reviewed primary report proved Google's account passwords were stolen or that a system-wide keylogger ran on this exact unit.
- No primary research demonstrated XCPE implant persistence in the KM6 boot ROM, bootloader, TEE, eMMC controller firmware or hardware.
- Neither stock V4.20201026 nor slimBOX 11.46/11.47 is proven clean merely by release date or removing known package names.

## Threat model for independent ROM

**Attack paths:** imported OEM APK, privileged HAL library, native ELF daemon, init service, OTA/updater, `/oem`, `/odm`, dormant `/data` installer, malicious signing/update chain or other bootable slot.

**Controls:** fully pinned AOSP build; SBOM and SHA256 for every binary; manufacturer blob allowlist with documented purpose; scan strings/DEX/ELF/imports/receivers/permissions/URLs; vendor HAL least privilege; no generic outbound MQTT or remote execute; SELinux enforcing; user builds; verified OTA signatures; AVB/rollback only after safe device testing; clean factory-reset/post-reboot capture.

**Immediate device handling:** isolate from trusted networks, do read-only examination first; do not authenticate sensitive accounts on an untrusted build. A security scanner must not automatically delete applications, rewrite partitions, boot recovery, or fetch untrusted code.

## Certification/DRM

GMS certification, Play Protect scanning and Widevine hardware protection are distinct. The historical project proved L3 DRM playback but lost L1 on slimBOX 11.46. Publishing a clean AOSP ROM does not confer Google licensing or restore TEE keys. Do not copy DRM keys between devices.