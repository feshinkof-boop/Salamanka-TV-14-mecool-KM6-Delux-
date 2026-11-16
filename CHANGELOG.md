# Development log

**16 Nov 2026 — Stage 56:** Reproduced eMMC CMD3 timeout under Linux 6.18 after CMD0–CMD2 succeeded. Existing Android 11 still boots. Latest local checkpoint reported as `2e06096` (not mirrored here).

**15–16 Nov — Stages 52–53:** Android 14 reached natural `sys.boot_completed=1` on the physical KM6 with RAM/NBD-backed storage; Stage 53 reported 94.52 s and 219 Binder services. SystemUI/Leanback reached, but HWUI RenderThread abort remained.

**Early–mid Nov:** AOSP Android 14 and Linux 6.18.55 builds; real init/Zygote/system_server bring-up, Panfrost/Mesa DRM/KMS and Composer3/SF integration.

**October:** Existing firmware/boot-chain investigations, partition readbacks and recovery preparation.

Full chronology: [docs/BRINGUP.md](docs/BRINGUP.md). These entries are local development milestones, **not** public firmware releases.
