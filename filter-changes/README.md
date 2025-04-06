# Filter changes

This is a sibling action to [find changes](../find-changes/), enabling useful functionality while maintaining separation of concerns.

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

      - name: Filter changes
        id: workflows
        uses: ./filter-changes # under development
        with:
          changes: ${{ steps.changed.outputs.files }}
          file: lefthook.yml
          yq: '.pre-commit.jobs[] | select(.name == "actionlint") | .glob'
          # .github/workflows/*.yml

      - name: Echo changed files
        shell: sh
        run: |
          echo ${{ steps.workflows.outputs.have_changed }}
        # true or false
```

```json
true
```
