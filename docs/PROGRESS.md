# Work behind the current build

The project has reached **Stage 56** in the local development record, as of 16 November 2026. That number is a checkpoint sequence, not a release count or a percentage-complete figure.

| Period | Work done | Why it mattered |
| --- | --- | --- |
| October | Audited existing firmware, U-Boot, embedded DTBs, A/B layout and USB gadget behavior. Preserved recovery data. | Corrected wrong assumptions about the boot chain before experimenting. |
| Early November | Built native ARM64 AOSP Android 14 products and Linux 6.18.55; iterated on Soong, SELinux labels, VINTF and graphics. | Produced a testable system, not just a launcher modification. |
| Mid-November | Ran physical ARM64 Linux and Android `init`, progressed through Zygote/system_server, GPU and HDMI composition. | Moved from cross-compilation to actual hardware execution. |
| Stages 52–53 | Android reached natural `sys.boot_completed=1` over temporary NBD; SystemUI/Leanback started. | Confirmed much of the Android framework starts on KM6. |
| Stages 54–56 | Verified 12 backup sets, isolated Linux MMC failure at CMD3. | Turned a storage failure into a specific reproducible protocol boundary without overwriting the working installation. |

## Test totals in context

The latest local engineering report records **450 passes and 3 skips** in a cumulative test suite. A separate status matrix records **230 PASS / 1 SKIP / 34 PARTIAL / 17 BLOCKED / 0 FAIL**. These are not additive, and the first figure does not represent 450 separate device tests. The 17 blockers mean substantial work remains.

There is no reliable timesheet or CPU-hour ledger in this repository, so those numbers are not invented. The work is better demonstrated by the sequence of solved and unresolved hardware problems documented in [the bring-up log](BRINGUP.md).

The original logs, source history and build artifacts are still on the maintainer's workstation, not in this public documentation checkout.

[Status](STATUS.md) · [Bring-up](BRINGUP.md) · [Testing](TESTING.md).
