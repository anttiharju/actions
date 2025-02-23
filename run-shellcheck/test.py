#!/usr/bin/env python3

import sys
import re

def read_file(filename):
    """Read file contents and return as list of lines."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def filter_shell_scripts(lines):
    """Filter lines to only include shell scripts."""
    shell_pattern = re.compile(r'.*?(shell script|sh script).*?executable')
    return [line for line in lines if shell_pattern.match(line)]

def run_test():
    """Run the test and compare results."""
    all = read_file('testdata/all.txt')
    want = read_file('testdata/expect.txt')
    got = filter_shell_scripts(all)
    
    if got == want:
        print("Test passed! ✅")
        return 0
    else:
        print("Test failed! ❌")
        print("\nGot:")
        for line in got:
            print(f"  {line}")
        print("\nWant:")
        for line in want:
            print(f"  {line}")
        return 1

if __name__ == '__main__':
    sys.exit(run_test())
