# Lint Actions

This composite action lints GitHub Actions with two tools by doing the following:
1. Downloads 1) [mpalmer/action-validator](https://github.com/mpalmer/action-validator) with [asdf](https://github.com/asdf-vm/asdf)
2. Finds GitHub Actions -related .yml files
3. Feeds them to action-validator
4. Runs a different tool, 2) [rhysd/actionlint](https://github.com/rhysd/actionlint) in the checked out repository.
