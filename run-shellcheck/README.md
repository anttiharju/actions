# Check ShellCheck

[![check-shellcheck](https://github.com/anttiharju/actions/actions/workflows/check-shellcheck.yml/badge.svg)](https://github.com/anttiharju/actions/actions/workflows/check-shellcheck.yml)

Finds POSIX/sh and Bash scripts tracked by Git and runs `shellcheck --color=always --external-sources` on them. Also prints out shellcheck version so upon discrepancies people can check whether their local version matches CI, although this latter point is not expected to be an issue.

The action tries to remain as generic as possible. As an example, it can be used in repositories with Python scripts to ShellCheck just the shell scripts. This goal is supported by an integration test and an unit test. The tests can be ran with

```sh
./check-shellcheck/test.py # from Git repository root
```

If you encounter cases where some files are incorrectly detected as ShellCheckable scripts, please open a PR with an example incorrectly detected file under [`testdata/`](./testdata/)

## Usage example

```yml
on:
  pull_request:

jobs:
  validate:
    name: Validate
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: ShellCheck
        uses: anttiharju/actions/check-shellcheck@9e42dc22a4d9352ed4452b3a1c259bc4bdc17778
```

## macOS and Ubuntu 24.04 compatibility

[`filter.py`](./filter.py) supports both macOS and Ubuntu 24.04. Some incompatibilities were faced due to differing `xargs -0 file` output. The need to support both arose from:

1. The author develops on a Macbook
2. ubuntu-24.04 is author's preferred GitHub Actions runner

Incompatibilities can be debugged with the following command

```sh
find check-shellcheck/testdata -type f -print0 | xargs -0 file
```

> Highlighting has been used below to emphasise the files that should be ShellChecked

Command output from ubuntu-24.04 has been highlighted with green

```diff
 check-shellcheck/testdata/usrbinenvpython:  Python script, ASCII text executable
+check-shellcheck/testdata/binbash:          Bourne-Again shell script, ASCII text executable
 check-shellcheck/testdata/binpython:        a /bin/python script, ASCII text executable
+check-shellcheck/testdata/usrbinenvsh:      a sh script, ASCII text executable
+check-shellcheck/testdata/usrbinenvbash:    Bourne-Again shell script, ASCII text executable
+check-shellcheck/testdata/binsh:            POSIX shell script, ASCII text executable
 check-shellcheck/testdata/binpython3:       a /bin/python3 script, ASCII text executable
 check-shellcheck/testdata/usrbinenvpython3: Python script, ASCII text executable
```

and from macOS 15.3.1 with red

```diff
 check-shellcheck/testdata/binpython:        a /bin/python script text executable, ASCII text
 check-shellcheck/testdata/usrbinenvpython3: Python script text executable, ASCII text
-check-shellcheck/testdata/binsh:            POSIX shell script text executable, ASCII text
-check-shellcheck/testdata/usrbinenvbash:    Bourne-Again shell script text executable, ASCII text
-check-shellcheck/testdata/usrbinenvsh:      a /usr/bin/env sh script text executable, ASCII text
-check-shellcheck/testdata/binbash:          Bourne-Again shell script text executable, ASCII text
 check-shellcheck/testdata/usrbinenvpython:  Python script text executable, ASCII text
 check-shellcheck/testdata/binpython3:       a /bin/python3 script text executable, ASCII text
```

The differences are easier to see when the highlighted portions are cuddled

```diff
-check-shellcheck/testdata/binsh:            POSIX shell script text executable, ASCII text
+check-shellcheck/testdata/binsh:            POSIX shell script, ASCII text executable
-check-shellcheck/testdata/usrbinenvsh:      a /usr/bin/env sh script text executable, ASCII text
+check-shellcheck/testdata/usrbinenvsh:      a sh script, ASCII text executable
-check-shellcheck/testdata/binbash:          Bourne-Again shell script text executable, ASCII text
+check-shellcheck/testdata/binbash:          Bourne-Again shell script, ASCII text executable
-check-shellcheck/testdata/usrbinenvbash:    Bourne-Again shell script text executable, ASCII text
+check-shellcheck/testdata/usrbinenvbash:    Bourne-Again shell script, ASCII text executable
```

Based on the above [`filter.py`](./filter.py) detects a file as ShellCheckable if `xargs -0 file` output matches any of the following lines

```
POSIX shell script
sh script text executable
sh script, ASCII text executable
Bourne-Again shell script
```
