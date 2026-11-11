# Salamanka TV 14 user-facing design

The features below are **proposed**, not implemented. They should be introduced after essential hardware acceptance.

## Media Engine
- Per-app and per-content AFR, EDID mode list, HDR/SDR policies, frame-rate/resolution diagnostics.
- Supported output bit depth/color mode only; avoid impossible HDMI settings.
- Decoder stats (codec name, hardware/software, dropped frames, frame pacing), optional performance HUD.
- Audio profile output (HDMI, optical, analog, USB/Bluetooth), sync offset, passthrough status.

## Remote Manager
- V01 voice, V03 and compatible third-party remotes; HID/mic diagnostics.
- Button mapping for sponsored/shortcut keys, long-press/double-press actions; event-level inspection.
- Bluetooth connection/battery state where exposed; proper wake routing.

## Power Manager
- Sleep, network standby, supported deep sleep, reboot/shutdown, HDMI-CEC coordination.
- Wake history and explicit separation of radio wake, IR wake, Bluetooth wake, network wake.

## Performance + Network Suite
- Thermal, memory, GPU, storage and background-work graphs.
- Optional local SFTP/SSH, SMB/NFS, VPN, media server and background transfers; explicit opt-in and least privilege.
- A TV-friendly launcher and task switcher with optional supported PiP/split screen.

Avoid invented capability claims: availability depends on board-level drivers, HALs, app support and licenses.