# XCPE and firmware provenance gate

- [ ] Enumerate all partitions and boot slots **without writing**.
- [ ] Hash all accessible APK/DEX/ELF/firmware blobs from current build and donor images.
- [ ] Generate a machine-readable SBOM: image, path, hash, architecture, package name, signer, purpose, privilege, origin, license.
- [ ] Examine `/oem`, `/odm`, `/vendor`, `/system/priv-app`, init RC, SELinux policy, manifests and updater.
- [ ] Check IOCs published by Google/Synthient/Plume, including `x.cpe`, `com.oemservice`, `com.abc.nexus`, `com.android.system.ntp`, `com.android.sso.auth.handler`.
- [ ] Scan for suspicious domains/protocols, HTTP/MQTT clients, dynamic loading, package installation and unexpected shells.
- [ ] Review every `android.uid.system`, privileged permission and boot receiver.
- [ ] Enforce no vendor HAL arbitrary Internet access absent evidence.
- [ ] Verify AVB signing keys, update process and rollback; **never** relock until complete recovery is demonstrated.
- [ ] Test clean installation, reboot and factory reset for repopulation of suspicious packages.
- [ ] Sanitize packet captures and logs (MAC/IP/account/serial) before public upload.
- [ ] Perform independent review; a zero known-IOC match is **not** evidence of complete cleanliness.

## Placeholders

Populate `security/BINARY-PROVENANCE.csv` from actual local build sources. Do not invent hashes or source paths.