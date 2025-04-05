#!/bin/sh

shellcheck --version
git ls-files -z '*.sh' '*.bash' '*.dash' '*.ksh' | xargs -0 shellcheck --color=always --source-path=SCRIPTDIR
