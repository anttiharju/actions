#!/usr/bin/env python3

import os
from helpers import FormulaConfig, render_formula

config = FormulaConfig(
    template=os.environ["TEMPLATE"],
    app_name=os.environ["APP_NAME"],
    description=os.environ["DESCRIPTION"],
    homepage=os.environ["HOMEPAGE"],
    url=os.environ["URL"],
    go_version=os.environ["GO_VERSION"],
)

render_formula(config)
