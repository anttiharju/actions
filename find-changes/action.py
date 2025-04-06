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


def get_github_env_variables() -> Dict[str, str]:
    """Get required GitHub environment variables."""
    # Common GitHub env variables
    github_event_name = os.environ.get("GITHUB_EVENT_NAME")
    github_event_path = os.environ.get("GITHUB_EVENT_PATH")
    github_sha = os.environ.get("GITHUB_SHA")
    github_output = os.environ.get("GITHUB_OUTPUT")
    github_action_path = os.environ.get("GITHUB_ACTION_PATH")

    # Read event data if available
    pr_base_sha = None
    pr_head_sha = None

    if github_event_path and os.path.exists(github_event_path):
        try:
            with open(github_event_path, 'r') as f:
                event_data = json.load(f)
                if github_event_name == 'pull_request':
                    # Extract PR-specific information
                    pr_base_sha = event_data.get('pull_request', {}).get('base', {}).get('sha')
                    pr_head_sha = event_data.get('pull_request', {}).get('head', {}).get('sha')
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read event data: {e}")

    return {
        "GITHUB_EVENT_NAME": github_event_name,
        "GITHUB_SHA": github_sha,
        "GITHUB_OUTPUT": github_output,
        "GITHUB_ACTION_PATH": github_action_path,
        "PR_BASE_SHA": pr_base_sha,
        "PR_HEAD_SHA": pr_head_sha
    }


def get_changed_files() -> List[str]:
    """Get list of changed files using git diff."""
    # Get GitHub environment variables
    github_vars = get_github_env_variables()
    github_event_name = github_vars["GITHUB_EVENT_NAME"]

    if github_event_name == "pull_request" and github_vars["PR_BASE_SHA"] and github_vars["PR_HEAD_SHA"]:
        base_sha = github_vars["PR_BASE_SHA"]
        head_sha = github_vars["PR_HEAD_SHA"]
    else:
        # For pushes, compare with previous commit
        try:
            base_sha = subprocess.check_output(["git", "rev-parse", "HEAD~1"]).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            # If the above fails (e.g., shallow clone with only one commit),
            # try getting the first parent commit
            try:
                merge_base = subprocess.check_output(
                    ["git", "rev-parse", "HEAD^1"]
                ).decode("utf-8").strip()
                base_sha = merge_base
            except subprocess.CalledProcessError as e:
                print(f"Error getting base commit: {e}")
                # Fallback to empty tree object if we can't get a parent
                base_sha = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"  # git empty tree hash

        head_sha = github_vars["GITHUB_SHA"]

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
    # Get GitHub environment variables
    github_vars = get_github_env_variables()

    # Get input variables - updated to match the action.yml input names
    regex = os.environ.get("REGEX")
    all_regex = os.environ.get("ALL_REGEX")  # Changed to ALL_REGEX to match input name all-regex
    exclude_regex = os.environ.get("EXCLUDE_REGEX")
    existing_matrix = os.environ.get("EXISTING_MATRIX", "[]")
    output_file = github_vars["GITHUB_OUTPUT"]

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
    match_all_pattern = re.compile(all_regex) if all_regex else None  # Variable name updated
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
