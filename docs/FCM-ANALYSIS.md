# Android 14 FCM and Composer notes

An earlier build report referenced **FCM `202404`** alongside a HIDL Composer 2.4 declaration and a `checkvintf` failure. That has been incorrectly described in older discussion as an Android 14 requirement.

Android **14 corresponds to FCM level 8**. `202404` is the Android 15-era level. See [Android FCM lifecycle](https://source.android.com/docs/core/architecture/vintf/fcm).

AIDL Composer3 has been available since Android 13; older HIDL Composer versions are deprecated. That does **not** establish that HIDL Composer 2.4 is universally rejected by every Android 14 target. The exact error must be diagnosed against the real product/vendor manifests, compatibility matrices and shipping API. [AIDL Composer documentation](https://source.android.com/docs/core/graphics/aidl-hwc).

Since the early report, the local project has progressed to **AIDL Composer3/SurfaceFlinger activity on physical hardware** (see [graphics](GRAPHICS.md)). It would be misleading to present Composer3 integration as still completely missing.

The current graphics blocker is **HWUI RenderThread surface setup**, not merely a manifest declaration. Recover the source-specific VINTF logs from the local checkout before making claims about remaining compatibility issues.

This public repository contains the historical issue and summary, not the complete local manifest revisions.
