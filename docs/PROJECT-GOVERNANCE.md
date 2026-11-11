# Project governance

This is **independent, experimental firmware development** for KM6 Deluxe Rev1, not an official MECOOL, AOSP, Google or slimBOX release.

## Language for evidence

- **DEVICE-PASS:** procedure ran on the real board, with logs and repeatable observations.
- **HOST-PASS:** source/image or utility tested on a workstation only.
- **BUILT:** compilation produced named images, no proof of runtime.
- **COMMUNITY REPORT:** a 4PDA owner described it; not independently verified.
- **HYPOTHESIS:** plausible risk requiring experiments.
- **UNKNOWN:** no adequate evidence.

Do not convert one classification to another without new artifacts.

## Design constraints

A genuine **ARM64-only Android 14 userspace** is mandatory. The project must not claim a working 4K hardware decoder, audio or remote from compilation alone. Avoid unrecoverable bricks: never perform device writes in CI; invasive testing requires independent owner approval and a verified rescue path.

## Publication rights

**The owner has not selected a blanket public license.** Earlier publication of a CC BY 4.0 documentation license was premature and has been withdrawn for subsequent distribution. Original authors retain rights unless otherwise licensed. When real code is imported, retain upstream AOSP/Linux licenses and review proprietary blob redistribution permissions. Never commit Widevine/TEE material, per-device identifiers, private SSH credentials, network addresses, proprietary firmware dumps or private signing keys.

## Practical repository scope

This GitHub repository currently includes project documents, historical sanitized research and host-side tools. The complete Kubuntu checkout and firmware build images are not available here; they must be imported from verified local sources rather than reconstructed by guessing.
