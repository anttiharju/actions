#!/usr/bin/env python3
# filepath: /Users/antti/anttiharju/actions/find-changes/action.py

import os
import yaml
import fnmatch
import sys


def main():
    # Check if we're in test mode
    test_file = os.environ.get("test-file")

    if test_file:
        # We're in test mode, use the test file
        with open(test_file, "r") as f:
            test_data = yaml.safe_load(f)

        # Use test inputs instead of actual git diff
        changed_files = [item["path"] for item in test_data.get("input_files", [])]

        # Still extract the glob pattern normally
        glob_pattern = extract_glob_pattern(os.environ["glob-file"])

        # Match files against the pattern
        has_changes = any(fnmatch.fnmatch(file, glob_pattern) for file in changed_files)

        # Set output
        set_github_output("has_changes", str(has_changes).lower())

        # Check if result matches expected output (for testing purposes)
        expected = test_data.get("expected_output", {}).get("has_changes")
        if expected is not None and has_changes != expected:
            print(
                f"TEST FAILED: Expected {expected}, got {has_changes}", file=sys.stderr
            )
            sys.exit(1)
        else:
            print("TEST PASSED")
    else:
        # Normal production mode - use real git diff
        event_name = os.environ.get("GITHUB_EVENT_NAME")
        glob_pattern = extract_glob_pattern(os.environ["glob-file"])

        # Get changed files based on event type
        if event_name == "pull_request":
            # Handle PR case
            # ...
            pass
        else:  # Assume push event otherwise
            # Handle push case
            # ...
            pass

        # TODO: Implement the actual git diff logic based on your README logic
        # ...


def extract_glob_pattern(glob_file_path):
    # Parse the glob-file input in format 'file.yml:path.to.key'
    parts = glob_file_path.split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid glob-file format: {glob_file_path}")

    file_path, key_path = parts

    with open(file_path, "r") as f:
        yaml_data = yaml.safe_load(f)

    # Navigate the nested structure to get the glob pattern
    keys = key_path.split(".")
    result = yaml_data
    for key in keys:
        result = result.get(key)
        if result is None:
            raise ValueError(f"Key path {key_path} not found in {file_path}")

    return result


def set_github_output(name, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"{name}={value}\n")


if __name__ == "__main__":
    main()
