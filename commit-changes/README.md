# Commit changes

Commits all changes as `github-actions[bot]` and uses [`github.actor`](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs#github-context) as commit author to leave a record of automation origin.

Also has an output changes so following steps can be ran conditionally based on the output of this step.

Confirmed to work on the following events

- [`workflow_dispatch`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_dispatch)
