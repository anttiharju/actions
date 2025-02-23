#!/usr/bin/env python3

import os
import subprocess
from typing import Set

def filter() -> Set[str]:
    """Execute the shell command and return output as set of lines."""
    os.chdir('testdata')
    try:
        find_process = subprocess.Popen(
            ['find', '.', '-type', 'f', '-print0'],
            stdout=subprocess.PIPE
        )
        
        xargs_process = subprocess.Popen(
            ['xargs', '-0', 'file'],
            stdin=find_process.stdout,
            stdout=subprocess.PIPE
        )
        
        filter_process = subprocess.Popen(
            ['../filter.py'],
            stdin=xargs_process.stdout,
            stdout=subprocess.PIPE,
            text=True
        )
        
        output = filter_process.communicate()[0]
    finally:
        os.chdir('..')
    
    return {line.strip() for line in output.splitlines() if line.strip()}

def unit_test() -> bool:
    """Run unit test and return True if test passes."""
    want = {
        './binsh',
        './usrbinenvsh',
        './binbash',
        './usrbinenvbash',
    }
    
    got = set(filter())
    
    if not got == want:
        print("Unit test failed! ❌")
        print("Got:    ", sorted(list(got)))
        print("Want:   ", sorted(list(want)))
        print("Missing:", sorted(list(got - want)))
        return False
    else:
        print("Unit test passed! ✅")
        return True

def run_tests():
    """Run all tests and exit with appropriate status code."""
    # Integration test (will always match testdata)
    #find testdata -type f -print0 | xargs -0 file | ./filter.py | cut -d: -f1 | xargs shellcheck -x

    if not unit_test():
        exit(1)
    exit(0)

if __name__ == "__main__":
    run_tests()