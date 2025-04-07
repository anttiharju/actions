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
    expression_path = os.environ.get("expression_path")

    # Write the expression to a file (for security reasons)
    with open(expression_path, "w") as f:
        f.write(yq_expression)

    # Run yq to extract the glob pattern
    try:
        result = subprocess.run(
            ["yq", "--from-file", expression_path, yaml_file],
            capture_output=True,
            text=True,
            check=True,
        )
        pattern = result.stdout.strip()

        # Check if yq found anything (empty or null result)
        if not pattern or pattern == "null":
            print(f"Error: yq expression did not match anything in file '{yaml_file}'")
            sys.exit(1)

        return pattern
    except subprocess.CalledProcessError as e:
        print(f"Error executing yq command: {e.stderr}")
        sys.exit(1)


def expand_braces(pattern):
    """Expand brace patterns like {a,b} into separate patterns"""
    # Find all brace patterns
    brace_pattern = re.compile(r"{([^{}]*)}")
    match = brace_pattern.search(pattern)
    if not match:
        return [pattern]

    # Get the options inside braces
    options = match.group(1).split(",")
    start, end = match.span()

    # Create patterns with each option substituted
    results = []
    for option in options:
        new_pattern = pattern[:start] + option + pattern[end:]
        # Recursively expand any remaining braces
        results.extend(expand_braces(new_pattern))

    return results


def check_changes(glob_pattern, changed_files):
    """Check changed files based on glob patterns"""
    changed = False

    # First, handle comma-separated patterns outside of braces
    patterns = []

    # Check if the pattern has commas outside of braces
    if "," in glob_pattern and "{" not in glob_pattern:
        patterns = [p.strip() for p in glob_pattern.split(",")]
    else:
        # Process patterns with braces
        if "{" in glob_pattern:
            patterns = expand_braces(glob_pattern)
        else:
            patterns = [glob_pattern]

    for file_path in changed_files:
        for pattern in patterns:
            # Use fnmatch for glob pattern matching
            if fnmatch.fnmatch(file_path, pattern):
                print(f"Match found: {file_path} matches pattern {pattern}")
                changed = True
                break

        if changed:
            break

    return changed


def main():
    try:
        # Get inputs from environment variables
        changes_json = os.environ.get("changes")

        # Check if file exists before extraction
        yaml_file = os.environ.get("file")
        if not os.path.isfile(yaml_file):
            print(f"Error: File not found: {yaml_file}")
            sys.exit(1)

        # Extract glob pattern
        glob_pattern = extract_glob_pattern()
        print(f"glob={glob_pattern}")

        # Parse the changes JSON
        try:
            changed_files = json.loads(changes_json)
        except json.JSONDecodeError:
            print("Error: Failed to parse changes JSON")
            sys.exit(1)

        # Check glob
        changed = check_changes(glob_pattern, changed_files)

        # Output the result
        github_output = os.environ.get("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"changed={str(changed).lower()}\n")
        # Log the result
        print(f"changed={str(changed).lower()}")

    except Exception as e:
        print(f"Error: Unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
