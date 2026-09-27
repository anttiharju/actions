#!/usr/bin/env bash
set -euo pipefail

case "$TARGET" in
  aarch64-apple-darwin) checksum="$MACOS_ARM_SHA" ;;
  aarch64-unknown-linux-musl) checksum="$LINUX_ARM_SHA" ;;
  x86_64-unknown-linux-musl) checksum="$LINUX_X64_SHA" ;;
  *) echo "Unsupported target: $TARGET" >&2; exit 1 ;;
esac

printf '%s  %s\n' "$checksum" "$BINARY" | shasum -a 256 -c
