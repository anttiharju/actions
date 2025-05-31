# golangci-lint

https://github.com/golangci/golangci-lint-action but supports `version-file:` input, which defaults to `.golangci-version`. Ideal for use with [`vmatch`](https://github.com/anttiharju/vmatch).

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

      - name: golangci-lint
        uses: anttiharju/actions/golangci-lint@v1
```
