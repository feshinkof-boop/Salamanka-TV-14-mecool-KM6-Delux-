# Actionable P0 blockers

1. **Independent XCPE supply chain audit:** examine real Android 14 and donor images; complete `security/BINARY-PROVENANCE.csv`. Do not assume a model-family match establishes compromise.
2. **Android 14 HAL VINTF:** investigate why an Android 14 build used Android 15-level FCM 202404; compare real manifests against Android 14 FCM 8, then demonstrate KMS composition. AIDL migration is an option, not a presumed mandate.
3. **64-bit-only runtime:** investigate any 32-bit-only legacy Amlogic HAL and build verified ARM64 replacements.
4. **Hardware video decode:** determine VPU driver, Codec2/MediaCodec service and 4K AV1/HEVC support under the selected kernel.
5. **Audio:** implement and test HDMI, optical SPDIF and analog routing on S905X4.
6. **V01 voice:** enumerate original remote transport and microphone protocol; compare stock configuration and V03 behavior without copying entire packages.
7. **Wireless/Ethernet/BT:** validate exact Rev1 PHY/radio, firmware provenance, wake/reconnect, throughput and interference.
8. **Recovery:** inventory active slots, dynamic partitions, U-Boot/AVB and known-good readbacks, and prove a safe rollback route without dangerous writes during investigation.
9. **Security baseline:** enforce SELinux, remove unjustified privileged services, ensure all release keys/config are under project control.

Each task must be accompanied by evidence; update STATUS.md and release gates only when verified.