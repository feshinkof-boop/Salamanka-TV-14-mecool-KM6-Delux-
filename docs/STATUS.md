# Salamanka TV 14 — current engineering status

**Updated: 16 November 2026 • Latest maintainer report: Stage 56 • Target: MECOOL KM6 Deluxe Rev 1 (Amlogic S905X4 / SC2 / AH212)**

> [!IMPORTANT]
> **Working physical Android 14 boot path demonstrated; production firmware NOT ready.** Android 14 has reached `sys.boot_completed=1` on the physical KM6 using temporary RAM boot and host-backed NBD storage. This is not an Android 14 installation on the internal eMMC, and no stable end-user TV interface has been demonstrated.

## At a glance

| Subsystem | Latest evidence-based position |
| --- | --- |
| AOSP Android TV 14, native ARM64 | **Built; executed on physical hardware** with 64-bit Android services. Full final architecture audit for every HAL not published. |
| Linux 6.18.55 kernel | **Physical bring-up achieved.** Mainline-oriented driver/DTB integration ongoing. |
| Core Android boot | **Milestone reached in RAM/NBD tests:** natural `sys.boot_completed=1`; 219 Binder services reported; SystemUI and Leanback HOME resumed. |
| GPU and display | **Physical progress:** Mali-G31/Panfrost, Mesa EGL/GLES, HDMI 1080p60, DRM/KMS, AIDL Composer3 and SurfaceFlinger. Stable visible home screen **not verified**. |
| Launcher and UI | **Partial:** Leanback activity resumes; `libhwui CanvasContext::setupPipelineSurface` / RenderThread SIGABRT observed. |
| Local eMMC under modern kernel | **Blocked:** CMD0–CMD2 succeed; CMD3 SET_RELATIVE_ADDR times out. No `/dev/mmcblk*` enumeration or native super access. |
| Temporary test storage | **Demonstrated:** host-served NBD backing Android images; NOT a standalone persistent installation. |
| Existing Android 11 / recovery | **Verified operational in latest audit:** 12/12 backups checked; installed Android 11 retained. |
| SELinux | **Not release-ready:** physical tests permissive; enforcing is an outstanding requirement. |
| Video hardware codecs | **Unverified:** native Android 14 MediaCodec/Codec2 hardware AVC/HEVC/AV1 path. |
| Audio, radios, voice remote and power | **Unverified or incomplete:** HDMI, optical SPDIF, analog, gigabit LAN beyond test transport, Wi-Fi, BT/V01 mic, suspend/CEC. |
| XCPE supply-chain security | **Research and tooling started, full provenance unverified.** No claim that this exact Rev1 box is infected. |
| Release | **Not available. Do not flash.** |

## Development effort — numbers with context

| Measure | Reported total | Meaning |
| --- | ---: | --- |
| Engineering stages | **56** | Staged investigation, changes, audits and repeated bring-up work; **not** 56 releases or a completion percentage. |
| Test-suite passes | **450** | Cumulative passing test checks in the latest reported full suite; not 450 distinct physical validations. |
| Test-suite skips | **3** | Cumulative skipped checks. |
| Technical assessment | **230 PASS / 1 SKIP / 34 PARTIAL / 17 BLOCKED / 0 FAIL** | A separate status/acceptance matrix; **17 blockers still exist**. |
| Backup verification | **12/12** | Verified backup sets in the latest recovery audit; does not imply every restoration scenario is proven. |
| Android Binder services | **219** | Observed in a reported boot; count is not a complete health/compatibility test. |
| Latest reported Android boot time | **94.52 s** | Temporary NBD-backed test boot, not a production startup benchmark. |

**Source of the numbers:** maintainer-shared OpenCode/local engineering reports through Stage 56, dated 16 November 2026. Full raw logs and source revisions are not yet in this public GitHub checkout. GitHub Actions tests for the small offline audit utility are **not** the 450 figure. These measures must not be added together or treated as independent test counts.

## Development timeline

**October — understanding and preserving the hardware.** Identified KM6 Deluxe Rev1's boot chain, A/B partition layout, embedded U-Boot multi-DTB selection, USB-gadget limitations and recovery constraints. Investigated the legacy firmware, root and Widevine behavior; archived audit previously recorded 29/29 checks. Work also included native ARM64 Linux exploration and access tooling.

**Early November — building the new operating system.** Synced/configured Android 14 AOSP, brought up a device product and cross-compiled system/vendor/product/ODM/dynamic-super artifacts. Built Linux 6.18.55 for ARM64; investigated SELinux policy collisions, VINTF matrix issues, DMA-BUF naming and composer compatibility. Compilation alone did not constitute a boot.

**November 12–14 — hardware Android bring-up.** Temporary ADNL/RAM boots on KM6 reached Android's ARM64 init and then progressed through `zygote64` and `system_server`. The physical graphics path progressed through Panfrost and Mesa EGL/GLES to HDMI 1920×1080@60, AIDL Composer3, SurfaceFlinger and DRM atomic commits. Rendering activity was captured in logs, without declaring a stable user-visible launcher.

**November 15–16 — operating system and storage investigation.** Progressed from earlier Android service restarts and netd/routing/NBD stalls to a natural `sys.boot_completed=1` using images served over the network from the Kubuntu workstation. Stage 52 reported **101.70 seconds** to completion and **219 Binder services**; Stage 53 reported **94.52 seconds**, SystemUI/app activity and Leanback HOME resumed. A RenderThread SIGABRT during graphics-surface setup remains. **These are physical KM6 tests with temporary host-served storage, not an eMMC-installed ROM.**

**Stages 54–56 — safer native-storage diagnosis.** Verified **12/12** backup sets and demonstrated return to the existing Android 11 installation. A corrected test DTB moved modern-kernel eMMC initialization past an earlier `-EINVAL` error, but it still failed later. Stage 55 observed low-speed initialization and successful CMD0/CMD1/CMD2. Stage 56 localized repeatable failure to **CMD3 SET_RELATIVE_ADDR (RCA 0x0001 at 400 kHz)**, with response-timeout status `0xa1ff2800`. Device storage is **not enumerated**, so local super/system cannot be read or installed through this kernel path. Card-versus-controller root cause remains unproven. **No persistent bootloader, environment, GPT, eMMC or separate Arch installation writes were made during the Stage 54–56 diagnostics.**

## Immediate technical priorities

1. Diagnose **CMD3 eMMC initialization timeout** with controlled read-only traces and board-specific DTB/controller evidence; do not guess at partition writes.
2. Investigate the **Android launcher RenderThread graphics-surface abort** and demonstrate a stable, human-visible UI.
3. Move from **temporary NBD-based experiments** to a recoverable native storage solution only after explicit safety gates.
4. Complete SELinux enforcing and reconcile Android 14 manifests/Composer/allocator policy with the running build.
5. Bring up real 4K hardware video decoding, HDMI/SPDIF/analog audio, V01 voice, Wi-Fi/Bluetooth, power management and sustained stability.
6. Audit origin, licensing, privileges and network behavior of all shipped components; produce device-specific acceptance evidence.

## Evidence labels and important limitations

- **PHYSICAL / RAM-NBD:** observed on real Rev1 hardware while a host supplies system data. Does **not** imply standalone eMMC boot.
- **HOST-BUILT / HOST-TESTED:** compilation or verification on Kubuntu. Does **not** imply working hardware.
- **RECOVERY-VERIFIED:** stated backed-up assets and the existing Android 11 recovery outcome; not a universal unbrick guarantee.
- **PLANNED:** features still dependent on implementation and release testing.
- **COMMUNITY REPORTED:** 4PDA observations, not independently reproduced.

Historically, slimBOX 11.46 provided Widevine L3 playback where earlier stock had supported L1; **nothing here promises Widevine L1, licensed Google services, or Netflix certification**. XCPE research does not prove this exact Rev1 unit infected.

**Do not publish a flashable image or instructions implying production readiness.** The full evolving local AOSP/kernel worktree, build outputs, sensitive device backups and detailed bring-up logs are not automatically available in this public GitHub repository.

See also [engineering effort](PROGRESS.md) · [release criteria](RELEASE-CRITERIA.md) · [roadmap](ROADMAP.md) · [security](../security/XCPE-VIDEOSTRONG.md).
