# Run ShellCheck

Finds POSIX/sh and Bash scripts tracked by Git and runs `shellcheck -x` on them. Also prints out shellcheck version so upon discrepancies people can check whether their local version matches CI.

This action tries to be as generic as possible. To support that goal, tests were written for it. If you encounter cases where it incorrectly detects some files as ShellCheckable scripts, please provide an example file under testdata in a PR.
