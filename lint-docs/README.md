# Lint docs

This action setups mkdocs via pip and builds documentation in strict mode. Strict mode is helpful for catching broken file references, such as links to websites or images.

## Usage example

```yml
validate:
  runs-on: ubuntu-24.04
  steps:
    - name: Checkout
      uses: actions/checkout@v4
    - name: Docs
      uses: anttiharju/actions/validate-docs@v0
```
