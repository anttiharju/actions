#!/bin/sh

default_branch="$1"

# Check if current branch is the default branch
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" = "$default_branch" ]; then
	# Increase checkout depth
	git fetch origin "$default_branch:$default_branch"
else
	# Fetch latest state of default branch branch
	git fetch --depth=1 origin "$default_branch:$default_branch"
fi

# Determine the base ref
base_ref=$(git merge-base HEAD "origin/$default_branch")

# Get the list of changed first-level directories compared to the base ref
changes=$(git diff --name-only "$base_ref...HEAD" | awk -F/ '{print $1}' | sort --unique)

# Filter out files and directories that start with a dot, only include directories
directories=$(echo "$changes" | xargs -I {} sh -c '[ -d "{}" ] && echo "{}"' | grep -v '^\.')

# Format the output for matrix strategy
directories=$(echo "$directories" | jq -R -s -c 'split("\n") | map(select(length > 0))')

# Set the output
echo "directories=${directories}" >> "$GITHUB_ENV"
