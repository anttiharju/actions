#!/usr/bin/env python3

import os
import subprocess
import json
import sys


def ensure_sufficient_git_depth(event_name, event_data):
    """Ensure the git repository has enough history to perform the diff."""
    print("Ensuring sufficient git history...")

    try:
        # Determine what commit we need to fetch
        target_commit = None

        if event_name == "push" and event_data.get("before"):
            target_commit = event_data["before"]
        elif event_name in ("pull_request", "merge_group"):
            if event_data.get("repository") and event_data["repository"].get(
                "default_branch"
            ):
                # For PR events, we need to ensure we have the default branch
                default_branch = event_data["repository"]["default_branch"]

                # Fetch the default branch
                subprocess.run(
                    [
                        "git",
                        "fetch",
                        "--depth=1",
                        "--no-tags",
                        "origin",
                        f"{default_branch}:refs/remotes/origin/{default_branch}",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                print(f"Fetched default branch: origin/{default_branch}")
                return

        if target_commit:
            # Fetch the specific commit we need
            subprocess.run(
                ["git", "fetch", "--depth=1", "--no-tags", "origin", target_commit],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"Fetched commit: {target_commit}")

    except subprocess.CalledProcessError as e:
        print(f"Warning: Error while fetching git history: {e.stderr}", file=sys.stderr)
        print("Continuing with available history...")


def run_git_diff(comparison_point):
    """Run git diff to get changed files."""
    print("Finding changed files")
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", comparison_point],
            capture_output=True,
            text=True,
            check=True,
        )
        # Filter out empty lines and return list of changed files
        return [file for file in result.stdout.splitlines() if file]
    except subprocess.CalledProcessError:
        print(f"Error running git diff against {comparison_point}", file=sys.stderr)
        return []


def handle_push(event_data):
    """Handle push events to determine branch point."""
    if event_data.get("before"):
        print(f"Found branch point {event_data['before']}")
        return event_data["before"]

    print("Unable to determine push branch point to compare changes.", file=sys.stderr)
    sys.exit(1)


def handle_pull_request(event_data):
    """Handle pull_request or merge_group events to determine branch point."""
    if event_data.get("action") == "closed":
        print(
            "Running find-changes on: pull_request: closed is not supported in v2 - please migrate workflow to on: push:",
            file=sys.stderr,
        )
        sys.exit(1)

    if event_data.get("repository") and event_data["repository"].get("default_branch"):
        upstream = f"origin/{event_data['repository']['default_branch']}"
        print(f"Found branch point {upstream}")
        return upstream

    print(
        "Unable to determine pull request branch point to compare changes.",
        file=sys.stderr,
    )
    sys.exit(1)


def get_branch_point(event_name, event_data):
    """Get the branch point for comparison based on event type."""
    if event_name in ("pull_request", "merge_group"):
        return handle_pull_request(event_data)
    elif event_name == "push":
        return handle_push(event_data)
    else:
        print(
            "find-changed-packages only works on pull_request, merge_group, and push events",
            file=sys.stderr,
        )
        sys.exit(1)


def get_event_data():
    """Load GitHub event data from the event path file."""
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    print(f"Reading event from {event_path}")

    if not event_path:
        print(
            "Could not find event payload file to determine branch point.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        with open(event_path) as f:
            event_data = json.load(f)
            if not event_data:
                print("Event payload does not provide data.", file=sys.stderr)
                sys.exit(1)
            return event_data
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading event data: {e}", file=sys.stderr)
        sys.exit(1)


def get_github_event():
    """Get the GitHub event type from environment variables."""
    return os.environ.get("GITHUB_EVENT_NAME")


def main():
    """Main function to output changed files in GitHub Actions format."""
    event_name = get_github_event()
    event_data = get_event_data()

    # Ensure we have sufficient git history before proceeding
    ensure_sufficient_git_depth(event_name, event_data)

    # Get the branch point for comparison
    diff_base = get_branch_point(event_name, event_data)

    print(f'Using branch point of "{diff_base}" to determine changes')

    # Get the changed files using git diff
    array = run_git_diff(diff_base)

    # Output the changed files
    print(f"Found {len(array)} changed files")

    # Write to GITHUB_OUTPUT file using the new approach
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output and array:
        files_output = json.dumps(array)
        appending_mode = "a"
        with open(github_output, appending_mode) as f:
            f.write(f"array={files_output}\n")

    # Print changed files for logging
    if array:
        for file in array:
            print(f"Changed: {file}")
    else:
        print("No files changed")


if __name__ == "__main__":
    main()
