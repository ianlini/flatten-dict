from typing import Callable, Tuple, TypeVar, Optional, Union

T = TypeVar("T")


def tuple_reducer(k1: Optional[Tuple[T, ...]], k2: T) -> Tuple[T, ...]:
    if k1 is None:
        return (k2,)
    else:
        return k1 + (k2,)


def path_reducer(k1: Optional[str], k2: Union[str, int]) -> str:
    import os.path

    if k1 is None:
        return str(k2)
    else:
        return os.path.join(k1, str(k2))


def dot_reducer(
    k1: Optional[Union[T, str, int]], k2: Union[T, int]
) -> Union[T, str, int]:
    if k1 is None:
        return k2
    else:
        return "{}.{}".format(k1, k2)


def underscore_reducer(
    k1: Optional[Union[T, str, int]], k2: Union[T, int]
) -> Union[T, str, int]:
    if k1 is None:
        return k2
    else:
        return "{}_{}".format(k1, k2)


def make_reducer(
    delimiter: str,
) -> Callable[[Union[T, str, int, None], Union[T, str, int]], Union[T, str, int]]:
    """Create a reducer with a custom delimiter.

    Parameters
    ----------
    delimiter : str
        Delimiter to use to join keys.

    Returns
    -------
    f : Callable
        Callable that can be passed to `flatten()`'s `reducer` argument.
    """

    def f(
        k1: Optional[Union[T, str, int]], k2: Union[T, str, int]
    ) -> Union[T, str, int]:
        if k1 is None:
            return k2
        else:
            return "{}{}{}".format(k1, delimiter, k2)

    return f
