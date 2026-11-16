# Open technical problems

This file is a short map to the current issues. The [GitHub issue tracker](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues) is the place to attach logs and patches.

| Problem | Evidence | Tracker |
| --- | --- | --- |
| Linux 6.18 eMMC stops at CMD3 | CMD0–CMD2 complete at 400 kHz, CMD3 times out; `0xa1ff2800` status | [#12](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues/12) |
| HWUI / Leanback abort | Android boot-complete over NBD, `CanvasContext::setupPipelineSurface` abort | [#1](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues/1) |
| Safe persistent Android install | RAM/NBD path works; internal storage and recovery not complete | [#13](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues/13), [#7](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues/7) |
| Actual project source in public Git | Device/kernel/HAL changes are local to the workstation | [#3](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues/3) |
| VPU/media, audio, V01 voice | Not validated on Android 14 | [#4](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues/4) · [#6](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues/6) · [#5](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues/5) |
| Vendor component trust | XCPE research; exact hardware infection not proven | [#2](https://github.com/feshinkof-boop/Salamanka-TV-14-mecool-KM6-Delux-/issues/2) |

[Current state](../docs/STATUS.md) · [Roadmap](../docs/ROADMAP.md).
