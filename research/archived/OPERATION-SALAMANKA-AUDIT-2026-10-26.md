> [!CAUTION]
> HISTORICAL ARCHIVE: not current instructions and NOT a verified recovery procedure. Original local file was sanitized for public display. No bootloader, env, DTB, TEE or firmware write should be performed from this text without independent verification and explicit approval. Private IPs/device serials have been redacted.

# FINAL REPORT — OPERATION SALAMANKA
## KM6 autonomous audit, repair and development

**Date:** 2026-10-26 (UTC) · **Device:** Mecool KM6 Deluxe Rev 1 (SC2 / AH212)
**Session:** autonomous, owner unavailable
**Mission directory:** `/home/salamanka/km6-lab/KM6_AUTONOMOUS_AUDIT_2026-10-25`
**Nature:** investigation + offline implementation; **no bootloader, env, DTB, logo, AVB or tee
write was performed**, and no unsafe reboot.

---

# 1. Executive summary

The device is **healthy, rooted and remotely reachable**, running **slimBOXtv ATV 11.46**
(Android 11, kernel 5.4.125) flashed on 2026-10-20. The previous state (stock Android 10,
U-Boot 2021, L1 Widevine) is gone. The installed bootloader is SlimBOX's own 2022 Superceleron
U-Boot 2019.01 build.

Three headline results:

1. **The 2026-10-20 `_aml_dtb` patch is provably inert.** The bootloader uses its own internal
   multi-DTB; the store area is never consulted because `storeboot`'s `fdt addr` succeeds first.
   Live `controller-type` is still `0x03`, which is why USB ADB is dead.
2. **A genuine pre-Android timed animation is possible after all** — not because `sleep` exists
   (it does not), but because the vendor `irkey` command is a microsecond-class timer wait
   (`0xfe0100ec`), and the IR device is enabled in U-Boot's control FDT. 8/12-frame SALAMANKA
   sequences, a static 1080p logo, and the corresponding env images are built and validated
   offline. Timing needs one visual calibration boot.
3. **Widevine L1 is lost, but L3 works end-to-end.** The CDM is L3; provisioning, licence
   acquisition and **protected playback are verified** (Media3/ExoPlayer, first frame 1,958 ms,
   >60 s). The L1 Root of Trust is rejected (`keybox error 25`, `Bad Level 1 Root of Trust`).
   Stock had a verified L1 path. This is a vendor/TEE-keybox firmware regression, not a hardware
   limit.

The laboratory was reorganised into a mission directory with an inventory, evidence index, issue
register, changes log, scripts, tests and deployable artifacts. All original evidence was
preserved.

---

# 2. Q1 — What is the KM6's actual current state?

| item | value |
|---|---|
| Connection | **network ADB only**: `[PRIVATE-LAN-ADDRESS]`; no Amlogic USB device enumerated |
| Model / product | `Mecool_KM6` / `ohm` |
| Serial | `[REDACTED-DEVICE-SERIAL]` (not published) |
| Firmware | SlimBOXtv ATV 11.46 (Android 11, `RD2A.211001.002`, userdebug/test-keys) |
| Security patch | 2023-06-05 |
| Kernel | `5.4.125-android11-2-g654a19776817` (2022-05-17) |
| Bootloader | U-Boot `2019.01-g42a9be9793` (2022-12-15), version `01.01.221215.194137` |
| Slot / AVB | `_a`; `verifiedbootstate=green`; `flash.locked=1`; AVB 1.1 |
| SELinux | Permissive |
| Root | Magisk 30.7 |
| Active DTB | `sc2_s905x4_ah212-4g`, `controller-type=0x03` |
| USB gadget | UDC `fdd00000.dwc2_a`, **not attached** |
| DRM | Widevine **L3, provisioned, protected playback verified**; L1 unavailable; PlayReady unsupported |
| Storage | eMMC 58 GiB, A/B dynamic partitions; userdata ~53 GiB |
| Remote | SSH:8022 (Termux, autostart), LAN ADB:5555; Tailscale app present but not connected |

It is a **modified, non-stock, A/B Android 11 device**, not the original Android 10 firmware.

---

# 3. Q2 — What firmware and bootloader components are installed?

* **eMMC boot0 and boot1** are byte-identical for the first `0x319000` bytes and equal SlimBOX
  11.46's `bootloader.PARTITION` (sha256 `a4bc877b…`, sha1 `65a63bba…`). The vendor flash log
  `oem verify sha1sum 65a63bba…` confirms this payload was written.
* The **4 MiB GPT `bootloader` partition** is a **different DBLK store** (`ef be ad de`, `@ML`, `DBLK_PAYLOAD_END`). It is not the running code; preserved as
  `bootloader-gpt-20261025.img`.
* **U-Boot** is LZ4C-compressed at file offset `0x198010`; decompression yields 1,370,936 bytes of
  `U-Boot 2019.01-g42a9be9793 (Dec 15 2022)`. The **original 2021 bootloader** is also preserved
  (`~/KM6-Startup/bootloader-analysis/bootloader-original.bin`, 512-byte zero prefix; stripped
  copy in `evidence/bootloader/bootloader-original-2021.shifted.bin`, U-Boot
  `2019.01-g5f543bb605-dirty`, Jan 27 2021).
* **U-Boot control FDT** at decompressed `0x10d6c0` describes `Amlogic Meson SC2 S905X4 AH212
  Board` and enables `meson-ir`, `fb`, `vpu`, `osd`, `dwc3`, USB PHYs.
* **Environment** is 8 MiB with two CRC-valid 64 KiB objects (block 0 current, block 1 older).
  The original 2021 env is preserved (`env-original-2021.img`, 103 vars, SELinux enforce).
  The boot logic is reconstructed in `docs/BOOTLOADER_DTB_ANALYSIS.md`.
* **Kernel DTB** is the bootloader-internal `sc2_s905x4_ah212-4g` table (structurally table 2 of
  the flashed `_aml_dtb` container plus U-Boot/kernel edits).
* **Logo partition** is SlimBOX's AML_RES v2 container (920,800 B logical, CRC valid, 8 resources).
* **Vendor** contains SlimBOX's Widevine stack (CDM 16.0.1, `liboemcrypto.so` 71,492 B), **not**
  the stock stack (CDM 15, 98,916 B). `tee` was **not** flashed.

---

# 4. Q3 / Q4 — Which historical research was right, and which was wrong?

### Correct and independently reproduced

* U-Boot 2019.01; Magisk 30.7; Android 11; SELinux Permissive; A/B layout.
* The `_aml_dtb` store is not the live DTB source; the bootloader's embedded DTB wins.
* The live DTB is the AH212 4 GB table (`sc2_s905x4_ah212-4g`).
* The USB PHY is forced to host mode; `controller-type=3` + `phy-interface=2` + `otg=0`.
* Stock Widevine L1 provisioning/playback history (verified on stock, not transferable).
* The logo container format (AML_RES v2, 8 resources, gzip BMP, RGB565).
* The flash log's DTB/partition write sequence; the store read-back was genuine.

### Wrong, contradicted or obsolete

| prior claim | correction |
|---|---|
| "`autoscr` is absent" (Deep Audit 05/08) | **Present** in the installed 2022 SlimBOX build (command + help + env macro). The earlier `KM6_EXTERNAL_BOOT_CORRECTED_DIAGNOSIS.md` was right for this bootloader. |
| "The `_aml_dtb` patch will fix USB" | It is **inert**; live DTB still `0x03`. |
| "Widevine L1-capable" (current) | Current firmware is **L3**; L1 only on stock. |
| "KM6 connected via USB" | No USB enumeration; network ADB only. |
| "Termux/Tailscale absent after flash" | Both installed now; SSH autostart works. |
| "SlimBOX bootloader is Tanix X4-based" | **Unverified.** The build paths are Superceleron/AOSP 11; the control FDT is AH212. Do not repeat as fact. |
| "`tee`/keys may have been wiped by the flash" | `tee` was not flashed; the L1 failure is a CDM/keybox-contract mismatch, not a wiped TEE. |
| "No autoscr → no external script path" | Reopened; the external `update`/`aml_autoscript` route is evidence-supported but **not executed**. |

---

# 5. Q5 — What previously unidentified information was discovered?

1. **`irkey` is a timer primitive.** The U-Boot command `irkey <timeout> <keys>` waits on the
   Amlogic AO timer at `0xfe0100ec`, returns `0` and sets `irkey_value` on a match, and loops until
   timeout otherwise. This enables both a timed frame sequence and an IR-driven selector.
2. **The installed 2022 bootloader has `autoscr`/`source`.** It is not the same command set as the
   2021/2024 OEM images analysed earlier.
3. **The GPT `bootloader` partition is a DBLK store**, distinct from boot0/1.
4. **The exact L1 failure** is `cmd 1005 return 16` + `Bad Level 1 Root of Trust` + `keybox error
   25`, not a generic "unprovisioned" state. Provisioning at L3 works.
5. **The SlimBOX vendor replaced the whole Widevine stack** (sizes/hashes above).
6. **The boot logo primary path is `rdext4pic` from `odm_ext_a:/logo_files/bootup.bmp`**; that file
   is absent today, so the fallback logo partition is used.
7. **`env` block 0 is current** (matches `/proc/cmdline`); block 1 is an older 8-bit/checksum-0
   env. A safe env writer must update both.
8. **A mainline 6.18.55 SC2 AH212 DTB exists in the lab**, with framebuffer console and Ethernet
   built in — making an HDMI-visible external Linux proof plausible.

---

# 6. Q6 / Q7 — What was fixed, and what was modified?

### Fixed / resolved

* Reconstructed the real boot chain and proved why the previous USB fix failed (**root cause
  complete**).
* Recovered the full U-Boot environment and built a verified offline env editor.
* Decompressed and verified the installed U-Boot; enumerated its real command set.
* Resolved the `autoscr` contradiction.
* Established the true Widevine level and root cause; restored at least **working L3
  provisioning/session/licence**.
* Established the real external-boot route and built a validated mainline rescue payload.
* Built a reproducible startup asset pipeline and guarded deployment scripts.

### Modified (details in `CHANGES.md`)

* Installed the diagnostic APK `km6.drmprobe`.
* Performed **one** legitimate L3 Widevine provisioning (persistent certificate).
* Created and removed `/dev/mem` during a diagnostic attempt.
* No bootloader/env/logo/DTB/AVB/tee writes; no reboot.

---

# 7. Q8 — What tests were performed?

| test | result |
|---|---|
| Fresh 37-file live audit | PASS (all captured) |
| Bootloader identity cmp/hash | PASS (live boot0/1 == SlimBOX payload) |
| U-Boot LZ4C decompression | PASS (1,370,936 B, version verified) |
| Env CRC parse (both blocks) | PASS |
| Env patch round-trip (test var) | PASS (both blocks, CRC valid) |
| Live DTB decompile/diff vs table 2 | PASS (structural match + known edits) |
| `_aml_dtb` patch effect | **FAIL to change live DTB** (expected; proves inertness) |
| AML_RES verify (live + stock) | PASS (CRC, offsets, gzip, BMP) |
| New static BMP validator | PASS (16bpp, BI_BITFIELDS, masks, 4,147,272 B) |
| AML_RES repack with new bootup | PASS (CRC, 8 resources) |
| 8/12-frame U-Boot env images | PASS (CRC, both blocks, preboot) |
| Android bootanimation zip | PASS (90 frames, desc, 5.29 MB) |
| Magisk module zip | PASS (contains animation) |
| Mainline payload validation | PASS (mkimage, DTB model, ARM64 magic, initramfs) |
| Stock-kernel experiment B validation | PASS (mkimage, bootimg header) |
| Deploy scripts syntax + `--check` | PASS (read-only) |
| Widevine Probe (pre) | L3, NotProvisioned |
| Widevine Phase A (local) | PASS (4,687 B request, googleapis host) |
| Widevine provisioning | PASS (HTTP 200, openSession L3) |
| Widevine licence | PASS (HTTP 200, keys accepted) |
| Widevine L3 playback | **PASS** (Media3/ExoPlayer, first frame 1,958 ms, >60 s) |
| SSH/ADB/root after reboot | PASS |
| Tailscale | not connected (no interface) |

---

# 8. Q9 / Q10 — What remains unresolved, and why?

| issue | blocker |
|---|---|
| USB ADB fix | requires a live DTB change: env `preboot` write, external RAM override, or bootloader edit. The RAM-only test is packaged; **owner-present boot needed** |
| L1 Widevine | vendor/TEE keybox mismatch; needs stock reflash or a risky vendor-stack experiment. **External/firmware dependency** |
| PlayReady/HDCP | PlayReady scheme absent; HDCP reports none; **vendor stack limitation** |
| Animation timing | `irkey` timeout is in µs (evidence below); visual calibration still recommended; **one boot** |
| Static logo visual proof | **one boot** |
| Embedded DTB raw extraction | container/compression not decoded; **not needed** for the current plan |
| DBLK partition semantics | unidentified; preserved, do not overwrite |
| Mainline Linux boot | **not executed**; needs USB stick + one `reboot update` |
| Wi-Fi on mainline | BCM43752 firmware/CLM/NVRAM missing; **external dependency** |
| Audio/GPU/VPU on mainline | known mainline gaps; later stage |
| Ethernet | physical cable test |
| Tailscale | owner login |
| Android AutostartApp crash | cosmetic; reversible disable available |
| Full multiboot selector | design only; depends on the Linux proof |

---

# 9. Q11 — Safest viable bootloader customization approach

**Do not replace or patch the bootloader.** Use, in order:

1. **Static logo**: write `/logo_files/bootup.bmp` on `odm_ext_a` (ordinary file; no boot-critical
   partition). This is the lowest-risk branding path and is prepared.
2. **Timed animation**: env `preboot` + frames on `odm_ext_a` (variant A). The env write is
   boot-critical but reversible: live env backup + CRC-verified image + rollback script. The
   animation is a sequence, not a smooth video.
3. **USB fix / Linux**: external `aml_autoscript` via `reboot update`, with a RAM-only `fdt set`
   and a RAM-only initramfs. No persistent change; a normal reboot returns to Android.
4. **Only if unavoidable**: bootloader-internal DTB or logo partition (variant B) — higher risk,
   owner-approved, with full backups.

The env route is safer than the logo partition because the original env is a small, known,
restorable blob; the logo partition is also restorable (we have the live 8 MiB image) but a corrupt
container affects the boot logo only, not the boot chain.

---

# 10. Q12 — Can SALAMANKA OS have a genuine pre-Android animated startup?

**Yes — a genuine timed frame sequence, with caveats.** The installed U-Boot has no `sleep`/
`mdelay`/`udelay`, but `irkey` is a timer wait. A `preboot` script can:

```
ext4load mmc 1:15 ${loadaddr} /logo_files/salamanka_0.bmp
bmp display ${loadaddr}; bmp scale
irkey 150000 0xffffffff
... repeat for 8 frames ...
run load_bmp_logo; bmp scale
```

This runs **before Android**, after `init_display` has enabled HDMI/OSD. It is a designed
slideshow (8–15 fps equivalent), not a 30 fps video. The delay unit must be calibrated once
(µs, see `docs/BOOTLOADER_DTB_ANALYSIS.md` §4). The static logo is the fallback/final frame, so a
timing error cannot leave a blank screen.

**What is not possible:** a smooth high-frame-rate animation, alpha-blended motion, or a real
animation engine in this U-Boot. Android's `bootanimation.zip` provides that later, after the
kernel (~11 s), and is prepared as a Magisk module.

---

# 11. Q13 — What boot graphics and startup components are prepared?

* `salamanka_bootup_1920x1080.bmp` — static SALAMANKA matrix logo, exact U-Boot BMP layout.
* `salamanka_logo_8mb.img` — 8 MiB logo partition image with the static logo (alternative).
* 8 × 960×540 RGB565 frames + env image A (odm_ext route).
* One-shot RAM animation test (`uboot-anim/experiment-C/`) — no persistent change.
* 12 × 1920×1080 frames + 8 MiB AML_RES container + env image B (logo route).
* `bootanimation.zip` — 1280×720, 24 fps, 30 intro + 60 loop frames, Matrix style.
* `salamanka_bootanim_module.zip` — Magisk systemless module.
* `salamanka_concept.png` — static design preview.
* Reproducible generators, validators, AML_RES tool, env tool, deploy/rollback scripts.

All are **offline validated**; none is deployed.

---

# 12. Q14 — SlimBOX/Android compatibility status

Working: boot, root, Magisk persistence, LAN ADB, SSH autostart, Wi-Fi, Google services, Cast
remote service, GPU driver, HDMI audio route, thermal (43–45 °C idle), storage.

Defects: USB ADB dead (bootloader DTB), Widevine L1 lost (L3 only), PlayReady removed, HDCP
reports none, `tv.autostart` crash, Wi-Fi boot warnings, Ethernet untested, SELinux permissive.
No critical Android failure. The SlimBOX build is usable; the DRM/USB regressions are the price of
the port.

---

# 13. Q15 — Actual Widevine provisioning status

* CDM: Google Widevine 16.0.1@005, systemId 29560.
* **Level: L3.** Provisioning completed (HTTP 200), `openSession` succeeds, public test licence
  accepted.
* **L1 unavailable:** TEE L1 init succeeds, but `cmd 1005` fails and the CDM reports
  `Bad Level 1 Root of Trust`, keybox error 25 → L3 fallback.
* **Playback:** **L3 verified** with Media3/ExoPlayer (Shaka Sintel DASH): first frame 1,958 ms,
  non-secure VP9 decoder, >60 s, ABR 1920×818. L1 remains unavailable.
* **L1 restoration:** stock firmware (proven) or a vendor-stack experiment (risky, not done).
* No keys/certificates were extracted or logged.

---

# 14. Q16 — What Linux support is available?

* The SoC is AArch64; the stock kernel is 64-bit.
* **Mainline 6.18.55-meson64** with an SC2 AH212 DTB is available in the lab; config has
  framebuffer console, DRM Meson, stmmac Ethernet, DWC2, USB gadget/RNDIS (modules).
* **Ready now:** external USB boot prototype (kernel + DTB + RAM initramfs), HDMI/serial console,
  Ethernet, RAM-only diagnostics.
* **Not ready:** onboard Wi-Fi (missing BCM43752 firmware/CLM/NVRAM), audio (known mainline gap),
  GPU/VPU acceleration (DT clock issues), Bluetooth, thermal policy, full desktop.
* **Recovery:** external boot is RAM-only; Android remains intact. UART is the reliable fallback.
* **BlackArch ARM64:** feasible as a userspace/rootfs goal after a Debian/Arch boot proof; no
  turnkey KM6 image.

---

# 15. Q17 — Technically defensible native ARM64 multiboot path

1. Keep eMMC Android untouched.
2. Boot a **mainline rescue kernel/initramfs from USB** via the verified `reboot update` →
   `usb start` → `aml_autoscript` → `autoscr` path (no persistent change).
3. Add an external root filesystem (USB) and a Linux-level selector (framebuffer menu with a
   timeout) that can return to Android by reboot or kexec another Linux kernel.
4. Later, optionally, an **IR-driven U-Boot menu** using `irkey` + `irkey_value` + `bmp display`
   (env write, owner-approved).
5. Do **not** repartition eMMC or replace the bootloader for the first three phases.
6. Treat Android+slimBOX coexistence as a separate, later project requiring independent data,
   vendor and AVB contracts.

The external `aml_autoscript` route is now evidence-supported on this bootloader, but it has **not
been executed**; that is the first gate.

---

# 16. Q18 — Which components are ready for deployment?

| component | readiness |
|---|---|
| Static boot logo (odm_ext) | **READY** — BMP validated; deploy script `--check` passed |
| Pre-Android animation A (odm_ext + env) | **READY OFFLINE** — frames + env CRC-valid; timing calibration needed |
| Pre-Android animation B (logo + env) | **READY OFFLINE** — container + env CRC-valid; higher risk |
| Android bootanimation + Magisk module | **READY OFFLINE** — zip/module valid |
| Mainline rescue USB | **READY OFFLINE** — payload/hashes validated |
| Stock-kernel RAM USB experiment | **READY OFFLINE** — script validated |
| Devmfc Debian USB | image ready; needs a ≥2 GB stick and Phase 1 success |
| Env/DTB tools | **READY** — tested round-trip |
| Analysis reports | **COMPLETE** |

---

# 17. Q19 — Which changes require physical testing or interactive approval?

**Interactive approval (boot-critical / persistent):**

1. Writing `env` (animation, or any `preboot` change).
2. Writing the `logo` partition (variant B).
3. Writing `/logo_files/bootup.bmp` on `odm_ext_a` (low risk, but a boot-display change).
4. Any bootloader/DTB/AVB/tee operation (not prepared for execution).

**Physical presence (one boot):**

5. Static logo display check.
6. Animation timing calibration and visual check.
7. Mainline rescue boot (USB stick, HDMI/serial observation).
8. RAM USB fix experiment (USB stick, host USB network observation).
9. Devmfc Debian boot (USB stick).
10. Ethernet cable test.

---

# 18. Q20 — Exact remaining steps to reach the intended final state

### Gate 0 — owner present, 15 minutes

1. Run `scripts/deploy_logo_odm_ext.sh --approve`, reboot, confirm the SALAMANKA static logo.
2. If it shows: the earliest-stage branding goal is complete.

### Gate 1 — animation (one boot)

3. Run `scripts/deploy_startup_animation.sh --variant A --approve`.
4. Reboot; observe. If frames flash, multiply the `irkey` values by 1000; if slow, divide.
5. Re-deploy or roll back. The final static logo must remain.

### Gate 2 — USB fix / Linux (one boot each)

6. Copy `artifacts/linux-rescue/usb/*` to a FAT32 stick; `reboot update`; observe HDMI.
7. If no HDMI: try `experiment-B` (RNDIS) and/or UART.
8. Once Linux boots: verify Ethernet, storage, thermal; then write the Devmfc image to a ≥2 GB USB
   and repeat.
9. Add BCM43752 firmware if Wi-Fi is required; accept no audio/GPU for now.

### Gate 3 — multiboot

10. Build the Linux framebuffer selector; test return-to-Android and kexec.
11. Optionally prototype the IR menu; never make it the only entry path.
12. Keep eMMC Android intact until a full recovery path is proven.

### Gate 4 — DRM decision

13. Choose: accept L3, restore stock for L1, or approve a systemless vendor-stack experiment.
14. Do not promise L1 on SlimBOX.

---

# 19. Completed-task register

| # | task | status |
|---:|---|---|
| 1 | Locate labs, audit archive, firmware, reports | VERIFIED COMPLETE |
| 2 | Fresh 37-file device baseline | VERIFIED COMPLETE |
| 3 | Identify bootloader/env/DTB/logo | VERIFIED COMPLETE |
| 4 | Reconstruct boot flow | VERIFIED COMPLETE |
| 5 | Prove `_aml_dtb` inertness | VERIFIED COMPLETE |
| 6 | Decompress/verify U-Boot + command set | VERIFIED COMPLETE |
| 7 | Resolve autoscr contradiction | VERIFIED COMPLETE |
| 8 | Discover `irkey` timer primitive | VERIFIED COMPLETE |
| 9 | Build AML_RES tool + validate containers | IMPLEMENTED — OFFLINE VALIDATED |
| 10 | Build static logo + BMP validator | IMPLEMENTED — OFFLINE VALIDATED |
| 11 | Build 8/12-frame U-Boot animation + env images | IMPLEMENTED — OFFLINE VALIDATED |
| 12 | Build Android bootanimation + Magisk module | IMPLEMENTED — OFFLINE VALIDATED |
| 13 | Build env tool + patch round-trip | IMPLEMENTED — OFFLINE VALIDATED |
| 14 | Build mainline rescue payload | IMPLEMENTED — OFFLINE VALIDATED |
| 15 | Build stock-kernel RAM USB experiment | IMPLEMENTED — OFFLINE VALIDATED |
| 16 | Widevine level/provisioning diagnosis | VERIFIED COMPLETE (L3, L1 blocked) |
| 17 | L3 playback proof | VERIFIED COMPLETE |
| 18 | Termux/SSH/Tailscale audit | VERIFIED COMPLETE |
| 19 | Mainline Linux feasibility + design | INVESTIGATED — DESIGN COMPLETE |
| 20 | Multiboot design | DESIGN COMPLETE |
| 21 | Registers, inventory, evidence index | VERIFIED COMPLETE |
| 22 | Deploy static logo / animation | BLOCKED — REQUIRES DEVICE / OWNER |
| 23 | Execute Linux boot | BLOCKED — REQUIRES DEVICE / OWNER |
| 24 | Restore L1 | BLOCKED — EXTERNAL / FIRMWARE |

---

# 20. Test results (summary)

```
PASS  live audit (37 captures)
PASS  bootloader identity (boot0 == boot1 == SlimBOX payload)
PASS  U-Boot LZ4C decompress + version
PASS  env CRC (2 blocks) + patch round-trip
PASS  live FDT decompile + table-2 structural comparison
PASS  AML_RES verify (stock/live) + repack CRC
PASS  static BMP 16bpp BI_BITFIELDS validator
PASS  U-Boot animation env images (A/B, both blocks)
PASS  Android bootanimation zip + Magisk module
PASS  mainline payload (mkimage/DTB/Image/initramfs)
PASS  experiment-B payload (mkimage/bootimg)
PASS  deploy scripts syntax + read-only preflight
FAIL* _aml_dtb store write does not change live DTB (expected; proves inertness)
PASS  Widevine Phase A + provisioning (L3)
PASS  Widevine licence HTTP 200
PASS  Widevine L3 playback (Media3/ExoPlayer, 1,958 ms, >60 s)
PASS  SSH/ADB/root after reboot
WARN  Tailscale not connected
```

---

# 21. Artifact locations

```
KM6_AUTONOMOUS_AUDIT_2026-10-25/
├── MISSION_STATE.md  INVENTORY.md  EVIDENCE_INDEX.md  ISSUES.md  CHANGES.md  FINAL_REPORT.md
├── docs/BOOTLOADER_DTB_ANALYSIS.md
├── docs/STARTUP_ASSETS.md
├── docs/WIDEVINE_STATUS.md
├── docs/LINUX_MULTIBOOT.md
├── docs/TERMUX_ANDROID.md
├── evidence/{live,bootloader,logo,dtb,drm}/
├── scripts/{aml_res_tool,uboot_env_tool,build_startup_assets,build_uboot_animation,
│             build_mainline_rescue,live_audit,deploy_logo_odm_ext,deploy_startup_animation}
├── artifacts/startup/{BMP,PNG,logo images,bootanimation.zip,module.zip,uboot-anim/}
├── artifacts/linux-rescue/{usb/,experiment-B-stock-kernel/}
└── work/{stock-vendor/,venv/,env-test.img}
```

---

# 22. Ordered deployment plan (owner-present)

| order | action | risk | rollback |
|---:|---|---|---|
| 1 | **Boot 0**: `experiment-C` RAM animation test via `reboot update` | **none (RAM only)** | power cycle |
| 2 | `deploy_logo_odm_ext.sh --approve`, reboot | very low | `--rollback` |
| 3 | `deploy_startup_animation.sh --variant A --approve`, reboot, calibrate `irkey` | medium (env) | `--rollback <backup>` |
| 4 | Copy `linux-rescue/usb/*` to FAT32, `reboot update` | low (RAM only) | power cycle |
| 5 | If needed, `experiment-B` RAM DTB/USB fix | low (RAM only) | power cycle |
| 6 | Write Devmfc image to ≥2 GB USB, boot, verify hardware | medium (USB only) | remove stick |
| 7 | Install `salamanka_bootanim_module.zip`, reboot | low | remove module |
| 8 | Decide DRM path (accept L3 / stock / vendor experiment) | high for stock/reflash | full backup |

**Do not** do the persistent steps (2–3) and an external-boot step (4–5) in the same session
without verifying the previous one; keep the ability to distinguish a boot-logo failure from a
boot-chain failure.

---

# 23. Bottom line

The project has moved from fragmented research to a **verified, reproducible engineering state**.
The true firmware, bootloader, DTB source, USB failure, Widevine regression, startup capabilities
and Linux path are now established with primary evidence.

The highest-value remaining work is **not more offline analysis** — it is five owner-present boots:
the RAM animation test, static logo, persistent animation calibration, mainline rescue, and the
RAM USB fix. Everything needed for those is prepared, hashed and reversible. Widevine L3
protected playback is already verified; only L1 requires a firmware decision.