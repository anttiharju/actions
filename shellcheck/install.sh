#!/bin/sh

curl -sSL "$URL" | tar -xJ -C "$TMP" --strip-components=1
cp "$TMP/shellcheck" /usr/local/bin/
