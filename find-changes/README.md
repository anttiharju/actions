# Find changes

This action outputs list of changed files as JSON. It works in `pull_request`, `merge_group`, and `push` events, supporting all merge types: `merge commit`, `squash`, and `rebase`.

If you use this, you should have either [merge queues](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) or `Require branches to be up to date before merging` branch protection rule enabled.

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
        uses: anttiharju/actions/find-changes@d3cf964588f604b270572f63188ded03d96eed99

      - name: Echo changed files
        shell: sh
        run: |
          echo ${{ steps.changed.outputs.files }}
```

```json
["foo/bar", "baz"]
```
