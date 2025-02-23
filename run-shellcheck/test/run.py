#!/usr/bin/env python3

# Actual action command
# git ls-files -z | xargs -0 file | grep "script text executable" | cut -d: -f1 | xargs shellcheck -x
# we want to mimick git ls-files with data/got.txt
# and test the grep command to see if we end up with data/want.txt
# do not actually run shellcheck or cut
