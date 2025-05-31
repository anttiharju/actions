# MkDocs GitHub Deploy

This actions setups MkDocs via pip and runs `mkdocs gh-deploy --force --no-history` which deploys pushes built documentation site to branch `gh-pages`. The actions needs to run in a checked out git repository that has a token with enough permissions, read more [here](https://github.com/peter-evans/create-pull-request/blob/main/docs/concepts-guidelines.md#authenticating-with-github-app-generated-tokens).

The action can optionally be provided a committer. By default it uses `github-actions[bot]` but you may desire to use the name of your GitHub App to match what GitHub UI shows in the branches view.

Recommended trigger event is push to the default branch. In that case, you may wish to run [mkdocs-build-strict](../mkdocs-build-strict/) on pull request events to catch mistakes early.

## Example

```yml
name: Documentation
on:
  workflow_call:
    secrets:
      ANTTIHARJU_BOT_ID:
        required: true
      ANTTIHARJU_BOT_PRIVATE_KEY:
        required: true

jobs:
  website:
    name: Website
    runs-on: ubuntu-24.04
    permissions:
      contents: write
    steps:
      - name: Generate deploy token
        id: deploy
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ secrets.ANTTIHARJU_BOT_ID }}
          private-key: ${{ secrets.ANTTIHARJU_BOT_PRIVATE_KEY }}
      - name: Checkout
        uses: actions/checkout@v4
        with:
          token: ${{ steps.deploy.outputs.token }}
      - name: Deploy to GitHub Pages
        uses: anttiharju/actions/mkdocs-gh-deploy@v1
```
