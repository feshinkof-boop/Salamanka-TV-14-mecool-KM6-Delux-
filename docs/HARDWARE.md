# Target hardware and validation gaps

**Primary target:** MECOOL KM6 Deluxe Rev. 1, 4 GB RAM / 64 GB eMMC, Amlogic S905X4 (SC2/AH212), quad Cortex-A55 and Mali-G31 MP2. Different KM6 revisions may use different network and remote hardware. Do not apply a Rev. 2 test result to Rev. 1 without checking.

| Hardware area | Known board capability | Salamanka Android 14 evidence / outstanding work |
| --- | --- | --- |
| CPU | ARMv8-A / AArch64 | Native Android 14 userspace has executed on the board |
| GPU | Mali-G31 | Panfrost/Mesa and Composer3/SF activity reported; stable UI still blocked |
| HDMI | Digital video and audio | DRM/KMS at 1080p60; sound/CEC/HDR/AFR unverified |
| eMMC | 64 GB | Linux 6.18 enumeration stops at CMD3 |
| RAM | 4 GB | Framework and NBD-backed boot tests; production memory behavior not qualified |
| VPU | Hardware AVC/HEVC/AV1 capability | Android 14 hardware decode **not verified** |
| Audio | HDMI, optical SPDIF, analog | Android 14 drivers/HAL and passthrough **not verified** |
| Ethernet | Gigabit LAN | NBD transport used; general device/network functionality not qualified |
| Wi-Fi / BT | 2.4/5 GHz Wi-Fi and Bluetooth | Android 14 connection, recovery and V01 voice **not verified** |
| USB | USB host ports | Host/device roles and accessories require revision-specific validation |
| Remote | MECOOL original V01 | Voice microphone, HID mapping and standby still to be tested |
| microSD | Slot present | Not used or required for experimental bring-up or recovery |

## Media test requirements

Use repeatable 4K AVC, HEVC Main/Main10 and AV1 samples with actual MediaCodec decoder names, frame timings and dropped-frame statistics. Test HDMI and optical audio separately, including supported passthrough, pause/resume and lip sync. Run EDID/AFR/HDR and standby cycles only after basic video/audio work.

The original firmware's capabilities are a reference, not proof that the new kernel and Android HAL support them.

[Status](STATUS.md) · [4PDA observations](../research/4PDA-COMMUNITY.md).
