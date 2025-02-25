#!/usr/bin/env python3

import os
import subprocess
import pathlib
from typing import Set

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()


def filter() -> Set[str]:
    """Execute the shell command and return output as set of lines."""
    os.chdir(SCRIPT_DIR / "testdata")
    try:
        find_process = subprocess.Popen(
            ["find", ".", "-type", "f", "-print0"], stdout=subprocess.PIPE
        )

        xargs_process = subprocess.Popen(
            ["xargs", "-0", "file"], stdin=find_process.stdout, stdout=subprocess.PIPE
        )

        filter_process = subprocess.Popen(
            [str(SCRIPT_DIR / "filter.py")],
            stdin=xargs_process.stdout,
            stdout=subprocess.PIPE,
            text=True,
        )

        output = filter_process.communicate()[0]
    finally:
        os.chdir(SCRIPT_DIR)

    return {line.strip() for line in output.splitlines() if line.strip()}


def unit_test() -> bool:
    """Run unit test and return True if test passes."""
    want = {
        "./binsh",
        "./usrbinenvsh",
        "./binbash",
        "./usrbinenvbash",
    }

    got = set(filter())

    if not got == want:
        print("❌ Unit test failed!")
        print("Got:    ", sorted(got))
        print("Want:   ", sorted(want))
        print("Missing:", sorted(got - want))
        print("Extra:  ", sorted(want - got))
        return False
    else:
        print("✅ Unit test passed!")
        return True


def integration_test() -> bool:
    """Run integration test and return True if ShellCheck passes."""
    try:
        files = filter()
        if not files:
            print("❌ Integration test failed! No files found to check")
            return False

        os.chdir(SCRIPT_DIR / "testdata")
        try:
            shellcheck_process = subprocess.run(
                ["shellcheck", "-x"] + list(files), capture_output=True, text=True
            )
        finally:
            os.chdir(SCRIPT_DIR)

        if shellcheck_process.returncode == 0:
            print("✅ Integration test passed!")
            return True

        print("❌ Integration test failed! ShellCheck output:")
        print(shellcheck_process.stderr)
        return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Integration test failed! Error running ShellCheck: {e}")
        print(e.stderr)
        return False


def run_tests():
    """Run all tests and exit with appropriate status code."""
    integration_result = integration_test()
    unit_result = unit_test()

    if not integration_result or not unit_result:
        exit(1)
    exit(0)


if __name__ == "__main__":
    run_tests()
