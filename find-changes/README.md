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
      uses: anttiharju/actions/find-changes@eb5c0d6d0e5dbfd48be43731574514ab737ac628

    - name: Echo changed files
      shell: sh
      run: |
        echo ${{ steps.changed.outputs.files }}
```
