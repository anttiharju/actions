# Find changes

This action outputs list of changed files as JSON. It works in `pull_request`, `merge_group`, and `push` events, supporting all merge types: `merge commit`, `squash`, and `rebase`.

## Usage example

```yml
test:
  name: Test
  runs-on: ubuntu-24.04
  steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Find changes
      id: changed
      uses: anttiharju/actions/find-changes@77ee8c08cd2350d5935d1b5dd2575c535456dc64

    - name: Echo changed files
      shell: sh
      run: |
        echo ${{ steps.changed.outputs.files }}
```
