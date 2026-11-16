# What it has taken to build Salamanka TV 14

**Development record through Stage 56 · 16 November 2026**

A modern Android TV 14 firmware for the MECOOL KM6 Deluxe Rev1 is not a launcher replacement or a simple version-number update. The effort involves porting an operating system to hardware that was shipped with an older software stack, much of it tied to proprietary Amlogic components.

This page is intentionally about **engineering work and evidence**, not about a countdown to release.

## The scale of the work

**56 staged engineering iterations.** These covered bootloader and device-tree investigation, backups, early Linux ARM64 experiments, AOSP build configuration, graphics and Android service integration, repeated on-device RAM boot experiments, remote block transport, storage-controller debugging and release-security research.

**450 reported cumulative test-suite passes, 3 skipped.** These are outcomes of the local development full-suite runs, **not 450 unique physical-device tests**. The separate engineering matrix currently contains **230 PASS, 1 SKIP, 34 PARTIAL, 17 BLOCKED and 0 FAIL**. This matrix includes unresolved work: the project is not 100% complete, and "0 FAIL" is not a shipping certificate.

**12 of 12 backup sets verified.** Recovery work has been an engineering track in its own right: the existing Android 11 environment remains bootable, and the most recent Stage 54–56 eMMC investigation did not rewrite the bootloader, environment, GPT, internal storage or a separate Arch installation. Recovery scenarios are documented separately rather than casually assumed.

These are **maintainer-reported results** based on the local OpenCode/workstation reports. The full original logs and implementation repository are not yet mirrored here. They are presented as documented engineering milestones, not independently reproduced GitHub CI metrics or a timesheet; we do not invent person-hours, commit totals or money spent.

## The problem required several distinct engineering projects

### 1. Knowing what actually boots the device

The original vendor software does not provide a straightforward modern AOSP target. Early work reconstructed the real partition, environment, U-Boot and embedded device-tree selection logic, identified cases where a proposed DTB patch had no effect, and prepared reversible test approaches. Without this work, risky flash experiments would have been guesses.

### 2. Building Android 14 and a modern kernel

An AOSP 14 product, system/vendor/product/ODM partitions and dynamic-super artifacts were built locally. Linux 6.18.55 was compiled for S905X4/SC2 hardware. This required repeated configuration and policy iteration: build memory limits, SELinux types and labels, VINTF/FCM matrix compatibility, graphics allocator/device nodes, native 64-bit services and Android userspace startup.

A successful compiler exit is only the first major gate.

### 3. Getting Android onto the physical board without erasing the working installation

Instead of immediately overwriting eMMC, the project used controlled RAM boots and later host-provided NBD storage. That allowed observation of real Android `init`, `zygote64`, `system_server`, and many Binder services while keeping the existing Android 11 installation available.

The platform reached a natural `sys.boot_completed=1` in an NBD-backed physical experiment, with **219 Binder services** reported. At the later milestone, SystemUI and Leanback HOME were active but the launcher still hit a RenderThread abort. **This is major progress—not a finished TV interface.**

### 4. Bringing up a graphics stack rather than copying a boot animation

The physical KM6 showed Mali-G31/Panfrost and Mesa EGL/GLES progress, actual HDMI DRM/KMS mode setting at 1080p60, AIDL Composer3 and SurfaceFlinger communication, and recorded DRM atomic activity. The engineering challenge is now **stable rendering through the Android UI**, not simply displaying a static logo.

### 5. Turning storage failure into a reproducible hardware diagnosis

Modern-kernel internal eMMC access remains a release blocker. Investigation progressed from generic driver errors to a reproducible protocol boundary: low-speed eMMC commands **CMD0, CMD1 and CMD2 complete; CMD3 times out**. That is a much more actionable fault description, but it is **not a fix**. Until the underlying controller/card interaction is resolved, the test image still relies on the host computer rather than standalone internal storage.

### 6. Recoverability, security and long-term hardware functionality

The project has treated backup verification, safe rollback and read-only diagnosis as first-class tasks. It also investigates the Videostrong/XCPE supply-chain findings, rather than assuming generic vendor binaries are trustworthy. A clean release will need verified source provenance, safe permissions and SELinux enforcing.

The final product must also preserve the point of owning a TV box: hardware video acceleration, HDMI/SPDIF/analog audio, gigabit LAN, Wi-Fi/Bluetooth, original V01 voice control, HDR/AFR and standby. **Those requirements have not all passed physical Android 14 tests.**

## Visible milestones, not imaginary percentages

| Period | Real milestone | Remaining gap at that point |
| --- | --- | --- |
| October 2026 | Board/boot-chain audit, DTB and rollback findings | No modern Android userspace running |
| Early November | AOSP Android 14 images and Linux ARM64 kernel built | Build success did not prove device boot |
| Mid November | Physical Android 14 init, Zygote, system_server, GPU/compositor activity | Incomplete services, stability, persistent storage |
| 15–16 November | Natural Android 14 boot-complete milestone, SystemUI/Leanback, 219 Binder services | Launcher RenderThread abort; no confirmed finished visual experience |
| 16 November, Stage 56 | Verified backup/recovery and isolated modern-kernel eMMC CMD3 timeout | Internal storage inaccessible; no standalone flashable release |

A percentage like "90% complete" would mislead contributors. A working boot with incomplete drivers and unsafe recovery can still require substantial work. The project will use evidence-backed milestones and hardware acceptance criteria instead.

## How to help

Developers with Amlogic SC2/S905X4 experience, modern Linux eMMC/MMC drivers, AOSP `init`/VINTF/SELinux, Panfrost/DRM/KMS, Android HWUI/SurfaceFlinger, VPU decode, ASoC audio, Bluetooth remote/voice and OTA security expertise can help with specific unresolved issues.

- [Current evidence-based status](STATUS.md)
- [Open issues](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues)
- [Hardware acceptance requirements](HARDWARE.md)
- [What a safe release must demonstrate](RELEASE-CRITERIA.md)

**We are not reviving a launcher. We are rebuilding an operating system on real hardware, one verified subsystem at a time.**
