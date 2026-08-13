#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
GRADLE_VERSION=8.13
CACHE="$ROOT/.gradle-bootstrap/gradle-$GRADLE_VERSION"
if [ ! -x "$CACHE/bin/gradle" ]; then
  mkdir -p "$ROOT/.gradle-bootstrap"
  ARCHIVE="$ROOT/.gradle-bootstrap/gradle.zip"
  if command -v curl >/dev/null 2>&1; then curl -L --fail -o "$ARCHIVE" "https://services.gradle.org/distributions/gradle-$GRADLE_VERSION-bin.zip"; else wget -O "$ARCHIVE" "https://services.gradle.org/distributions/gradle-$GRADLE_VERSION-bin.zip"; fi
  rm -rf "$CACHE"
  mkdir -p "$CACHE"
  unzip -q "$ARCHIVE" -d "$ROOT/.gradle-bootstrap/unpack"
  mv "$ROOT/.gradle-bootstrap/unpack/gradle-$GRADLE_VERSION" "$CACHE"
  rm -rf "$ROOT/.gradle-bootstrap/unpack" "$ARCHIVE"
fi
exec "$CACHE/bin/gradle" "$@"
