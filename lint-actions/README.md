# Lint GitHub Actions

This composite action does the following things:
1. Downloads [mpalmer/action-validator](https://github.com/mpalmer/action-validator) with [asdf](https://github.com/asdf-vm/asdf)
2. Finds GitHub Actions -related .yml files
3. Feeds them to action-validator
4. Runs a different tool, [rhysd/actionlint](https://github.com/rhysd/actionlint), in the checked out repository.
5. Checks all `.yml` or `.yaml` files under .github are compliant with prettier. 
