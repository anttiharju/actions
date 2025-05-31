# Prettier

Runs Prettier in check mode to ensure everything that can be compliant with Prettier, is compliant.

By default checks all files, but globs, for example `{*.yml,*.md}` can be provided via the patterns input.

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
        uses: actions/checkout@v4

      - name: Prettier
        uses: anttiharju/actions/prettier@v0
        with:
          patterns: "{*.yml,*.md}"
```
