# Critical correction: Android 14 FCM and Composer (2026-11-12)

The initial repository incorrectly said that FCM **202404** is Android 14 and therefore AIDL Composer3 is universally mandatory. **FCM 8 corresponds to Android 14 (U); 202404 belongs to Android 15 (V).** [AOSP FCM lifecycle](https://source.android.com/docs/core/architecture/vintf/fcm).

Google [AIDL Hardware Composer documentation](https://source.android.com/docs/core/graphics/aidl-hwc) says AIDL Composer3 has been defined since Android 13; HIDL Composer 2.1–2.4 is **deprecated**, which does not by itself imply that every Android 14 framework rejects HIDL Composer 2.4.

## Actual issue requiring diagnosis

The November 2026 local build previously reported a **checkvintf failure at FCM 202404**, with a vendor manifest declaring **HIDL Composer 2.4**. We **do not have the original complete source and logs in this GitHub repository**. It is not yet established whether the primary error is an incorrect target FCM, a matrix mismatch, a missing HAL instance, or incompatible HAL transport.

**Do not blindly set level 8 or replace a running compositor with an untested AIDL stub.** Investigate:

1. Locate and publish the sanitized full `checkvintf` invocation and error.
2. Inspect the actual `DEVICE_MANIFEST_FILE`, product/system/vendor/ODM compatibility matrices and FCM declarations.
3. Verify Android 14 source revision and `hardware/interfaces/compatibility_matrices/compatibility_matrix.8.xml`.
4. Compare `PRODUCT_SHIPPING_API_LEVEL`, `ro.product.first_api_level`, `ro.vendor.api_level` (where present), and SELinux policy version.
5. Inspect the Composer service implementation, its VINTF registration, GPU gralloc allocator, DRM/KMS and binder interfaces.
6. Resolve compatibility for a valid target FCM with host-side VINTF tests, then demonstrate physical composition, not just XML compatibility.

**AIDL Composer3 is a modernization option, not a proven requirement for this exact historical build configuration.**
