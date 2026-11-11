#!/bin/sh
# Local/ADB-only read-only diagnostic sketch. NEVER writes to partitions.
# Run only after isolating the test device and confirming target.
set -eu
if ! command -v adb >/dev/null 2>&1; then echo "adb required" >&2; exit 1; fi
echo "== Build identity =="
adb shell getprop ro.build.fingerprint
adb shell getprop ro.product.model
adb shell getprop ro.product.device
adb shell getprop ro.build.version.release
adb shell getprop ro.product.cpu.abilist
adb shell getprop ro.boot.verifiedbootstate
echo "== Known research package names (absence is not proof of safety) =="
for pkg in x.cpe com.oemservice com.abc.nexus com.android.system.ntp com.android.sso.auth.handler; do
  echo "-- $pkg"
  adb shell cmd package path "$pkg" || :
done
echo "== Security runtime status =="
adb shell getenforce || :
adb shell settings get global package_verifier_user_consent || :
echo "== Sensitive outputs omitted intentionally =="
echo "No full getprop, serials, network addresses, dumpsys or partition backups are saved by this script."
