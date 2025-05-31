# check-relative-markdown links

Runs https://github.com/anttiharju/check-relative-markdown-links

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

      - name: actionlint
        uses: anttiharju/actions/check-relative-markdown-links@v0
```
