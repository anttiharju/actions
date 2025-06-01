# relcheck

Runs https://github.com/anttiharju/relcheck

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

      - name: relcheck
        uses: anttiharju/actions/relcheck@v0
```
