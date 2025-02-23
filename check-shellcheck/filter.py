#!/usr/bin/env python3

import sys


def is_shell_script(file_info):
    return any(
        shell_indicator.lower() in file_info.lower()
        for shell_indicator in [
            "POSIX shell script",
            "sh script text executable",
            "sh script, ASCII text executable",
            "Bourne-Again shell script",
        ]
    )


def main():
    for line in sys.stdin:
        parts = line.strip().split(":", 1)
        if len(parts) != 2:
            continue

        filename, file_type = parts

        if is_shell_script(file_type):
            print(filename)


if __name__ == "__main__":
    main()
