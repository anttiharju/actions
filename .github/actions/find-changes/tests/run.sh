#!/bin/sh

BASE_DIR=$(cd "$(dirname "$0")" && pwd)

run_script() {
	local SCRIPT_PATH="$1"
	if [ -x "$SCRIPT_PATH" ]; then
		"$SCRIPT_PATH"
	else
		echo "Error: $SCRIPT_PATH is not executable or does not exist"
		exit 1
	fi
}

if [ -z "$1" ]; then
	FILES=$(cd "$BASE_DIR/scenarios" && ls)
	FILE_ARRAY=($FILES)

	# Iterate over the array and run each script
	for TEST in "${FILE_ARRAY[@]}"; do
		run_script "$BASE_DIR/scenarios/$TEST"
	done
else
	run_script "$BASE_DIR/scenarios/$1.sh"
fi
