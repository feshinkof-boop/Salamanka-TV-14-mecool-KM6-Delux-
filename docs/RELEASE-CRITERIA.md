# Release gate specification

## Validation classes

`DEVICE-PASS`: repeated test on target hardware with logs and configuration details.
`HOST-PASS`: offline/static/host-side test with exact hashes and commands.
`BUILT`: compilation only.
`FAIL`: reproduced issue with evidence.
`BLOCKED`: unmet dependency.
`UNKNOWN`: no adequate evidence.

## Gates

| Gate | Requirements | State |
|---|---|---|
| A — architectural | 64-bit-only userspace verified on running Android, valid target FCM VINTF and functioning Composer implementation | BLOCKED / not device-tested |
| B — boot and recovery | Cold boot, slot B, recovery path, no lost device credentials/provisioning | UNKNOWN |
| C — video | Panfrost/graphics + Codec2/MediaCodec HW AVC/HEVC/AV1 4K, SDR/HDR | UNKNOWN |
| D — audio | HDMI, SPDIF, analog, SPDIF surround compatible formats, lip sync | UNKNOWN |
| E — network / remote | Gigabit LAN, 2.4/5 GHz Wi-Fi, original V01 mic + pairing/wake | UNKNOWN |
| F — stability | 24-hour and 72-hour concurrent media/network/remote tests | UNKNOWN |
| G — security | full SBOM, no XCPE or unknown privileged agents, SELinux enforcing, approved OTA | UNKNOWN |
| H — distribution | Full-source/third-party licenses and verifiable build/recovery instructions | UNKNOWN |

## Required release evidence

- Device revision and source revision IDs, build fingerprint, kernel, partition table and images' hashes.
- Test logs with start/end timestamps, actual hardware, expected/observed behavior and pass/fail.
- Network packet capture during clean boot, idle, media playback, setup, update and after reset (sanitized).
- Verified non-reappearance of prohibited packages after factory reset.
- Validated recovery from *the actual target board*, not a nearby S905X4 model.
- License declaration, known limitations and security disclosure instructions.

**No prebuilt images are released in this repository yet.**