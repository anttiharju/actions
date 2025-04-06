#!/usr/bin/env python3
"""
Process changed files to find matches based on regex patterns.
"""

import json
import os
import re
import sys
from typing import List, Dict, Any, Set


def read_changed_files(file_path: str) -> List[str]:
    """Read the list of changed files from a file."""
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except IOError as e:
        print(f"Error reading changed files: {e}")
        sys.exit(1)


def process_matrix(matrix_json: str) -> List[Dict[str, Any]]:
    """Parse and validate the input matrix JSON."""
    if not matrix_json or matrix_json == "[]":
        return []

    try:
        return json.loads(matrix_json)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in existing matrix input")
        sys.exit(1)


def process_changed_files(
    changed_files: List[str],
    regex_pattern: re.Pattern,
    match_all_pattern: re.Pattern = None,
    exclude_pattern: re.Pattern = None,
    existing_matrix: List[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Process the changed files and return matches."""
    if existing_matrix is None:
        existing_matrix = []

    # Check if we should include all matches
    include_all = False
    if match_all_pattern:
        for file in changed_files:
            if match_all_pattern.search(file):
                include_all = True
                break

    # Find matches
    existing_paths: Set[str] = set()
    for item in existing_matrix:
        if "path" in item:
            existing_paths.add(item["path"])

    new_matches = []
    for file in changed_files:
        # Check if file matches the main regex or should be included due to match_all
        if regex_pattern.search(file) or (include_all and regex_pattern.search(file)):
            # Skip if file matches exclude pattern
            if exclude_pattern and exclude_pattern.search(file):
                continue

            # Extract project information
            project_name = file.split("/")[0] if "/" in file else file
            project_path = os.path.dirname(file)

            # Only add if this path isn't already in the matrix
            if project_path not in existing_paths:
                new_matches.append({
                    "name": project_name,
                    "path": project_path,
                    "file": file
                })
                existing_paths.add(project_path)

    # Add new matches to result matrix
    result_matrix = existing_matrix.copy()
    result_matrix.extend(new_matches)
    return result_matrix


def write_output(output_file: str, result_matrix: List[Dict[str, Any]]) -> None:
    """Write the result matrix to the GitHub Actions output file."""
    try:
        with open(output_file, "a") as f:
            f.write("matrix<<EOF\n")
            f.write(json.dumps(result_matrix))
            f.write("\nEOF\n")
    except IOError as e:
        print(f"Error writing output: {e}")
        sys.exit(1)


def main():
    """Main function."""
    # Get environment variables
    regex = os.environ.get("REGEX")
    match_all_regex = os.environ.get("MATCH_ALL_REGEX")
    exclude_regex = os.environ.get("EXCLUDE_REGEX")
    existing_matrix = os.environ.get("EXISTING_MATRIX", "[]")
    changed_files_path = os.environ.get("CHANGED_FILES_PATH")
    output_file = os.environ.get("GITHUB_OUTPUT")

    # Validate required inputs
    if not regex:
        print("Error: REGEX environment variable is required")
        sys.exit(1)

    if not changed_files_path:
        print("Error: CHANGED_FILES_PATH environment variable is required")
        sys.exit(1)

    if not output_file:
        print("Error: GITHUB_OUTPUT environment variable is required")
        sys.exit(1)

    # Read changed files
    changed_files = read_changed_files(changed_files_path)

    # Process existing matrix
    matrix = process_matrix(existing_matrix)

    # Compile regex patterns
    regex_pattern = re.compile(regex)
    match_all_pattern = re.compile(match_all_regex) if match_all_regex else None
    exclude_pattern = re.compile(exclude_regex) if exclude_regex else None

    # Process changed files
    result_matrix = process_changed_files(
        changed_files,
        regex_pattern,
        match_all_pattern,
        exclude_pattern,
        matrix
    )

    # Write output
    write_output(output_file, result_matrix)


if __name__ == "__main__":
    main()
