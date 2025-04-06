# Find changes (WIP)

Whole point is Lefthook integration (in a generic manner) - monorepos are out of scope, but nice if they can be easily supported

**DISREGARD ALL BELOW**

[![find-changes](https://github.com/anttiharju/actions/actions/workflows/find-changes.yml/badge.svg)](https://github.com/anttiharju/actions/actions/workflows/find-changes.yml)

Find changes is an action to enable conditional runs of CI jobs based on what files changes have occurred within a PR or a merge.

Usage: either with merge queues or 'Require branches to be up to date before merging' branch protection.

Runner type: one with python3.12 or newer (ubuntu-24.04)

## Why

While GitHub Actions has the default `paths:` filter, I've yet find a way to do some of the following things with it:

- Have jobs run conditionally but still wait for all CI to complete before satisfying branch protection rules
- Enforce a certain order within conditional CI jobs, for example building the latest version of a container if the container definition has changed to have it immediately available for later jobs

Running jobs conditionally based on changes speeds up CI significantly for most use. For example think about running a heavy test suite just because you updated documentation or updated a part of the program that has nothing to do with said changes.

## Usage

### Matrix strategy (monorepos)

This way is very dynamic and any new "projects" added will automatically get ran in the existing CI. Requires standardisation.

```yml
jobs:
  find-changed:
    name: Find changed projects
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4 # might be optional (use api?) let's see
      - uses: anttiharju/actions/find-changes@v0
        id: find
        with:
          regex: "TBD"
          match_all_regex: "TBD" # optional
          exclude-regex: "TBD" # exclude for example sample apps that are not meant to have CI ran on them
    outputs:
      projects: ${{ steps.find.outputs.changes }}

  build-projects:
    needs: find-changes
    if: ${{ needs.find-changed.outputs.projects != '[]' }}
    strategy:
      matrix:
        project: ${{ fromJSON(needs.find-changed.outputs.projects) }}
    name: ${{ matrix.project.name || 'Build' }}
    uses: ./.github/workflows/reusable-project-build.yml
    with:
      name: ${{ matrix.project.name }}
      path: ${{ matrix.project.path }}

  finish-ci: # base your branch protection rules on this job
    name: "Finish CI"
    runs-on: ubuntu-24.04
    needs: build-projects
    steps:
      run: |
        echo "success"
```

### Conditional jobs

This way produces nicer UI (no skipped jobs etc.) but when adding a new project the CI manifests need to be updated accordingly, although it should be a fairly simple copy-paste. Be aware that there's a limit of 20 references to unique workflows, i.e., a generic workflow can scale without limits, but if you create a new workflow for each project, you have to stay below the 20 workflow limit. Also consider using composite actions to create "workflow" that are defined in the example top-level workflow.

```yml
jobs:
  changed:
    name: Find changed projects
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4 # might be optional (use api?) let's see
      - uses: anttiharju/actions/find-changes@v0
        id: found
        with:
          regex: "TBD"
          match_all_regex: "TBD" # optional
    outputs:
      projects: ${{ steps.found.outputs.changes }}

  specific-app:
    name: Specific app
    needs: changed
    if: |
      always() && !failure() && !cancelled() &&
      contains(fromJSON(needs.changed.outputs.projects).path, 'specific/app')
    uses: ./.github/workflows/specific.app.yml
    with:
      matrix: ${{ needs.changed.outputs.projects }} # you can define matrix strategy inside the reusable workflow and it works nicely with UI
      name: App # or hardcode inputs
      path: specific/app

  finish-ci: # base your branch protection rules on this job
    if: always()
    name: "Finish CI"
    runs-on: ubuntu-24.04
    needs: # list all previous ci jobs
      - changed
      - specific-app
    steps:
      run: |
        if [[ "$cancelled" == 'true' ]]; then
          echo "cancelled"
          exit 1
        fi
        if [[ "$failed" == 'true' ]]; then
          echo "failed"
          exit 1
        fi
        echo "success"
```

### Conditional jobs, chained to the same matrix

Demonstration of chaining multiple uses of this action

```yml
jobs:
  changed:
    name: Find changed projects
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4 # might be optional (use api?) let's see
      - uses: anttiharju/actions/find-changes@v0
        id: found-first
        with:
          regex: "TBD" # specific/app something
          match_all_regex: "TBD" # if changes to ci (.github), insert all regex input matches into output matrix
      - uses: anttiharju/actions/find-changes@v0
        id: found
        with:
          matrix: ${{ steps.found-first.outputs.changes }} # (optional obviously) this just gets appended to
          regex: "TBD" # other-place/app2 something
          match_all_regex: "TBD" # if changes to ci (.github), insert all regex input matches into output matrix
    outputs:
      projects: ${{ steps.found.outputs.changes }} # so we still have flexibility without overcomplicated action inputs/outputs but only one job output

  specific-app:
    name: Specific app
    needs: changed
    if: | # and we can keep using a similar pattern as before
      always() && !failure() && !cancelled() &&
      contains(fromJSON(needs.changed.outputs.projects).path, 'specific/app')
    uses: ./.github/workflows/generic-app.yml
    with:
      matrix: ${{ needs.changed.outputs.projects }} # you can define matrix strategy inside the reusable workflow and it works nicely with UI
      name: App # or hardcode inputs
      path: specific/app

  specific-app-2:
    name: Specific app 2
    needs: changed
    if: |
      always() && !failure() && !cancelled() &&
      contains(fromJSON(needs.changed.outputs.projects).path, 'other-place/app2')
    uses: ./.github/workflows/generic-app.yml
    with:
      matrix: ${{ needs.changed.outputs.projects }} # you can define matrix strategy inside the reusable workflow and it works nicely with UI
      name: App 2 # or hardcode inputs
      path: specific/app2

  # todo: composite action for this that also does validations such as 'are all previous ci jobs listed as needs' for safety
  finish-ci: # base your branch protection rules on this job
    if: always()
    name: "Finish CI"
    runs-on: ubuntu-24.04
    needs: # list all previous ci jobs
      - changed
      - specific-app
      - specific-app-2
    steps:
      name: Check workflow status
      env:
        cancelled: ${{ contains(needs.*.result, 'cancelled') }}
        failure: ${{ contains(needs.*.result, 'failure') }}
      run: |
        if [[ "$cancelled" == 'true' ]]; then
          echo "cancelled"
          exit 1
        fi
        if [[ "$failure" == 'true' ]]; then
          echo "failure"
          exit 1
        fi
        echo "success"
```
