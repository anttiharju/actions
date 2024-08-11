#!/bin/sh

default_branch="$1"

# Check if current branch is the default branch
current_branch=$(git rev-parse --abbrev-ref HEAD)
base_ref=""
if [ "$current_branch" = "$default_branch" ]; then
	if git log -1 --pretty=%P | grep -q ' '; then
		git fetch --depth=2 origin "$default_branch:$default_branch"
		merge_ref=$(git log --merges -n 1 --pretty=format:"%H")
		base_ref=$(git rev-parse HEAD^) # merge commit
	else
		latest_commit=$(git rev-parse HEAD)
		base_ref=$(git merge-base HEAD "$default_branch")
		if [ "$latest_commit" = "$base_ref" ]; then
			base_ref=$(git rev-parse HEAD^) # squash
		else
			base_ref=$(git merge-base HEAD "$default_branch") # rebase
		fi
	fi
else
	# Fetch latest state of default branch branch
	git fetch --depth=1 origin "$default_branch:$default_branch"
	base_ref=$(git merge-base HEAD "$default_branch")
fi

# Get the list of changed first-level directories compared to the base ref
changes=$(git diff --name-only "$base_ref...HEAD" | awk -F/ '{print $1}' | sort --unique)

# Filter out files and directories that start with a dot, only include directories
directories=$(echo "$changes" | xargs -I {} sh -c '[ -d "{}" ] && echo "{}"' | grep -v '^\.')

# Format the output for matrix strategy
directories=$(echo "$directories" | jq -R -s -c 'split("\n") | map(select(length > 0))')

# Set the output
echo "directories=${directories}" >> "$GITHUB_ENV"
