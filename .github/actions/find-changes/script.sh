#!/bin/sh

# Check if the current branch is main
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" = "main" ]; then
	# Increase checkout depth
	git fetch origin main:main
else
	# Fetch latest state of main branch
	git fetch --depth=1 origin main
fi

# Determine the base ref for comparison using merge base
base_ref=$(git merge-base HEAD origin/main)

# Get the list of changed first-level directories compared to the base ref
changes=$(git diff --name-only "$base_ref...HEAD" | awk -F/ '{print $1}' | sort --unique)

# Filter out files and directories that start with a dot, only include directories
directories=$(echo "$changes" | xargs -I {} sh -c '[ -d "{}" ] && echo "{}"' | grep -v '^\.')

# Format the output for matrix strategy
directories=$(echo "$directories" | jq -R -s -c 'split("\n") | map(select(length > 0))')

# Set the output
echo "directories=${directories}" >> "$GITHUB_ENV"
