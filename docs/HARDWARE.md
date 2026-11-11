# KM6 Deluxe Rev 1 hardware & acceptance matrix

| Subsystem | Known hardware | Stock reference | Salamanka release acceptance |
|---|---|---|---|
| SoC | Amlogic S905X4 / SC2 / AH212 | Quad Cortex-A55 | Functional ARM64 boot and stability |
| GPU | Mali-G31 MP2 | Hardware graphics | DRM/KMS, Panfrost/appropriate driver, accelerated UI and proper Android composition |
| DRAM | 4 GB DDR4 | Existing platform | Memory pressure, suspend and multitasking validation |
| Storage | 64 GB eMMC; A/B dynamic partitions on audited slimBOX | Userdata, system partitions | Reliable storage, safe update and verified rollback |
| Ethernet | 1 Gbit | Working in some configurations | Negotiates gigabit and survives repeated networking / sleep tests |
| WLAN | 2.4/5 GHz; 802.11ax-capable | Driver and board revision vary | Verified WLAN firmware and power recovery |
| Bluetooth | 5.0 | Native remote support | Reliable original V01 HID + microphone and third-party remotes |
| HDMI | Digital display and audio | 4K/HDR/AFR problems reported | EDID, mode switching, HDMI-CEC, stable AV sync |
| Hardware video | S905X4 includes AV1 and HEVC decoder blocks | Codec support | Hardware AVC/HEVC/AV1 and real 4K decode not merely software playback |
| SPDIF | Optical | Stock feature; some port regressions | PCM and supported passthrough receiver tests |
| Analog audio | 3.5 mm | Stock feature | Audio routing and playback without dropouts |
| USB | USB2 + USB3 | Host works; USB gadget ADB failed in Oct audit | Host disks/input and separate USB device-mode diagnosis |
| SD slot | Removable media | Present | Mount/read/write test |
| Remote | MECOOL V01 original | Voice generally available on stock | Voice search and input stable across boot/standby |

**Do not merge KM6 Classic, KM6 Deluxe Rev 1 and later HDMI-marked Rev 2 results.** Hardware revisions may differ in LAN/BT/WLAN wiring. The 'HDMI' chassis marking is a community shorthand, not a substitute for board/SKU, DTB and peripheral identification.

## Test media

- 2160p H.264, HEVC Main/Main10, AV1, VP9 (as available); test supported profiles only.
- SDR/HDR10 and 23.976/24/25/50/59.94/60fps content.
- Lossless PCM stereo, AC3 5.1 optical/receiver path, HDMI multichannel where hardware supports.
- Repeat 2h seek/pause/resume, 24h soak and 72h soak with activity logs.
- Compare MediaCodec to software decode; log actual decoder names and dropped frames.

## Root cause discipline

A disappearing picture or repeated reboot can be a power adapter, eMMC, cable, heat or firmware fault. Validate non-invasive hypotheses and basic configuration first. Do not claim software fixes untested hardware faults.