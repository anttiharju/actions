#!/usr/bin/env bash
set -euo pipefail

PKGS_DIR="pkgs"
DEFAULT_NIX="default.nix"

# Check if pkgs directory exists
if [ ! -d "$PKGS_DIR" ]; then
  echo "Error: $PKGS_DIR directory not found"
  exit 1
fi

# Check if default.nix exists
if [ ! -f "$DEFAULT_NIX" ]; then
  echo "Error: $DEFAULT_NIX not found"
  exit 1
fi

# Get list of package directories
packages=$(find "$PKGS_DIR" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort)

# Create temporary file
temp_file=$(mktemp)

# Read default.nix and process it
while IFS= read -r line; do
  # Skip lines with pkgs.callPackage
  if echo "$line" | grep -q "pkgs.callPackage"; then
    continue
  fi

  # Detect the closing brace of the package set
  if echo "$line" | grep -q "^}"; then
    # Inject package calls before the closing brace
    for pkg in $packages; do
      # Skip if not a directory
      if [ ! -d "$PKGS_DIR/$pkg" ]; then
        continue
      fi
      echo "  $pkg = pkgs.callPackage ./pkgs/$pkg { };" >> "$temp_file"
    done
  fi

  echo "$line" >> "$temp_file"
done < "$DEFAULT_NIX"

# Replace original file with updated one
mv "$temp_file" "$DEFAULT_NIX"

echo "Successfully synced packages in $DEFAULT_NIX"
for pkg in $packages; do
  if [ -d "$PKGS_DIR/$pkg" ]; then
    echo "  - $pkg"
  fi
done
