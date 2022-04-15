import inspect
import sys
from collections.abc import Mapping
from typing import (
    cast,
    Any,
    Callable,
    Dict,
    Hashable,
    Iterable,
    Optional,
    Sequence,
    Union,
    Tuple,
    TypeVar,
    overload,
)
import typing

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal


import six

from .reducers import tuple_reducer, path_reducer, dot_reducer, underscore_reducer
from .splitters import tuple_splitter, path_splitter, dot_splitter, underscore_splitter

TKeyIn = TypeVar("TKeyIn", bound=Hashable, contravariant=True)
TKeyIn2 = TypeVar("TKeyIn2", bound=Hashable)
TKeyOut = TypeVar("TKeyOut", bound=Hashable, covariant=True)

TReducerCallable2Args = Callable[
    [Optional[Union[TKeyIn, TKeyOut]], Union[TKeyIn, int]], TKeyOut
]

TReducerCallable3Args = Callable[
    [
        Optional[Union[TKeyIn, TKeyOut]],
        Union[TKeyIn, int],
        Union[typing.Mapping[TKeyIn, Any], Iterable[Any]],
    ],
    TKeyOut,
]


TReducerCallable = Union[TReducerCallable2Args, TReducerCallable3Args]

TSplitterCallable = Callable[[TKeyIn], Tuple[TKeyOut, ...]]


REDUCER_DICT: Dict[str, TReducerCallable2Args] = {
    "tuple": tuple_reducer,
    "path": path_reducer,
    "dot": dot_reducer,
    "underscore": underscore_reducer,
}

SPLITTER_DICT: Dict[str, TSplitterCallable] = {
    "tuple": tuple_splitter,
    "path": path_splitter,
    "dot": dot_splitter,
    "underscore": underscore_splitter,
}


@overload
def flatten(
    d: typing.Mapping[TKeyIn, Any],
    reducer: Union[
        TReducerCallable2Args[TKeyIn, TKeyOut], TReducerCallable3Args[TKeyIn, TKeyOut]
    ],
    inverse: bool = False,
    max_flatten_depth: Optional[int] = None,
    enumerate_types: Tuple[type, ...] = (),
    keep_empty_types: Tuple[type, ...] = (),
) -> Dict[TKeyOut, Any]:
    pass


@overload
def flatten(
    d: typing.Mapping[TKeyIn, Any],
    reducer: Literal["tuple"] = "tuple",
    inverse: bool = False,
    max_flatten_depth: Optional[int] = None,
    enumerate_types: Tuple[type, ...] = (),
    keep_empty_types: Tuple[type, ...] = (),
) -> Dict[Tuple[Any, ...], Any]:
    pass


@overload
def flatten(
    d: typing.Mapping[TKeyIn, Any],
    reducer: Literal["dot", "path", "underscore"],
    inverse: bool = False,
    max_flatten_depth: Optional[int] = None,
    enumerate_types: Tuple[type, ...] = (),
    keep_empty_types: Tuple[type, ...] = (),
) -> Dict[Union[TKeyIn, str], Any]:
    pass


@overload
def flatten(
    d: typing.Mapping[TKeyIn, Any],
    reducer: str = "tuple",
    inverse: bool = False,
    max_flatten_depth: Optional[int] = None,
    enumerate_types: Tuple[type, ...] = (),
    keep_empty_types: Tuple[type, ...] = (),
) -> Union[Dict[Tuple[Any, ...], Any], Dict[Union[TKeyIn, str], Any]]:
    pass


@overload
def flatten(
    d: Sequence[Any],
    reducer: Union[
        TReducerCallable2Args[TKeyIn, TKeyOut], TReducerCallable3Args[TKeyIn, TKeyOut]
    ],
    inverse: bool = False,
    max_flatten_depth: Optional[int] = None,
    enumerate_types: Tuple[type, ...] = (),
    keep_empty_types: Tuple[type, ...] = (),
) -> Dict[TKeyOut, Any]:
    pass


@overload
def flatten(
    d: Sequence[Any],
    reducer: Literal["tuple"] = "tuple",
    inverse: bool = False,
    max_flatten_depth: Optional[int] = None,
    enumerate_types: Tuple[type, ...] = (),
    keep_empty_types: Tuple[type, ...] = (),
) -> Dict[Tuple[Any, ...], Any]:
    pass


@overload
def flatten(
    d: Sequence[Any],
    reducer: Literal["dot", "path", "underscore"],
    inverse: bool = False,
    max_flatten_depth: Optional[int] = None,
    enumerate_types: Tuple[type, ...] = (),
    keep_empty_types: Tuple[type, ...] = (),
) -> Dict[Union[int, str], Any]:
    pass


@overload
def flatten(
    d: Sequence[Any],
    reducer: str = "tuple",
    inverse: bool = False,
    max_flatten_depth: Optional[int] = None,
    enumerate_types: Tuple[type, ...] = (),
    keep_empty_types: Tuple[type, ...] = (),
) -> Union[Dict[Tuple[Any, ...], Any], Dict[Union[int, str], Any]]:
    pass


def flatten(
    d: Any,
    reducer: Union[
        str,
        TReducerCallable2Args[TKeyIn, TKeyOut],
        TReducerCallable3Args[TKeyIn, TKeyOut],
    ] = "tuple",
    inverse: bool = False,
    max_flatten_depth: Optional[int] = None,
    enumerate_types: Tuple[type, ...] = (),
    keep_empty_types: Tuple[type, ...] = (),
) -> Any:
    """Flatten `Mapping` object.

    Parameters
    ----------
    d : dict-like object
        The dict that will be flattened.
    reducer : {'tuple', 'path', 'underscore', 'dot', Callable}
        The key joining method. If a `Callable` is given, the `Callable` will be
        used to reduce.
        'tuple': The resulting key will be tuple of the original keys.
        'path': Use `os.path.join` to join keys.
        'underscore': Use underscores to join keys.
        'dot': Use dots to join keys.
    inverse : bool
        Whether you want invert the resulting key and value.
    max_flatten_depth : Optional[int]
        Maximum depth to merge.
    enumerate_types : Sequence[type]
        Flatten these types using `enumerate`.
        For example, if we set `enumerate_types` to ``(list,)``,
        `list` indices become keys: ``{'a': ['b', 'c']}`` -> ``{('a', 0): 'b', ('a', 1): 'c'}``.
    keep_empty_types : Sequence[type]
        By default, ``flatten({1: 2, 3: {}})`` will give you ``{(1,): 2}``, that is, the key ``3``
        will disappear.
        This is also applied for the types in `enumerate_types`, that is,
        ``flatten({1: 2, 3: []}, enumerate_types=(list,))`` will give you ``{(1,): 2}``.
        If you want to keep those empty values, you can specify the types in `keep_empty_types`:

        >>> flatten({1: 2, 3: {}}, keep_empty_types=(dict,))
        {(1,): 2, (3,): {}}

    Returns
    -------
    flat_dict : dict
    """
    enumerate_types = tuple(enumerate_types)
    flattenable_types = (Mapping,) + enumerate_types
    if not isinstance(d, flattenable_types):
        raise ValueError(
            "argument type %s is not in the flattenalbe types %s"
            % (type(d), flattenable_types)
        )

    # check max_flatten_depth
    if max_flatten_depth is not None and max_flatten_depth < 1:
        raise ValueError("max_flatten_depth should not be less than 1.")

    reducer = REDUCER_DICT[reducer] if isinstance(reducer, str) else reducer
    _reducer2: Optional[TReducerCallable2Args[TKeyIn, TKeyOut]] = None
    _reducer3: Optional[TReducerCallable3Args[TKeyIn, TKeyOut]] = None
    if len(inspect.signature(reducer).parameters) == 3:
        _reducer3 = cast(TReducerCallable3Args[TKeyIn, TKeyOut], reducer)
    else:
        _reducer2 = cast(TReducerCallable2Args[TKeyIn, TKeyOut], reducer)

    flat_dict = {}

    def _flatten(
        _d: Union[
            typing.Mapping[TKeyIn, Any], Any
        ],  # either mapping or one of enumerate_types
        depth: int,
        parent: TKeyOut = None,
    ) -> bool:
        key_value_iterable: Iterable[Tuple[Union[int, TKeyIn], Any]] = (
            enumerate(_d) if isinstance(_d, enumerate_types) else _d.items()
        )
        has_item = False
        for key, value in key_value_iterable:
            has_item = True
            if _reducer3 is not None:
                flat_key = _reducer3(parent, key, _d)
            elif _reducer2 is not None:
                flat_key = _reducer2(parent, key)

            if isinstance(value, flattenable_types) and (
                max_flatten_depth is None or depth < max_flatten_depth
            ):
                # recursively build the result
                has_child = _flatten(value, depth=depth + 1, parent=flat_key)
                if has_child or not isinstance(value, keep_empty_types):
                    # ignore the key in this level because it already has child key
                    # or its value is empty
                    continue

            # add an item to the result
            if inverse:
                flat_key, value = value, flat_key
            if flat_key in flat_dict:
                raise ValueError("duplicated key '{}'".format(flat_key))
            flat_dict[flat_key] = value

        return has_item

    _flatten(d, depth=1)
    return flat_dict


def nested_set_dict(d: Dict[TKeyIn, Any], keys: Sequence[TKeyIn], value: Any) -> None:
    """Set a value to a sequence of nested keys.

    Parameters
    ----------
    d : Mapping
    keys : Sequence[str]
    value : Any
    """
    assert keys
    key = keys[0]
    if len(keys) == 1:
        if key in d:
            raise ValueError("duplicated key '{}'".format(key))
        d[key] = value
        return
    d = d.setdefault(key, {})
    nested_set_dict(d, keys[1:], value)


@overload
def unflatten(
    d: typing.Mapping[str, Any],
    splitter: Literal["dot", "underscore", "path"],
    inverse: bool = False,
) -> Dict[str, Any]:
    pass


@overload
def unflatten(
    d: typing.Mapping[Tuple[TKeyIn, ...], Any],
    splitter: Literal["tuple"] = "tuple",
    inverse: bool = False,
) -> Dict[TKeyIn, Any]:
    pass


@overload
def unflatten(
    d: Union[typing.Mapping[str, Any], typing.Mapping[Tuple[TKeyIn, ...], Any]],
    splitter: str = "tuple",
    inverse: bool = False,
) -> Union[Dict[str, Any], Dict[TKeyIn, Any]]:
    pass


@overload
def unflatten(
    d: typing.Mapping[TKeyIn, Any],
    splitter: Callable[[TKeyIn], Tuple[TKeyOut, ...]],
    inverse: bool = False,
) -> Dict[TKeyOut, Any]:
    pass


def unflatten(d: Any, splitter: Any = "tuple", inverse: bool = False) -> Dict[Any, Any]:
    """Unflatten dict-like object.

    Parameters
    ----------
    d : dict-like object
        The dict that will be unflattened.
    splitter : {'tuple', 'path', 'underscore', 'dot', Callable}
        The key splitting method. If a Callable is given, the Callable will be
        used to split `d`.
        'tuple': Use each element in the tuple key as the key of the unflattened dict.
        'path': Use `pathlib.Path.parts` to split keys.
        'underscore': Use underscores to split keys.
        'dot': Use dots to split keys.
    inverse : bool
        Whether you want to invert the key and value before flattening.

    Returns
    -------
    unflattened_dict : dict
    """
    if isinstance(splitter, str):
        splitter = SPLITTER_DICT[splitter]

    unflattened_dict: Dict[Any, Any] = {}
    for flat_key, value in six.viewitems(d):
        if inverse:
            flat_key, value = value, flat_key
        key_tuple = splitter(flat_key)
        nested_set_dict(unflattened_dict, key_tuple, value)

    return unflattened_dict
