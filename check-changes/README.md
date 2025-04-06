# Filter changes

[![check-changes](https://github.com/anttiharju/actions/actions/workflows/check-changes.yml/badge.svg)](https://github.com/anttiharju/actions/actions/workflows/check-changes.yml)

This is a sibling action to [find changes](../find-changes/). With the two actions combined, following CI jobs or steps can run conditionally based on changes.

## Usage example

```yml
jobs:
  example:
    name: Example
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Find changes
        id: changed
        uses: anttiharju/actions/find-changes@5ec924ed92a6b276f2add1ffe31e9fa012cc2ed8

      - name: Filter changes
        id: workflows
        uses: anttiharju/actions/check-changes@5ec924ed92a6b276f2add1ffe31e9fa012cc2ed8
        with:
          changes: ${{ steps.changed.outputs.files }}
          file: lefthook.yml
          yq: '.pre-commit.jobs[] | select(.name == "actionlint") | .glob'

      - if: steps.workflows.outputs.changed == 'true'
        name: Echo true
        shell: sh
        run: |
          echo ${{ steps.workflows.outputs.changed }}
```
