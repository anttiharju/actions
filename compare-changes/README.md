# compare-changes

Takes JSON array from [](../find-changes/) and outputs whether any files matching the paths in a `wildcard` workflow have changed.

## Example

```yml
# ./.github/workflows/wildcard-actionlint.yml
on:
  push:
    branches:
      - wildcard
    paths:
      - ".github/workflows/*.yml"

jobs:
  wildcard:
    runs-on: ubuntu-latest
    if: false
    steps:
      - run: |
          true
```

```yml
# ./.github/workflows/validate.yml
name: "Detect changes"
description: "Decide what steps need running based on changes"
inputs:
  changes:
    description: "JSON array of changed files"
    required: true
runs:
  using: "composite"
  steps:
    - name: Find changes
      id: changes
      uses: anttiharju/actions/find-changes@v1
    - id: actionlint
      uses: anttiharju/actions/compare-changes@v1
      with:
        wildcard: actionlint
        changes: ${{ steps.changes.outputs.array }}
    - if: steps.changed.outputs.actionlint == 'true' || github.event_name != 'pull_request'
      name: actionlint
      uses: anttiharju/actions/actionlint@v1
```
