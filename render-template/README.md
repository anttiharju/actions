# Render template

[![tests](https://github.com/anttiharju/actions/actions/workflows/render-template.yml/badge.svg)](https://github.com/anttiharju/actions/actions/workflows/render-template.yml)

Templates a file using `envsubst` using three inputs:

1. `template`  
   Any file with templatable values such as `$value` or `${value}`
2. `values`  
   A script that outputs the necessary templatable values to environment.
3. `output`  
   Path for the final rendered template.

Additionally `working-directory` can be specified to avoid unnecessary repetition.

Usage example can be found [here](../.github/workflows/render-template.yml)
