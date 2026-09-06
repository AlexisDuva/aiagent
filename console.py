"""Terminal output helpers.

`info` is essential, user-facing output and always prints.
`detail` is diagnostic output and prints only when verbose mode is on.

Call `set_verbose` once at startup; the module keeps the flag so callers
never have to thread `args.verbose` around or repeat `if args.verbose`.
"""

_verbose = False


def set_verbose(value: bool) -> None:
    global _verbose
    _verbose = value


def is_verbose() -> bool:
    return _verbose


def info(message: str = "") -> None:
    print(message)


def detail(message: str = "") -> None:
    if _verbose:
        print(message)
