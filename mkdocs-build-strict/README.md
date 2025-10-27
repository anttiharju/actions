# MkDocs build strict

This action setups MkDocs via pip and builds documentation in strict mode. Strict mode is helpful for catching broken file references, such as links to websites or images.

## Usage example

```yml
name: Validate
on:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout
        uses: actions/checkout@v5
      - name: MkDocs build strict
        uses: anttiharju/actions/mkdocs-build-strict@v0
```
