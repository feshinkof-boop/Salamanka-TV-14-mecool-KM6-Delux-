# Recovery boundary

**There is no approved flashing guide for Salamanka TV 14.** The intent of the experiments has been to keep the box accessible while the modern kernel and Android userspace are still incomplete.

## Current verified protection

The latest local audit reports **12/12 verified backup sets**. The existing Android 11 installation remains bootable. Stages 54–56 investigated kernel/eMMC initialization without rewriting persistent bootloader, environment, GPT, eMMC or a separate Arch installation.

A verified backup file and a successful end-to-end restore are different tests. The public repository does not currently contain recovery images or raw evidence sufficient to promise an unbrick procedure.

## Why current tests use RAM/NBD

Temporary RAM boot and PC-hosted NBD images allow the Android 14 framework to run on the physical board while limiting writes to the known-good internal installation. The approach creates dependencies on the development PC and its network/storage serving path; it does not prove that native eMMC boot is ready.

## High-risk areas

The older audit found that the installed U-Boot's internal multi-DTB, not a previously modified external `_aml_dtb` store, determined the active DTB. That makes unverified DTB patches particularly easy to misunderstand.

Treat these as separately controlled operations: firmware update, bootloader/TEE provisioning, slot changes, AVB state, partitions, filesystem creation and relocking. Do not perform any of them based on assumptions from a different KM6 revision.

## Gate before an installation test

1. Verify the exact target board and current partition/slot layout.
2. Preserve and verify the necessary readbacks off-device.
3. Prove the proposed boot/recovery route on this board without destructive writes.
4. Confirm Linux can enumerate and read the internal eMMC reliably.
5. Record the exact image hashes, compatibility and rollback method.
6. Require an explicit, informed decision before any persistent writes.

Until then, use nonpersistent, reversible testing. The project's goal is a native ARM64 ROM **without destroying the currently recoverable unit**.

[Boot-chain analysis](../research/BOOTCHAIN.md) · [eMMC](EMMC.md) · [release checks](RELEASE-CRITERIA.md).
