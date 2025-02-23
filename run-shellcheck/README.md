# Run ShellCheck

Finds POSIX/sh and Bash scripts tracked by Git and runs `shellcheck --color=always --external-sources` on them. Also prints out shellcheck version so upon discrepancies people can check whether their local version matches CI, although this latter point is not expected to be an issue.

The action tries to remain as generic as possible. As an example, it can be used in repositories with Python scripts to ShellCheck just the shell scripts. This goal is supported by an integration test and an unit test. The tests can be ran with

```sh
./run-shellcheck/test.py # from Git repository root
```

If you encounter cases where some files are incorrectly detected as ShellCheckable scripts, please open a PR with an example incorrectly detected file under [`testdata/`](./testdata/)

## macOS and Ubuntu 24.04 compatibility

[`filter.py`](./filter.py) supports both macOS and Ubuntu 24.04. Some incompatibilities were faced due to differing `xargs -0 file` output. The need to support both arose from:

1. @anttiharju develops on a Macbook
2. @anttiharju uses ubuntu-24.04 as the preferred GitHub Actions runner

Incompatibilities can be debugged with the following command

```sh
find run-shellcheck/testdata -type f -print0 | xargs -0 file
```

> Highlighting has been used below to emphasise the files that should be ShellChecked.

Command output on ubuntu-24.04 has been highlighted with green:

```diff
 run-shellcheck/testdata/usrbinenvpython:  Python script, ASCII text executable
+run-shellcheck/testdata/binbash:          Bourne-Again shell script, ASCII text executable
 run-shellcheck/testdata/binpython:        a /bin/python script, ASCII text executable
+run-shellcheck/testdata/usrbinenvsh:      a sh script, ASCII text executable
+run-shellcheck/testdata/usrbinenvbash:    Bourne-Again shell script, ASCII text executable
+run-shellcheck/testdata/binsh:            POSIX shell script, ASCII text executable
 run-shellcheck/testdata/binpython3:       a /bin/python3 script, ASCII text executable
 run-shellcheck/testdata/usrbinenvpython3: Python script, ASCII text executable
```

and macOS 15.3.1 output with red:

```diff
 run-shellcheck/testdata/binpython:        a /bin/python script text executable, ASCII text
 run-shellcheck/testdata/usrbinenvpython3: Python script text executable, ASCII text
-run-shellcheck/testdata/binsh:            POSIX shell script text executable, ASCII text
-run-shellcheck/testdata/usrbinenvbash:    Bourne-Again shell script text executable, ASCII text
-run-shellcheck/testdata/usrbinenvsh:      a /usr/bin/env sh script text executable, ASCII text
-run-shellcheck/testdata/binbash:          Bourne-Again shell script text executable, ASCII text
 run-shellcheck/testdata/usrbinenvpython:  Python script text executable, ASCII text
 run-shellcheck/testdata/binpython3:       a /bin/python3 script text executable, ASCII text
```

The differences are bit easier to see when the highlighted bits are put together:

```diff
-run-shellcheck/testdata/binsh:            POSIX shell script text executable, ASCII text
+run-shellcheck/testdata/binsh:            POSIX shell script, ASCII text executable
-run-shellcheck/testdata/usrbinenvsh:      a /usr/bin/env sh script text executable, ASCII text
+run-shellcheck/testdata/usrbinenvsh:      a sh script, ASCII text executable
-run-shellcheck/testdata/binbash:          Bourne-Again shell script text executable, ASCII text
+run-shellcheck/testdata/binbash:          Bourne-Again shell script, ASCII text executable
-run-shellcheck/testdata/usrbinenvbash:    Bourne-Again shell script text executable, ASCII text
+run-shellcheck/testdata/usrbinenvbash:    Bourne-Again shell script, ASCII text executable
```

Based on the above, [`filter.py`](./filter.py) decides that a file is to be ShellChecked, if an output line matches any of the following:

- `Bourne-Again shell script`
- `POSIX shell script`
- `sh script text executable`
- `sh script, ASCII text executable`
