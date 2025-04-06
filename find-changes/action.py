#!/usr/bin/env python3
"""
Process changed files to find matches based on regex patterns.
"""

import json
import os
import re
import sys
import subprocess
from typing import List, Dict, Any, Set, Tuple


def get_changed_files() -> List[str]:
    """Get list of changed files using git diff."""
    # Determine the base and head commits for comparison
    github_event_name = os.environ.get("GITHUB_EVENT_NAME")

    if github_event_name == "pull_request":
        base_sha = os.environ.get("PR_BASE_SHA")
        head_sha = os.environ.get("PR_HEAD_SHA")
    else:
        # For pushes, compare with previous commit
        base_sha = subprocess.check_output(["git", "rev-parse", "HEAD~1"]).decode("utf-8").strip()
        head_sha = os.environ.get("GITHUB_SHA")

    # Get list of changed files
    try:
        changed_files = subprocess.check_output(
            ["git", "diff", "--name-only", base_sha, head_sha]
        ).decode("utf-8").strip().splitlines()
        return [file for file in changed_files if file.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
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
        if regex_pattern.search(file) and (not exclude_pattern or not exclude_pattern.search(file)):
            # Extract project information
            project_name = file.split("/")[0] if "/" in file else file
            project_path = os.path.dirname(file) or project_name

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
    output_file = os.environ.get("GITHUB_OUTPUT")

    # Validate required inputs
    if not regex:
        print("Error: REGEX environment variable is required")
        sys.exit(1)

    if not output_file:
        print("Error: GITHUB_OUTPUT environment variable is required")
        sys.exit(1)

    # Get and process changed files
    changed_files = get_changed_files()

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
