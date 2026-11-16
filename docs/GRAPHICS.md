# Display and Android UI bring-up

**Hardware:** Amlogic S905X4, Mali-G31 MP2, HDMI output.  
**Status:** display/composition path exercised on the physical KM6; launcher is not stable.

## Confirmed progress from local reports

- Linux 6.18.55 and the Meson DRM/KMS path exercised on target.
- HDMI mode-setting observed at **1920×1080, 60 Hz**.
- Mali-G31 graphics progress using Panfrost and Mesa EGL/GLES.
- AIDL Composer3 and SurfaceFlinger communicating in the Android 14 environment.
- Boot-animation-related rendering and DRM atomic commit activity observed in logs.

These observations are useful but do not amount to a verified, fully working graphical desktop. They also do **not** establish the separate S905X4 video-decoder (VPU) stack.

## Current Android UI fault

The system gets far enough to start SystemUI and resume the Leanback HOME activity. A fatal RenderThread signal was observed in the HWUI pipeline around:

```text
libhwui
CanvasContext::setupPipelineSurface
RenderThread SIGABRT
```

A fully usable launcher has **not** been confirmed.

## Investigation questions

- Is the failing layer creation a valid surface for the chosen graphics allocator and gralloc path?
- Are EGL/native buffer formats, modifiers and fences supported consistently end to end?
- Does the Composer service return valid display/configuration and fence results?
- Can the failure be reduced to a simple Activity/surface test before Leanback and SystemUI interactions?
- Does the problem change between permissive debug mode and release-target policy?
- Are the observed DRM commits from expected buffers, rather than just repeated failed or blank frames?

The next progress claim should be backed by a reproduced crash trace, a targeted patch, a stable repeated UI run and direct on-screen verification.

## Separate work

Hardware AVC/HEVC/AV1 decoding requires the S905X4 VPU kernel/userspace pipeline and Android MediaCodec/Codec2 integration. Working GLES and DRM **do not** demonstrate hardware media playback.

[Status](STATUS.md) · [Hardware](HARDWARE.md).
