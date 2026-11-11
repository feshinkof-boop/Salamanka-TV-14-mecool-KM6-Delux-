# Prioritized engineering roadmap

A project requirement is not a confirmed shipped feature. Every task is tracked as BUILT, HOST-PASS, DEVICE-PASS, BLOCKED or UNKNOWN.

## P0 — release blockers

| ID | Required outcome | Verification |
|---|---|---|
| P0-01 | Inventory/Audit stock, slimBOX and imported binary dependencies for XCPE, suspicious services and network access | SBOM + hashes + partitions + offline IOC results |
| P0-02 | Real ARM64-only Android 14 boot | Device properties, running service architecture, screenshot + dmesg |
| P0-03 | Recoverable image strategy and boot chain | Offline proofs, separate owner-approved recovery tests |
| P0-04 | Identify FCM 202404 vs Android 14 FCM 8 configuration issue; resolve manifest/HAL compatibility and verify working composition | VINTF check passes and compositor runs on hardware |
| P0-05 | Real accelerated playback H264/HEVC/AV1 | Decoder identity, CPU and frame-drop data on 4K samples |
| P0-06 | HDMI, SPDIF, analog audio | Device/receiver tests, pause/resume, audio sync |
| P0-07 | V01 remote microphone + navigation | HID/mic input through supported speech service |
| P0-08 | 1GbE, Wi-Fi, Bluetooth | Reconnect, sleep, link, throughput and stability |
| P0-09 | SELinux enforcing + minimal privilege | `getenforce`, policy audit, no broad permissive grants |
| P0-10 | No unexpected reboot, freeze or blocked playback | Reproducible soak logs |

## P1 — quality

- P1-01 display: HDR10/SDR, AFR matching, EDID, HDMI-CEC.
- P1-02 Bluetooth: key debounce, repeat, pairing, reconnect, wake and accidental wakes.
- P1-03 storage: eMMC and removable USB/SD health, filesystem and large-file handling.
- P1-04 power: sleep/network standby/deep standby semantics, fast wake.
- P1-05 security updates: signed OTA/AVB on supported hardware, rollback tested.
- P1-06 media stability: suspend/resume, app transitions, audio/video sync and problematic formats.
- P1-07 privacy: permission-safe voice search, no hidden telemetry.

## P2 — distinctive features

- Salamanka Media Engine: content display matching, HDR/saturation options, playback diagnostics.
- Salamanka Remote Manager: mapping, event trace, original/newer remote profiles.
- Salamanka Power Manager: explicit states, CEC and wake controls.
- Salamanka Performance Manager: 4 GB RAM tuning, storage and thermal metrics.
- Salamanka Network Suite: optional SSH/SFTP, SMB/NFS, VPN, local servers, **off by default**.
- TV-oriented split screen/PiP, launcher and background-service support.
- Branded boot logo/animation only after boot safety established.

## Rules

No P2 completion can compensate for a P0 failure. Do not claim device-level PASS from unit tests. Never replace a working feature with an attractive but unverified port.