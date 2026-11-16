# Test records and reporting

The source of truth for physical-device evidence remains the maintainer's local development logs. This GitHub repository contains summaries but not the full local logs or AOSP working tree.

## Latest reported totals

| Measurement | Value | Interpretation |
| --- | ---: | --- |
| Completed local stage | 56 | Checkpoint number, not release percentage |
| Cumulative test suite | 450 PASS, 3 SKIP | Checks in the reported full suite; not 450 distinct KM6 boots |
| Engineering assessment | 230 PASS, 1 SKIP, 34 PARTIAL, 17 BLOCKED, 0 FAIL | Separate status matrix; it still contains blockers |
| Verified backup sets | 12/12 | Backup audit, **not** proof of every restore scenario |
| Binder services | 219 | Observed during Android framework bring-up |
| NBD-backed boot-complete | 101.70 s (Stage 52); 94.52 s (Stage 53) | Physical KM6, dependent on host storage |

There is no verified time log for the development work, so person-hours, expenses, compile-attempt totals and aggregate CPU/GPU hours are intentionally **not** estimated.

## Evidence classification

- **PHYSICAL:** command or observation from the actual KM6 Rev. 1; record device state and whether storage was local or network-backed.
- **HOST:** compilation, static image checks or scripts on the workstation; not hardware proof.
- **HISTORICAL:** old vendor/slimBOX experiments; may not describe the current system.
- **REPORTED:** result described in a local report whose raw logs have not been mirrored here.
- **NOT TESTED:** absence of sufficient evidence. This is not PASS.
- **PLANNED:** next experiment, not completed work.

## Minimum record for a reproducible claim

Include stage, timestamp, exact kernel/AOSP revision, target board, whether eMMC was used, boot transport, input artifacts' hashes, command/test, expected/observed output, failure log, recovery result and sanitized evidence location. Never post account names, serials, private IPs or DRM keys.

The Python checks in this public repository test only [the offline ROM inventory tool](../tools/rom_audit.py); they are not included here as proof that the Android firmware works.

[Status](STATUS.md) · [Bring-up](BRINGUP.md).
