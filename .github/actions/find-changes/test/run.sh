#!/bin/sh
set -eu

BASE_DIR=$(cd "$(dirname "$0")" && pwd)
TARGET=""

gitcredentials() {
	git config user.name "github-actions[bot]"
	git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
}

arrange() {
	TEST="$1"
	if [ -x "$TEST" ]; then
		# Ensure clean state
		rm -rf "$BASE_DIR/tmp"

		# Setup origin
		(
			mkdir -p "$BASE_DIR/tmp/origin"
			cd "$BASE_DIR/tmp/origin"
			git init
			gitcredentials
			touch README.md
			git add README.md
			git commit -m "Initial commit"
		) > /dev/null 2>&1

		# Setup clone
		(
			git clone "$BASE_DIR/tmp/origin" "$BASE_DIR/tmp/clone"
			cd "$BASE_DIR/tmp/clone"
			gitcredentials
		) > /dev/null 2>&1

		# Execute test setup
		(
			cd "$BASE_DIR/tmp/clone"
			"$TEST"
		) > /dev/null 2>&1
		TARGET=$(cat "$BASE_DIR/tmp/clone/target")
	else
		echo "Error: $TEST is not executable."
		exit 1
	fi
}

act() {
	(cd "$BASE_DIR/tmp/$TARGET" && GITHUB_ENV=output ../../../script.sh) > /dev/null 2>&1
}

assert() {
	TEST="$1"
	TEST_FILE=$(basename "$TEST")

	EXPECTED="$(dirname "$TEST")/expects/$(basename "$TEST" .sh).output"
	ACTUAL="$BASE_DIR/tmp/$TARGET/output"
	if diff "$EXPECTED" "$ACTUAL" > /dev/null; then
		echo "ok   $TEST_FILE"
	else
		echo "FAIL $TEST_FILE"
		echo
        diff --color "$EXPECTED" "$ACTUAL"
    fi
}

# Run all tests
trap 'rm -rf "$BASE_DIR/tmp"' EXIT # Final cleanup
find "$BASE_DIR" -name "*.sh" ! -name "run.sh" | while IFS= read -r TEST; do
	arrange "$TEST"
	act
	assert "$TEST"
done
