# Salamanka TV 14

### Independent Android TV 14 • Native ARM64 • MECOOL KM6 Deluxe Rev 1

**Rebuilding the software foundation of an Amlogic S905X4 TV box—not just changing its launcher.** Salamanka TV 14 aims to turn aging but capable hardware into a modern Android TV and ARM64 development platform. The project combines AOSP, Linux kernel bring-up, graphics and media engineering, hardware debugging, and a security-first firmware design.

> [!IMPORTANT]
> **Experimental development — no public flashable firmware yet.** The physical KM6 has executed Android 14 and reached a natural `sys.boot_completed=1` in a temporary **RAM/host-backed NBD test environment**. This is **not** a verified persistent eMMC installation or a finished TV experience. Launcher rendering, internal eMMC support, media codecs, audio, connectivity and security gates still require work.
>
> **Latest verified project report: 16 November 2026 · Stage 56.** [Progress and effort](docs/PROGRESS.md) · [Engineering status](docs/STATUS.md) · [Краткий статус на русском](docs/STATUS-RU.md)

## The project in numbers

| Engineering effort reported through Stage 56 | Result |
| --- | --- |
| Documented engineering stages | **56** |
| Cumulative automated/host test-suite checks reported passing | **450** |
| Cumulative test-suite checks skipped | **3** |
| Engineering assessment matrix | **230 PASS · 1 SKIP · 34 PARTIAL · 17 BLOCKED · 0 FAIL** |
| Verified backup sets in latest recovery audit | **12 / 12** |
| Binder services in the Android 14 boot experiment | **219** |
| Physical TV box used for bring-up | **MECOOL KM6 Deluxe Rev 1** |

These are **maintainer-reported results from the local development environment**, not GitHub Actions metrics. The 450 figure is a **cumulative full-suite total**, not 450 different device validations. **0 FAIL in the assessment matrix does not mean the project is complete:** 34 items remain partial and 17 blocked. Complete local test reports and source changes have not yet been imported into this public repository.

## What has actually been achieved

- **AOSP Android 14 / 64-bit build:** system and related images generated; multiple compiler, SELinux, partition, VINTF and framework integration issues investigated.
- **Linux 6.18.55 on real S905X4 hardware:** native AArch64 kernel and early userspace reached through controlled temporary boots.
- **Real Android 14 execution:** `/init`, `zygote64`, `system_server` and a growing Android service stack started on the KM6.
- **Graphics progress:** Mali-G31/Panfrost with Mesa EGL/GLES, HDMI **1920×1080 @ 60 Hz**, DRM/KMS, AIDL Composer3 and SurfaceFlinger integration observed in physical experiments. GPU activity and boot-animation-related rendering were recorded in logs; a stable, visually confirmed finished interface is still outstanding.
- **Android boot milestone:** two reported temporary image boots reached `sys.boot_completed=1`; the later run took **94.52 seconds**, showed **219 Binder services**, and brought SystemUI and the Leanback HOME activity up. A `libhwui` RenderThread crash still prevents claiming a working launcher.
- **Repeatable recovery work:** 12 backup sets verified in the latest audit; the pre-existing Android 11 installation still boots. Recent eMMC/bootloader/GPT/other persistent partitions were not modified during the Stage 54–56 tests.

The recent Android test environment uses an image served from the Kubuntu development computer through **NBD**, rather than the KM6's internal eMMC. This is a major physical bring-up result, but not a release candidate.

## What is still blocking a release

**Native storage:** the modern-kernel eMMC controller progresses through early initialization but currently times out at **CMD3 (SET_RELATIVE_ADDR)**; local Android storage is not usable. **UI stability:** Leanback's RenderThread can abort during graphics-surface setup. **Media and peripherals:** hardware AVC/HEVC/AV1 decode, HDMI/SPDIF/analog audio, V01 microphone remote, Wi-Fi/Bluetooth, suspend/wake and long-term stability still require real-device validation. **Security:** SELinux enforcing and independent review of every imported proprietary component remain release requirements.

There is no percentage-complete claim or release date: compiling, booting, drawing frames and shipping a stable ROM are different milestones.

## Why ARM64, and why this hardware?

The KM6 Deluxe's quad Cortex-A55 S905X4 is a **64-bit** SoC, with 4 GB RAM, 64 GB eMMC, Gigabit Ethernet, Wi-Fi and a hardware AV1-capable VPU. Original factory firmware used a 32-bit Android userspace despite the 64-bit CPU. The project's requirement is **genuine native ARM64 Android userspace**, not a 32-bit ROM with a 64-bit kernel. This expands compatibility with applications and ARM64 Linux tooling, but does **not** guarantee more speed, Widevine L1, Google certification or working codecs without driver integration.

The broader vision is a versatile ARM computer with excellent TV capabilities. Planned components include a Media Engine (HDR/AFR/decoder diagnostics), Remote Manager (V01 voice and HID), Power Manager, Performance Manager, optional Network Suite and Linux ARM64 experiments. **These are goals, not already shipped features.** See [features](docs/FEATURES.md).

## Development beyond a typical firmware modification

Several weeks of work have gone into boot-chain and DTB analysis, board-specific ARM64 kernel configuration, AOSP image building, service-policy debugging, GPU/compositor bring-up, host-driven NBD boot infrastructure, repeated hardware tests, eMMC timing/command forensics, recoverability and the Videostrong/XCPE supply-chain investigation.

**The challenge is to preserve real hardware function while replacing the underlying OS—not to make a screenshot of a newer Android version.** [Read the project history and evidence boundaries →](docs/PROGRESS.md)

## Project resources

- **[Current engineering status](docs/STATUS.md)** — confirmed milestones, immediate blockers and what is not verified.
- **[Engineering history and effort](docs/PROGRESS.md)** — the work behind the milestone numbers.
- **[Russian status / Статус на русском](docs/STATUS-RU.md)** — short community-facing update.
- **[Roadmap](docs/ROADMAP.md)** · **[Release criteria](docs/RELEASE-CRITERIA.md)** · **[Hardware matrix](docs/HARDWARE.md)**.
- **[XCPE/Videostrong research](security/XCPE-VIDEOSTRONG.md)** · **[Security policy](SECURITY.md)**.
- **[Host-side ROM audit utility](tools/rom_audit.py)** and [synthetic tests](tests/test_rom_audit.py); these inspect files, **not** the KM6's current security state.
- **[Open engineering issues](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues)** · **[Contributing](CONTRIBUTING.md)**.
- **[4PDA KM6 Deluxe discussion](https://4pda.to/forum/index.php?showtopic=1007166)**.

## Public-source boundary

The **real, evolving AOSP tree, kernel modifications, runtime logs and large build products live on the local Kubuntu development workstation**; they are not all hosted in this GitHub repository. Public documentation summarizes the development reports available as of the stated date, and host-tool tests in GitHub Actions are independent of physical-device validation. Never flash the device based solely on a project-status claim; do not share TEE/DRM secrets, per-device identifiers or private recovery images.

## Support development / Поддержать проект / 支持开发

**[❤️ Support Salamanka TV 14 — English · Русский · 简体中文](SUPPORT.md)**

Voluntary contributions can help fund test hardware, driver research and development infrastructure. Verified public receiving addresses for **USDT on TRON/TRC20**, **TON** and **Bitcoin mainnet** are listed in [SUPPORT.md](SUPPORT.md). **USDT on TON is not enabled.** Contributions do not imply a release, early access or a guaranteed outcome.

## Licensing

No blanket license has been selected by the owner. See [project governance](docs/PROJECT-GOVERNANCE.md); AOSP, Linux and third-party components remain governed by their respective licenses.
