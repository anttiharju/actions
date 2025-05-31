# Editorconfig-Checker

Runs https://github.com/editorconfig-checker/editorconfig-checker on files tracked by Git.

## Example

```yml
name: Validate
on:
  pull_request:

jobs:
  validate:
    name: Validate
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout
        uses: actions/checkout

        name: EditorConfig-Checker
        uses: anttiharju/actions/editorconfig-checker@v1
```
