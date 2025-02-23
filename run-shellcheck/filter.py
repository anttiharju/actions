#!/usr/bin/env python3

import sys

def is_shell_script(file_info):
    lower_info = file_info.lower()
    return any(shell_indicator in lower_info for shell_indicator in [
        'shell script',
        '/bin/sh',
        '/bin/bash',
        'bourne',
        '/usr/bin/env sh'
    ])

def main():
    for line in sys.stdin:
        parts = line.strip().split(':', 1)
        if len(parts) != 2:
            continue
            
        filename, file_type = parts

        # Only output shell scripts
        if is_shell_script(file_type):
            print(filename)

if __name__ == '__main__':
    main()
