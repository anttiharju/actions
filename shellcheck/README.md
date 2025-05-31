# Run ShellCheck

Runs & caches https://github.com/koalaman/shellcheck

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

      - name: ShellCheck
        uses: anttiharju/actions/shellcheck@v0
```
