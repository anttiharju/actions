#!/bin/bash
set -euo pipefail

BASE_DIR=$(cd "$(dirname "$0")" && pwd)

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

		# Setup GitHub (source-of-truth)
		(
			mkdir -p "$BASE_DIR/tmp/origin"
			cd "$BASE_DIR/tmp/origin"
			git init
			git branch -M "$DEFAULT_BRANCH_NAME"
			gitcredentials
			touch 1
			git add 1
			git commit -m "first commit"
			touch 2
			git add 2
			git commit -m "second commit"
			git config receive.denyCurrentBranch ignore
		) > /dev/null 2>&1
		(
			cd "$BASE_DIR/tmp/origin"
			"$TEST"
		) > /dev/null 2>&1

		# Mock the checkout on a GitHub Actions Runner
		(
			BRANCH_FILE="$(dirname "$TEST")/on branch"
			if [ -f "$BRANCH_FILE" ]; then
				BRANCH=$(cat "$BRANCH_FILE")
				git clone --depth 1 --branch "$BRANCH" "file://$BASE_DIR/tmp/origin" "$BASE_DIR/tmp/clone"
			else
				git clone --depth 1 "file://$BASE_DIR/tmp/origin" "$BASE_DIR/tmp/clone"
			fi
			cd "$BASE_DIR/tmp/clone"
			gitcredentials
		) > /dev/null 2>&1

	else
		echo "Error: $TEST is not executable."
		exit 1
	fi
}

act() {
	(cd "$BASE_DIR/tmp/clone" && GITHUB_ENV=output ../../../script.sh "$DEFAULT_BRANCH_NAME") > /dev/null 2>&1
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
	ACTUAL="$BASE_DIR/tmp/clone/output"

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
	trap 'rm -rf "$BASE_DIR/tmp"' EXIT # Ensure cleanup
	find "$BASE_DIR" -name "*.sh" ! -name "run.sh" | while IFS= read -r TEST; do
		arrange "$TEST"
		act
		assert "$TEST"
	done
}

test() {
	input="$1"
	if [ -z "$input" ]; then
		all
	else
		single "$1"
	fi
}

test "${1:-}"
