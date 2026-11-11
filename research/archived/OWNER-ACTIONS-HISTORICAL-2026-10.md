> [!CAUTION]
> HISTORICAL ARCHIVE: not current instructions and NOT a verified recovery procedure. Original local file was sanitized for public display. No bootloader, env, DTB, TEE or firmware write should be performed from this text without independent verification and explicit approval. Private IPs/device serials have been redacted.

# OWNER ACTION SHEET — four reversible boots

Everything is prepared under `/home/salamanka/km6-lab/KM6_AUTONOMOUS_AUDIT_2026-10-25`.
No bootloader/env/logo write has been made. Do these in order; stop and report if one fails.

---

## Boot 0 (safest) — animation RAM test, no writes (10 min)

Use `artifacts/startup/uboot-anim/experiment-C/`:
copy `aml_autoscript` + `SALF0.BMP` … `SALF7.BMP` to a FAT32 USB root, insert, then
`adb -s [TARGET] shell reboot update`.
U-Boot shows the 8 frames and then `run storeboot` (normal Android). This calibrates the
`irkey` timing and proves `bmp scale` at 960×540 **without any persistent change**.
If the frames flash, multiply the `irkey` values by 1000; if too slow, divide by 1000.

## Boot 1 — static SALAMANKA boot logo (5 min)

```bash
cd ~/km6-lab/KM6_AUTONOMOUS_AUDIT_2026-10-25
./scripts/deploy_logo_odm_ext.sh --check
./scripts/deploy_logo_odm_ext.sh --approve
adb -s [TARGET] reboot
```

Expected: black/green SALAMANKA logo before Android. If it is missing, the fallback SlimBOX
logo is still shown; roll back with `--rollback`.

**This alone achieves the earliest-stage SALAMANKA branding.**

---

## Boot 2 — pre-Android animation (10 min + calibration)

```bash
./scripts/deploy_startup_animation.sh --variant A --check
./scripts/deploy_startup_animation.sh --variant A --approve
adb -s [TARGET] reboot
```

**Power stability matters:** this writes the 8 MiB `env` partition. Do not interrupt power
during the `--approve` step; the live env is backed up first and the script verifies the read-back.

Expected: ~1.2 s of 8 Matrix frames after the HDMI/OSD init, ending on the SALAMANKA logo.

Calibration:
* Too fast (likely if the timer is divided): multiply the `irkey` values by 1000.
* Too slow: divide by 1000.
* Edit `salamanka_anim` with `python3 scripts/uboot_env_tool.py …` and re-deploy, or adjust the
  reference env image before running the deploy.

Rollback: `./scripts/deploy_startup_animation.sh --variant A --rollback <timestamp-dir>`.

---

## Boot 3 — mainline Linux rescue (15 min)

1. Prepare a FAT32 USB stick; copy the **contents** of
   `artifacts/linux-rescue/usb/` to its root:
   `SALKERN.IMG`, `SALDTB.DTB`, `SALINIT.GZ`, `aml_autoscript`, `README.txt`.
2. Make sure the stick has **no** `recovery.img` or `dtb.img`.
3. Insert it into a USB-A port of the KM6.
4. Run:

```bash
adb -s [TARGET] shell reboot update
```

Expected: U-Boot `update` → USB → `aml_autoscript` → 6.18.55 kernel. HDMI shows the SALAMANKA
banner and kernel log; Ethernet DHCP IP is printed. The initramfs mounts **no storage**.
5. Leave with `reboot -f` (or power-cycle). Android returns.

If HDMI is black, the kernel did not reach fbcon. Try the serial console (ttyS0 921600) or
experiment B.

---

## Boot 4 — RAM-only USB fix test (15 min)

```bash
# FAT32 USB root: aml_autoscript + SALRESCUE.IMG from
# artifacts/linux-rescue/experiment-B-stock-kernel/
adb -s [TARGET] shell reboot update
```

Expected (if the hypothesis is right): a new USB network interface on the host; configure
`[PRIVATE-LAN-ADDRESS]/24` and `telnet [PRIVATE-LAN-ADDRESS]`. This boots the stock kernel with a **RAM-only**
`controller-type=1` DTB change; no partition is written.
If nothing appears, the DTB property alone is insufficient; report and revert to the env/DTB plan.

---

## Later — Android animation & Debian

```bash
adb push artifacts/startup/salamanka_bootanim_module.zip /sdcard/
adb shell su -c 'magisk --install-module /sdcard/salamanka_bootanim_module.zip'
adb reboot
# rollback: adb shell su -c 'rm -rf /data/adb/modules/salamanka_bootanim'
```

Debian PRoot (inside Termux):
`bash scripts/install_termux_debian.sh --check` then `--approve`.

---

## If something goes wrong

* **Android still boots, no logo/animation**: restore the env/logo backup with the rollback
  command printed by the deploy script; network ADB/SSH are independent.
* **No network ADB**: connect USB (if the USB fix is not applied, USB ADB is unavailable);
  the recovery path is the ADNL/USB update mode used for the original flash (documented in
  `docs/BOOTLOADER_DTB_ANALYSIS.md`).
* **Do not** flash `env`, `logo`, `bootloader`, `_aml_dtb`, `vbmeta*` or `tee` with anything other
  than the backed-up images.