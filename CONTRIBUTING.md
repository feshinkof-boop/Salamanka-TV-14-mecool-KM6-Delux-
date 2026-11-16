# Contributing

This is a work-in-progress AOSP port for one board: **KM6 Deluxe Rev. 1 / S905X4**. If you have patches or relevant board logs, they are welcome.

Before opening a hardware issue, include the board revision, kernel/Android version and how the device was booted (original Android 11, RAM, NBD or internal eMMC). Provide the exact failure and relevant sanitized logs, not just a screenshot of the problem.

Current areas where expertise would help: Linux MMC/eMMC command handling, Panfrost/DRM/KMS and Android HWUI, Amlogic video decoding, ASoC audio, the V01 Bluetooth microphone, AOSP SELinux and safe update/recovery.

Do not publish MAC addresses, serials, private network details, account IDs, firmware keys or private device backups. Do not copy vendor binaries into the repo without verifying redistribution rights.

Host-side unit tests are not device tests; describe which environment you actually used. Please avoid claims of a working ROM until a repeatable, standalone image is available.

[Project status](docs/STATUS.md) · [Roadmap](docs/ROADMAP.md).
