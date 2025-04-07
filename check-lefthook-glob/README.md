# Check changes

[![check-lefthook-glob](https://github.com/anttiharju/actions/actions/workflows/check-lefthook-glob.yml/badge.svg)](https://github.com/anttiharju/actions/actions/workflows/check-lefthook-glob.yml)

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
        uses: anttiharju/actions/find-changes@c438e97d73d750c3fc202d1342eb1b27aad17dd8

      - name: Check changes
        id: workflows
        uses: anttiharju/actions/check-lefthook-glob@c438e97d73d750c3fc202d1342eb1b27aad17dd8
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
