#!/usr/bin/env python3

import os
import json
import subprocess
import fnmatch
import re
import sys


def extract_glob_pattern():
    """Extract glob pattern from YAML file using yq expression"""
    yq_expression = os.environ.get("yq")
    yaml_file = os.environ.get("file")
    expression_path = os.environ.get("expression")

    # Write the expression to a file (for security reasons)
    with open(expression_path, "w") as f:
        f.write(yq_expression)

    # Run yq to extract the glob pattern
    result = subprocess.run(
        ["yq", "--from-file", expression_path, yaml_file],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.strip()


def filter_changes(glob_pattern, changed_files):
    """Filter changed files based on glob patterns"""
    have_changed = False

    # Process glob patterns (multiple patterns may be separated by commas in curly braces)
    # Remove curly braces and split by commas
    patterns = re.sub(r"[{}]", "", glob_pattern).split(",")

    for file_path in changed_files:
        for pattern in patterns:
            pattern = pattern.strip()
            # Use fnmatch for more robust glob pattern matching
            if fnmatch.fnmatch(file_path, pattern):
                print(f"Match found: {file_path} matches pattern {pattern}")
                have_changed = True
                break

        if have_changed:
            break

    return have_changed


def main():
    # Get inputs from environment variables
    changes_json = os.environ.get("changes")

    # Extract glob pattern
    glob_pattern = extract_glob_pattern()

    # Parse the changes JSON
    try:
        changed_files = json.loads(changes_json)
    except json.JSONDecodeError:
        print("Error: Failed to parse changes JSON")
        sys.exit(1)

    # Filter changes
    have_changed = filter_changes(glob_pattern, changed_files)

    # Output the result
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"have_changed={str(have_changed).lower()}\n")
    else:
        print(f"have_changed={str(have_changed).lower()}")


if __name__ == "__main__":
    main()
