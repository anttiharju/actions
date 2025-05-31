# action-validator

Runs & caches https://github.com/mpalmer/action-validator

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

      - name: action-validator
        uses: anttiharju/actions/action-validator@v0
```
