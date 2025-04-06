# Filter changes

This is a sibling action to [find changes](../find-changes/). With the two actions combined, following CI jobs or steps can run conditionally based on changes. This enables faster CI as it's cheaper to not run jobs if nothing meaningful to them has changed.

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
        uses: anttiharju/actions/find-changes@23d159effd5d8e7913d4bc8fb7ef704a7dc7dfe2

      - name: Filter changes
        id: workflows
        uses: anttiharju/actions/filter-changes@23d159effd5d8e7913d4bc8fb7ef704a7dc7dfe2
        with:
          changes: ${{ steps.changed.outputs.files }}
          file: lefthook.yml
          yq: '.pre-commit.jobs[] | select(.name == "actionlint") | .glob'

      - if: steps.workflows.outputs.have_changed == 'true'
        name: Echo true
        shell: sh
        run: |
          echo ${{ steps.workflows.outputs.have_changed }}
```
