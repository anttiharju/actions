# Find changes

[![find-changes](https://github.com/anttiharju/actions/actions/workflows/find-changes.yml/badge.svg)](https://github.com/anttiharju/actions/actions/workflows/find-changes.yml)

This action outputs list of changed files as JSON. It works in `pull_request`, `merge_group`, and `push` events, supporting all merge types: `merge commit`, `squash`, and `rebase`.

If you use this, you should have either [merge queues](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) (GitHub Enterprise feature) or `Require branches to be up to date before merging` branch protection rule enabled.

Combine the use of this action with its sibling [check-changes](../check-changes) to run following CI jobs conditionally.

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

      - name: Echo changed files
        shell: sh
        run: |
          echo ${{ steps.changed.outputs.files }}
```

```json
["foo/bar", "baz"]
```
