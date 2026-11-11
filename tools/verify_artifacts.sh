#!/bin/sh
# Read-only offline check of real images; does not establish device functionality.
set -eu
root="${1:-out/target/product}"
if [ ! -d "$root" ]; then echo "Usage: $0 <directory-containing-build-products>" >&2; exit 2; fi
find "$root" -type f \( -name 'system.img' -o -name 'vendor.img' -o -name 'super.img' -o -name 'product.img' -o -name 'vbmeta_system.img' \) -print | sort | while IFS= read -r f; do
  echo "-- $f"
  sha256sum "$f"
  file "$f"
done
echo "Only filenames, sizes, hash and file headers were examined. No image was flashed."
