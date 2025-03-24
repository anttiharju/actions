#!/bin/sh

xargs -0 file | grep -i -E "POSIX shell script|sh script text executable|sh script, ASCII text executable|Bourne-Again shell script" | cut -d: -f1
