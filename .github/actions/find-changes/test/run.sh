#!/bin/bash
set -euo pipefail

BASE_DIR=$(cd "$(dirname "$0")" && pwd)
TARGET=""

gitcredentials() {
	git config user.name "github-actions[bot]"
	git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
}

arrange() {
	TEST="$1"
	if [ -x "$TEST" ]; then
		# No logic should depend on hardcoded default branch name
		DEFAULT_BRANCH_NAME="d$RANDOM"

		# Ensure clean state
		rm -rf "$BASE_DIR/tmp"

		# Setup origin
		(
			mkdir -p "$BASE_DIR/tmp/origin"
			cd "$BASE_DIR/tmp/origin"
			git init
			git branch -M "$DEFAULT_BRANCH_NAME"
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

		# Determine target for act and assert (origin or clone)
		TARGET=$(cat "$(dirname "$TEST")/with target")
	else
		echo "Error: $TEST is not executable."
		exit 1
	fi
}

act() {
	(cd "$BASE_DIR/tmp/$TARGET" && GITHUB_ENV=output ../../../script.sh "$DEFAULT_BRANCH_NAME") > /dev/null 2>&1
}

test_passes() {
    EXPECTED="$1"
    ACTUAL="$2"

	SUCCESS=0
	FAILURE=1

	SHOULD_FAIL="$(dirname "$EXPECTED")/with diff success reverted"
    if [ -f "$SHOULD_FAIL" ]; then
		SUCCESS=1
		FAILURE=0
	fi

	if diff "$EXPECTED" "$ACTUAL" > /dev/null; then
		return "$SUCCESS"
	else
		return "$FAILURE"
	fi
}

assert() {
	TEST="$1"
	TEST_NAME=$(basename "$TEST" .sh)
    TEST_CATEGORY=$(basename "$(dirname "$TEST")")

	EXPECTED="$(dirname "$TEST")/being able to/$(basename "$TEST" .sh)"
	ACTUAL="$BASE_DIR/tmp/$TARGET/output"

	if test_passes "$EXPECTED" "$ACTUAL"; then
		echo "ok   $TEST_CATEGORY can $TEST_NAME"
	else
		echo "FAIL $TEST_CATEGORY can $TEST_NAME"
		echo
        diff --color "$EXPECTED" "$ACTUAL"
    fi
}

single() {
    TEST="$BASE_DIR/$1.sh"
    if [ -f "$TEST" ]; then
        arrange "$TEST"
        act
        assert "$TEST"
    else
        echo "Test file $TEST does not exist."
        exit 1
    fi
}

all() {
	find "$BASE_DIR" -name "*.sh" ! -name "run.sh" | while IFS= read -r TEST; do
		arrange "$TEST"
		act
		assert "$TEST"
	done
}

test() {
	trap 'rm -rf "$BASE_DIR/tmp"' EXIT # Ensure cleanup

	input="${1:-}"

	if [ -z "$input" ]; then
		all
	else
		single "$1"
	fi
}

test
