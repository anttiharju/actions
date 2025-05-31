# Go build

Setups Go and runs `go build`. `go test` can be run in steps that follow separately.

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
      - name: go build
        uses: anttiharju/actions/go-build@v1

      - name: go test
        shell: sh
        run: |
          go test ./...
```
