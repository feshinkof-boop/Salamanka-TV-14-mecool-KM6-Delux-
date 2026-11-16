# eMMC: failure at CMD3

**Status: blocked — Stage 56, 16 November 2026.**  
Target: internal eMMC on KM6 Deluxe Rev. 1 under Linux 6.18.55.

The device's original Android 11 installation can still use the internal storage. The problem described here concerns enumeration with the new kernel. It is **not evidence that the eMMC hardware has failed**.

## Observed progression

An initial modern-kernel MMC path returned `-EINVAL`. A corrected diagnostic DTB allowed the driver to advance into the card's identification sequence.

Stage 55 showed initial commands completing at 400 kHz. Stage 56 located the next failure:

| Command | Purpose | Reported outcome |
| --- | --- | --- |
| CMD0 | GO_IDLE_STATE | Completed |
| CMD1 | SEND_OP_COND | Completed |
| CMD2 | ALL_SEND_CID | Completed |
| CMD3 | SET_RELATIVE_ADDR | **Response timeout** |

Reported command argument: `0x00010000` (RCA 1).  
Reported controller status: `SD_EMMC_STATUS=0xa1ff2800`.

The Linux driver does not enumerate the eMMC as a block device; therefore the Android 14 test build cannot use local `super` or data partitions through this kernel path. Host-backed NBD is a test workaround, not a solution.

## What is still unknown

The evidence does not yet distinguish among response sampling/timing, controller configuration, clock/reset state, pinctrl or device-tree differences, the card's state after CMD2, or a kernel-driver interpretation issue. A timeout alone does not justify changing card contents, GPT, boot0/boot1 or eMMC firmware.

## Next diagnostic (planned, not completed)

Capture and compare the **read-only** register and command state around successful CMD2 and failing CMD3: `SD_EMMC_CFG`, command configuration/argument, relevant response registers, clock state, interrupt status and controller state. Check actual register definitions against the running driver and SoC documentation before interpreting bit fields.

The test must leave all persistent partitions untouched, preserve the known-good Android 11 recovery route and stop on unexpected device behavior. A solution requires repeatable enumeration and read verification on the exact board, followed by separately approved write/recovery testing.

## Acceptance

- eMMC enumerates consistently under the selected Linux kernel, without relying on the host PC.
- Existing partition map can be read without modification.
- Recovery path remains intact and is demonstrated independently.
- Persistent installation is only considered **after** those conditions have been met.

[Bring-up sequence](BRINGUP.md) · [Recovery](RECOVERY.md).
