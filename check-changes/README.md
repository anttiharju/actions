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
        uses: anttiharju/actions/find-changes@2ea89c9f5dc95de4353022345f87ea746cbc60a9

      - name: Filter changes
        id: workflows
        uses: anttiharju/actions/check-changes@2ea89c9f5dc95de4353022345f87ea746cbc60a9
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
