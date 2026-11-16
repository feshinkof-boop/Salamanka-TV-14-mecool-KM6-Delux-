# Maintenance and publication

**Maintainer:** [@feshinkof-boop](https://github.com/feshinkof-boop).

This is an independent hardware-porting project. The actual engineering changes are maintained on the developer's local workstation; this public GitHub tree presently contains documentation, older investigations and limited host-side tooling.

## Evidence rules

A successful local build is a **build result**. A temporary physical boot with PC-hosted NBD storage is a **device bring-up result**. Neither is an installable release. State explicitly when source logs are not mirrored here.

Do not infer hardware functionality from marketing specifications or from the same SoC in another TV box. Avoid percentages, invented hours worked and unverified feature claims.

## Contributions

Any code contribution must preserve the author and source license. Proprietary vendor binaries need an explicit right to redistribute and a recorded hash/origin. Do not commit device-specific keys, TEE/Widevine material, private IP addresses, signing keys or backup images.

No blanket license has been chosen for original project files. Upstream AOSP/Linux code remains under its existing terms.

No automated task may flash or rewrite the KM6. Physical persistent changes require informed approval and a tested recovery plan.

[Contributing](../CONTRIBUTING.md) · [Security](../SECURITY.md).
