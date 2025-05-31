# Rubocop file

Runs & caches https://github.com/rubocop/rubocop on the specified file.

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

      - uses: anttiharju/actions/rubocop-file@v0
        with:
          file: "Formula/app.rb"
```
