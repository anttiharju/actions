# Run ShellCheck

Runs ShellCheck for all _.sh and _.bash files.

Previous iteration of this action used `file` to detect ShellCheck-able scripts, but that approach is untenable in large repositories. The approach is also fundamentally incompatible with Lefthook globs for partial checks.
