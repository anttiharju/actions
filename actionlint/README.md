# actionlint

Runs & caches https://github.com/rhysd/actionlint

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
        uses: anttiharju/actions/actionlint@v0
```
