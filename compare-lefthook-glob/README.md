# Compare Lefthook glob

[![compare-lefthook-glob](https://github.com/anttiharju/actions/actions/workflows/compare-lefthook-glob.yml/badge.svg)](https://github.com/anttiharju/actions/actions/workflows/compare-lefthook-glob.yml)

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
        id: changes
        uses: anttiharju/actions/find-changes@c438e97d73d750c3fc202d1342eb1b27aad17dd8

      - name: Compare Lefthook glob
        id: workflows
        uses: anttiharju/actions/compare-lefthook-glob@c438e97d73d750c3fc202d1342eb1b27aad17dd8
        with:
          changes: ${{ steps.changes.outputs.array }}
          yq: '.pre-commit.jobs[] | select(.name == "actionlint") | .glob'

      - if: steps.workflows.outputs.changed == 'true'
        name: Echo true
        shell: sh
        run: |
          echo ${{ steps.workflows.outputs.changed }}
```
