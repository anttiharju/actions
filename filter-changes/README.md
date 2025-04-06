# Filter changes

This is a sibling action to [find changes](../find-changes/). With the two actions combined, following CI jobs can run conditionally based on changes.

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
        uses: anttiharju/actions/find-changes@77d35e5fef2de4fe65bc4479b45a6b42ef3ca8f6

      - name: Filter changes
        id: workflows
        uses: anttiharju/actions/filter-changes@77d35e5fef2de4fe65bc4479b45a6b42ef3ca8f6
        with:
          changes: ${{ steps.changed.outputs.files }}
          file: lefthook.yml
          yq: '.pre-commit.jobs[] | select(.name == "actionlint") | .glob'

      - name: Echo boolean
        shell: sh
        run: |
          echo ${{ steps.workflows.outputs.have_changed }}
```
