> [!CAUTION]
> HISTORICAL ARCHIVE: not current instructions and NOT a verified recovery procedure. Original local file was sanitized for public display. No bootloader, env, DTB, TEE or firmware write should be performed from this text without independent verification and explicit approval. Private IPs/device serials have been redacted.

# KM6 bootloader, U-Boot environment and DTB analysis

**Scope:** installed SlimBOXtv ATV 11.46 boot chain, verified 2026-10-25/26 from live readbacks
and offline binary analysis. **No bootloader, env, DTB or AVB write was performed.**

All paths below are relative to `/home/salamanka/km6-lab/` unless absolute.

---

## 1. Verified component identity

| component | evidence | sha256 / identity |
|---|---|---|
| Active bootloader (eMMC boot0 **and** boot1) | live readback `KM6_AUTONOMOUS_AUDIT_2026-10-25/evidence/bootloader/…`, `reports/slimbox-usbadb-fix/bootloader0/1.READBACK.bin` | `73a2cd00…` (md5) — first 0x319000 bytes are **byte-identical** to SlimBOX 11.46 `bootloader.PARTITION`, sha256 `a4bc877b…` |
| GPT `bootloader` partition (4 MiB) | live readback `evidence/bootloader/bootloader-gpt-20261025.img` | sha256 `890de78c…`; **different format**: `06 00 00 00 … ef be ad de`, contains `@ML` sections and `DBLK_PAYLOAD_END` markers. (The FDT-like bytes at 0x231a81 are inside a compressed stream, not a valid DTB.) This is a DBLK-marked dual-bootloader store (inferred from the `DBLK_PAYLOAD_END` markers), not the running boot code. Preserved for recovery. |
| U-Boot BL33 | decompressed from the `LZ4C` section at file offset `0x198010`, payload at `0x198090`; uncompressed size `0x14eb38` | `U-Boot 2019.01-g42a9be9793 (Dec 15 2022 - 19:41:37 +0000)`; sha256 `15d7b9ae…` |
| U-Boot control FDT | embedded at decompressed offset `0x10d6c0`, `totalsize=0x8104` | model `Amlogic Meson SC2 S905X4 AH212 Board`; sha256 `bb045b16…` |
| Environment | `env` partition, 8 MiB, two CRC-valid 64 KiB objects at 0 and 0x10000 | sha256 `fe44692e…` |
| Active kernel FDT | `/sys/firmware/fdt` (live), 77,952 B | sha256 `5e58a04e…` |

### Original (pre-SlimBOX) bootloader — recovered identity

`~/KM6-Startup/bootloader-analysis/bootloader-original.bin` (4,194,304 B) starts with **512 zero
bytes**, then an `@ML` container at offset 512. After stripping the prefix
(`evidence/bootloader/bootloader-original-2021.shifted.bin`, sha256 `ee308274…`) it contains
**U-Boot `2019.01-g5f543bb605-dirty` (Jan 27 2021)**. This is the device's original 2021
bootloader, **different** from the stock firmware image's `bootloader.PARTITION`
(`2019.01` 2020 build, sha256 `db8ac354…`) and from the current SlimBOX 2022 build
(`2019.01-g42a9be9793`). It is a valid rollback candidate for the 2021 era, but rolling back
requires matching the rest of the 2021 system; do not write it in isolation.

The flash log (`reports/slimbox-flash-resume-20261020.log`) shows the vendor tool wrote
`oem mwrite 0x319000 normal store bootloader` and verified sha1 `65a63bba…`, which is the sha1 of
the SlimBOX `bootloader.PARTITION`. The live boot0/1 readback matches it. The GPT `bootloader`
partition was **not** replaced by that write and still carries the DBLK structure.

### Decompression method (reproducible)

The installed U-Boot is not a raw FIP: at file offset `0x198010` there is an Amlogic `LZ4C`
header:

```
0x198010: 4c 5a 34 43   ("LZ4C")
0x198014: 00 00 80 00   (8 MiB buffer)
0x198018: 38 eb 14 00   (uncompressed size 0x14eb38)
0x19801c: 0e e4 0a 00   (compressed size 0x0ae40e)
0x198040: "2022121519:41:45"
0x198090: start of the LZ4 block
```

`lz4.block.decompress(data[0x198090:0x198090+0xae40e], uncompressed_size=0x14eb38)` yields the
1,370,936-byte U-Boot image. This is the method used to enumerate commands and disassemble
`irkey`.

---

## 2. Verified U-Boot environment (full boot logic)

The environment is stored in two 64 KiB objects, both with valid CRC32 over the whole 64 KiB block
after the CRC field. They are **not identical**:

| variable | block 0 | block 1 |
|---|---|---|
| size | 130 vars | 125 vars |
| `stdin/stdout/stderr/fdtcontroladdr` | present | absent |
| `reboot_mode` | `cold_boot` | `watchdog_reboot` |
| `bootargs` | current: `hdmitx=,444,10bit`, `hdmichecksum=0x531e0000`, `firstboot=0` | older: `8bit`, checksum `0`, `firstboot=1` |
| `preboot` / `common_dtb_load` / `boot_part` / `aml_dt` | identical | identical |

**Block 0 is the current environment** (its `bootargs` match `/proc/cmdline`). The tool
`scripts/uboot_env_tool.py` treats the block with the most variables as the base and, by default,
writes the merged result to **every** valid block, so the result does not depend on which one
U-Boot imports.

### Boot flow (verbatim, installed env)

```
preboot = run bcb_cmd; run upgrade_check; run init_display; run storeargs;
          run upgrade_key; bcb uboot-command; run switch_bootmode;

init_display = get_rebootmode; ... osd open; osd clear; run load_bmp_logo;
               bmp scale; vout output ${outputmode}; dovi set; dovi pkg; vpp hdrpkt;

load_bmp_logo = if rdext4pic ${board_logo_part} $loadaddr; then
                    bmp display $logoLoadAddr;
                else if imgread pic logo bootup $loadaddr; then
                    bmp display $bootup_offset;
                fi; fi;

storeboot = run get_os_type; run storage_param;
  if os_type = kernel:
    get_system_as_root_mode; get_valid_slot; get_avb_mode;
    if fdt addr ${dtb_mem_addr}; then else echo retry common dtb; run common_dtb_load; fi;
    setenv loadaddr ${loadaddr_kernel};
    if imgread kernel ${boot_part} ${loadaddr}; then bootm ${loadaddr}; fi
```

Key variables: `boot_part=boot_a`, `dtb_mem_addr=0x1000000`,
`common_dtb_load=imgread dtb boot_a 0x1000000`, `aml_dt=sc2_s905x4_ah212-4g`,
`board_logo_part=odm_ext`, `bootLogoPart=odm_ext_a`, `ext4LogoPath=/logo_files/bootup.bmp`,
`logoPart=f`, `bootup_offset=0x24e30`, `bootup_size=0x3f4848`, `usb_burning=adnl 1200`,
`bootcmd=run storeboot`.

`preboot` is executed by U-Boot's normal main loop on every boot. This is the only hook available
before Android without changing the bootloader.

The **original 2021 environment** is preserved as `evidence/bootloader/env-original-2021.img`
(2 CRC-valid blocks, 103 variables). It uses `EnableSelinux=enforce`,
`androidboot.selinux=enforce`, `common_dtb_load=imgread dtb _aml_dtb ${dtb_mem_addr}`, and an
`init_display` that reads `imgread pic logo bootup` directly (no `rdext4pic`). This is the stock
(pre-SlimBOX) behaviour and a rollback reference; do not mix it with the 2022 env.

---

## 3. Where the kernel DTB actually comes from (verified)

### 3.1 Live DTB vs the `_aml_dtb` store

The flashed `_aml_dtb` payload is a 4-table Amlogic `AML_` container (305,152 B after gunzip).
Tables start at `0x800`, `0x13000`, `0x25800`, `0x38000`; table 2 (`0x25800`) is
`amlogic-dt-id = "sc2_s905x4_ah212-4g"`, `controller-type = <0x03>`.

The live `/sys/firmware/fdt` (77,952 B) differs from table 2 only by U-Boot/kernel edits:
`serial-number`, `chosen` (bootargs/initrd), the two `dummy-charger`/`dummy-battery` overlay nodes
(proving `dtbo_a` was applied), two memory `reg` adjustments, and `memreserve` entries. It is the
same build as table 2, not a different DTB.

On 2026-10-20/21 the `_aml_dtb` store was written with a patched copy
(`controller-type 0x03 → 0x01`), verified by vendor `oem verify sha1sum` and an independent
`oem mread` read-back. After a reboot the live DTB still reads `controller-type = 0x03`
(`evidence/live/devicetree_dwc2.txt`, `evidence/dtb/live-20261025.fdt`).

**Conclusion:** the `_aml_dtb` store is **not** the kernel DTB source on this bootloader.

### 3.2 Why `common_dtb_load` never runs

`storeboot` calls `fdt addr 0x1000000` **before** `common_dtb_load`. BL33 board-init code has
already placed its own DTB at `dtb_mem_addr` (0x1000000), so `fdt addr` succeeds and the
`imgread dtb boot_a 0x1000000` branch is skipped. The U-Boot control FDT (embedded at 0x10d6c0)
itself contains the board compatible/model, and the runtime copy is at `fdtcontroladdr=f07776c0`.
The bootloader's internal DTB is therefore the effective kernel DTB.

The internal DTB is not a raw `d0 0d fe ed` blob at a known offset in the 4 MiB bootloader image.
The apparent FDT magic at file offset `0x231a81` is **inside the LZ4C compressed stream** (which
spans `0x198090..0x24649e`); it is a literal run in the compressed data, not a valid DTB (its
header offsets are nonsensical). The only real FDT extracted is U-Boot's control FDT at
decompressed `0x10d6c0`. The kernel DTB is therefore carried in an Amlogic container/compressed
component that has not been decoded; the **behaviour** is proven by the inert store write and the
live DTB.

### 3.3 What this means for changes

Persistent DTB changes require one of:

1. **U-Boot env `preboot`** that loads a DTB/overlay to `dtb_mem_addr` *after* board init and
   *before* `storeboot`'s `fdt addr` gate; or
2. a change to the bootloader's internal DTB (bootloader-class write; **not authorized**); or
3. a change to `dtbo_a` only (the overlay is applied to the base DTB; it can add/override nodes
   but AVB covers dtbo — `vbmeta` chain must be considered); or
4. a **RAM-only** DTB change from an external `aml_autoscript` before `bootm` (no persistence).

The previously prepared `_aml_dtb` patch remains a valid **offline artifact** but has no runtime
effect on this bootloader.

---

## 4. U-Boot capabilities (installed 2022 build)

The decompressed U-Boot was scanned and its command table located. Confirmed present:

`bmp`, `imgread`, `rdext4pic`, `osd`, `vout`, `vout2`, `hdmitx`, `dovi`, `vpp`, `ext4load`,
`fatload`, `bootm`, `booti`, `source`, **`autoscr`**, `sysboot`, `pxe`, `fdt`, `setenv`, `saveenv`,
`env`, `run`, `irkey`, `adnl`, `bcb`, `keyman`, `mmc`, `usb`, `store`, `gpio`, `saradc`,
`factory_provision`, `get_rebootmode`, `get_valid_slot`, `get_avb_mode`, `os_ident`, `imgread`,
`unpackimg`, `lzmadec`, `sha2`, `crc32`, `md`, `mw`, `fatwrite`, `watchdog`, `systemoff`.

**Not present:** `sleep`, `usleep`, `mdelay`, `udelay`, `bootmenu`, `menu` (the `menu` strings are
PXELINUX config keys, not a U-Boot bootmenu), `gettime`.

### `autoscr` correction

Two prior reports disagree. `SALAMANKA_DEEP_AUDIT` reports 05/08 claimed `autoscr` is absent from
the installed command table; `KM6_EXTERNAL_BOOT_CORRECTED_DIAGNOSIS.md` corrected that. This
session independently verified the **installed 2022 SlimBOX build** contains the `autoscr`
command name, help text (`DEPRECATED - use "source" command instead`, `argv: autoscr
script_mem_addr`) and the default-env macro `recovery_from_fat_dev=… autoscr ${loadaddr}`.

**Verdict:** `autoscr` is **present** in the current bootloader. The earlier "absent" conclusion is
**contradicted** for this build (it may have been true of the 2021/2024 OEM images analysed at the
time). This reopens the external-script boot route, subject to the `update`/BCB path below.

### `irkey` — a real timer primitive (new finding)

The command `irkey <timeout> <key1> … <keyN>` exists (`maxargs=12`, handler file offset `0x1f058`).
Disassembly (Capstone, AArch64) shows:

* `timeout` is parsed with `simple_strtoul` (base 0).
* elapsed time is obtained by calling the function at `0x4034`, which is a single
  `ldr w0, [0xfe0100ec]` (Amlogic AO timer register), then compared unsigned against the timeout.
* if the IR device is found, it polls a key with a driver call; on a match it sets the environment
  variable **`irkey_value`** and returns 0. On timeout it returns `-22` (-EINVAL).
* If the IR device lookup fails, it prints `failed to get ir udevice` and returns immediately
  (no delay).

U-Boot's control FDT at 0x10d6c0 contains a `meson-ir` node with
`compatible = "amlogic, meson-ir"`, `reg = <0x0 0xfe084040 0x44 0x0 0xfe084000 0x20>`,
`protocol = <1>`, `status = "okay"`. The IR device is therefore present for U-Boot.

**Implications**

* `irkey <n> 0xffffffff` is a timer-based wait of `n` units even when no key is pressed.
* It enables a **genuine timed multi-frame pre-Android animation** driven by a U-Boot script.
* It enables an **IR-remote-driven boot selection** (`if irkey …; then` + `irkey_value`), for a
  future boot menu, subject to key-code mapping and UX work.
* The unit of `n` is the `0xfe0100ec` timer. The register is the same one used by the sibling
  delay function at `0x4048`; call sites pass microsecond-scale constants (e.g. `0x2710` = 10 ms
  at `0x3fb8`), so the timer is **1 MHz and `irkey` timeouts are microseconds**. A visual
  calibration boot is still recommended. The generated animation uses `150000`/`120000` µs per
  frame and a documented calibration step.

This is the key technical result that turns "static logo only" into "timed sequence possible".

---

## 5. USB device mode (why USB ADB is dead)

Live state:
* `/sys/class/udc/fdd00000.dwc2_a/state = not attached`;
* no Amlogic USB device on the host (`lsusb` has only the host's built-in devices);
* live DTB `dwc2_a@fdd00000`: `controller-type = <0x03>` (USB_OTG), `phy-interface = <0x02>`,
  `status = "okay"`; `usb3phy@fe03a080 otg = <0x00>`;
* previous analysis: with `controller-type=USB_OTG` + `phy-interface=2` and no `phy-otg`, the
  vendor `aml_new_usb_v2_init()` reads the shared PHY ID and forces **host** mode; the gadget core
  never sees a B-session.

Changing the **stored** `_aml_dtb` table 2 does not change the live DTB (see §3). The RAM-only
paths are:

1. **U-Boot `preboot` script** that loads a patched DTB to `dtb_mem_addr` before `storeboot`
   (env write; prepared, not executed).
2. **External `aml_autoscript`** (via `reboot update`) that runs `fdt addr ${dtb_mem_addr}`,
   `fdt set /soc/dwc2_a@fdd00000 controller-type <0x1>`, then boots the rescue image. This is a
   **RAM-only** test and is packaged as `artifacts/linux-rescue/experiment-B-stock-kernel/`.
3. Bootloader-internal DTB modification (forbidden unattended).
4. `dtbo_a` overlay: current dtbo only carries dummy charger/battery nodes; it is applied, so an
   overlay could override `controller-type` if the base node is in the base DTB and the overlay
   targets it. AVB/dtbo hash implications must be handled; not prepared.

The host side sees no USB enumeration because the PHY is in host mode; this is consistent with
`otg_device=1` in the kernel cmdline (forces the gadget core peripheral) fighting the PHY.

---

## 6. Boot logo path (verified)

`load_bmp_logo` first calls `rdext4pic ${board_logo_part} $loadaddr`. The help text is
`rdext4pic <partName> <memAddr> <logoPath>`; with two arguments it defaults to
`ext4LogoPath=/logo_files/bootup.bmp` and `logoPart=f` (partition 15 = `odm_ext_a`, 16 MiB).
On success it runs `bmp display $logoLoadAddr` (`0x20000`).

Live `odm_ext_a:/logo_files/` contains only `upgrade_*.bmp`; **there is no `bootup.bmp`**, so the
primary path fails and U-Boot falls back to `imgread pic logo bootup $loadaddr` +
`bmp display $bootup_offset` (0x24e30). The live logo partition is the SlimBOX AML_RES v2
container (logical 920,800 B; CRC valid; 8 resources; `bootup` = gzip 19,439 B → 1920×1080
16bpp BMP).

This means the **lowest-risk branding path** is to place a 1920×1080 16bpp BMP at
`odm_ext_a:/logo_files/bootup.bmp`; no logo-partition or bootloader write is needed. The static
asset and a guarded deployment script are in `artifacts/startup/` and `scripts/`.