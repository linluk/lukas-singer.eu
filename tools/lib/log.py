#!/usr/bin/env python3

"""
    some simple logging, simply log to stdout and stderr.
"""

import sys

LOG_DEBUG = False
LOG_INFO = LOG_DEBUG or True
LOG_WARNING = LOG_INFO or True


def message_builder(message: str, *args, **kwargs) -> str:
    return (f'{message}'
            f'{", " if args else ""}{", ".join(map(str, args))}'
            f'{", " if args else ""}'
            f'{", ".join(f"{k}: {v}" for k, v in kwargs.items()) if kwargs is not None else ""}')  # noqa E501


def error(code: int | None, message: str, *args, **kwargs) -> None:
    print(f'[ERROR] {message_builder(message, *args, **kwargs)}',
          file=sys.stderr)
    if code is not None:
        exit(code)


def debug(message: str, *args, **kwargs) -> None:
    if LOG_DEBUG:
        print(f'[DEBUG] {message_builder(message, *args, **kwargs)}')


def info(message: str, *args, **kwargs) -> None:
    if LOG_INFO:
        print(f'[INFO] {message_builder(message, *args, **kwargs)}')


def warning(message: str, *args, **kwargs) -> None:
    if LOG_WARNING:
        print(f'[WARNING] {message_builder(message, *args, **kwargs)}')
