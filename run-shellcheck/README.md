# Run ShellCheck

Finds POSIX/sh and Bash scripts tracked by Git and runs `shellcheck -x` on them. Also prints out shellcheck version so upon discrepancies people can check whether their local version matches CI.

This action tries to be as generic as possible. To support that goal, tests were written for it. If you encounter cases where it incorrectly detects some files as ShellCheckable scripts, please provide an example file under testdata in a PR.

## macOS and Ubuntu 24.04 compatibility

The filter.py detection mechanism has been carefully crafted to support both operating systems for two reasons:

1. Antti uses a Macbook to develop
2. Antti assumes this action will be ran on the ubuntu-24.04 runner

The incompatibilities in the two OSs arise from differing `xargs` output. The output can be inspected with the following command.

```sh
find run-shellcheck/testdata -type f -print0 | xargs -0 file
```

On ubuntu-24.04 GitHub Actions runner it produces the following output.

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

Diff syntax is used to highlight what filter.py should pick out.

On macOS 15.3.1 it produces

```diff
run-shellcheck/testdata/binpython:        a /bin/python script text executable, ASCII text
run-shellcheck/testdata/usrbinenvpython3: Python script text executable, ASCII text
+run-shellcheck/testdata/binsh:            POSIX shell script text executable, ASCII text
+run-shellcheck/testdata/usrbinenvbash:    Bourne-Again shell script text executable, ASCII text
+run-shellcheck/testdata/usrbinenvsh:      a /usr/bin/env sh script text executable, ASCII text
+run-shellcheck/testdata/binbash:          Bourne-Again shell script text executable, ASCII text
run-shellcheck/testdata/usrbinenvpython:  Python script text executable, ASCII text
run-shellcheck/testdata/binpython3:       a /bin/python3 script text executable, ASCII text
```

To be more specific, here's the diff between the files that this action wants to validate with ShellCheck (macOS with red):

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
