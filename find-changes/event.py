#!/usr/bin/env python3

import os
import sys


def main():
    """Check if the GitHub event is allowed (pull_request, merge_group, or push)."""
    # Get the event name from GitHub Actions environment
    event_name = os.environ.get("GITHUB_EVENT_NAME")

    # List of allowed event types
    allowed_events = ["pull_request", "merge_group", "push"]

    # Check if the event type is allowed
    if not event_name:
        print("Error: GITHUB_EVENT_NAME environment variable is not set.")
        sys.exit(1)

    if event_name not in allowed_events:
        print(
            f"Error: Unsupported event type '{event_name}'. "
            f"Only {', '.join(allowed_events)} events are supported."
        )
        sys.exit(1)

    print(f"Event '{event_name}' is allowed. Proceeding...")
    sys.exit(0)


if __name__ == "__main__":
    main()
