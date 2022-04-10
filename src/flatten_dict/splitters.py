from typing import Tuple, Callable, TypeVar, Hashable
import sys

THashable = TypeVar("THashable", bound=Hashable)


def tuple_splitter(flat_key):
    # type: (Tuple[THashable, ...]) -> Tuple[THashable, ...]
    return flat_key


def path_splitter(flat_key):
    # type: (str) -> Tuple[str, ...]
    if sys.version_info >= (3, 4):
        from pathlib import PurePath
    else:
        from pathlib2 import PurePath
    keys = PurePath(flat_key).parts
    return keys


def dot_splitter(flat_key):
    # type: (str) -> Tuple[str, ...]
    keys = tuple(flat_key.split("."))
    return keys


def underscore_splitter(flat_key):
    # type: (str) -> Tuple[str, ...]
    keys = tuple(flat_key.split("_"))
    return keys


def make_splitter(delimiter):
    # type: (str) -> Callable[[str], Tuple[str, ...]]
    """Create a reducer with a custom delimiter.

    Parameters
    ----------
    delimiter : str
        Delimiter to use to split keys.

    Returns
    -------
    f : Callable
        Callable that can be passed to ``unflatten``'s ``splitter`` argument.
    """

    def f(flat_key):
        keys = tuple(flat_key.split(delimiter))
        return keys

    return f
