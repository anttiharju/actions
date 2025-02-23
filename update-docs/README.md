# Update docs

This actions setups mkdocs via pip and runs `mkdocs gh-deploy --force --no-history` which deploys pushes built documentation site to branch `gh-pages`. The actions needs to run in a checked out git repository that has a token with enough permissions, read more [here](https://github.com/peter-evans/create-pull-request/blob/main/docs/concepts-guidelines.md#authenticating-with-github-app-generated-tokens).

The action can optionally be provided a committer. By default it uses `github-actions[bot]` but you may desire to use the name of your GitHub App to match what GitHub UI shows in the branches view.

Recommended trigger event is push to the default branch. In that case, you may wish to run [validate-docs](../validate-docs/) on pull request events to catch mistakes early.

## Usage example

```yml
  publish:
    runs-on: ubuntu-24.04
    steps:
      - name: Generate docs token
        uses: actions/create-github-app-token@v1
        id: generate-token
        with:
          app-id: ${{ secrets.YOUR_GITHUB_APP_ID }}
          private-key: ${{ secrets.YOUR_GITHUB_APP_PRIVATE_KEY }}
      - name: Checkout
        uses: actions/checkout@v4
        with:
          token: ${{ steps.generate-token.outputs.token }}
      - name: Publish docs
        uses: ./.github/actions/publish-docs
```
