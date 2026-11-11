# Sources and research provenance (reviewed through 2026-11-12)

## Device-specific
- https://4pda.to/forum/index.php?showtopic=1007166
- https://4pda.to/forum/index.php?showtopic=1007166&st=20000
- https://4pda.to/forum/index.php?showtopic=1007166&st=20060
- https://4pda.to/forum/index.php?showtopic=1007166&view=findpost&p=145956348
- https://4pda.to/forum/index.php?showtopic=993324&st=21620
- https://slimboxtv.ru/mecool-km6/
- https://discourse.coreelec.org/t/installing-corelec-on-mecool-km6-classic-deluxe/50771

## Threat intelligence (2026)
- https://cloud.google.com/blog/topics/threat-intelligence/shutting-the-door-on-the-xcpe-botnet
- https://github.com/synthient/public-research/tree/main/2026/11/Videostrong
- https://www.plume.com/resources/the-x-cpe-botnet
- https://cdn.plume.com/3d/92/f7c576bd4afabd79df4e7b39ca7f/xcpe-botnet-whitepaper-10-2026.pdf

## Prior local evidence
- 2026-10-26 local audit report and bootloader/DTB analysis (sanitized archive files in this repository).
- Nov 2026 build status reported by owner; original source tree and artifacts have **not** been uploaded here.

## Source confidence

An independent technical investigation by Google is not interchangeable with a community hypothesis. A report about KM6 Classic, Rev2 or a different S905X4 board does not establish the same behavior on Deluxe Rev1. The Synthient `KM6` identifier alone is not a unique infection confirmation of our unit.
## Authoritative Android compatibility references
- https://source.android.com/docs/core/architecture/vintf/fcm — FCM 8 for Android 14; 202404 for Android 15.
- https://source.android.com/docs/core/graphics/aidl-hwc — AIDL Composer3 and HIDL deprecation.
