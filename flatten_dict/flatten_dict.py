from collections import Mapping

import six

from .reducer import tuple_reducer, path_reducer
from .splitter import tuple_splitter, path_splitter


REDUCER_DICT = {
    'tuple': tuple_reducer,
    'path': path_reducer,
}

SPLITTER_DICT = {
    'tuple': tuple_splitter,
    'path': path_splitter,
}


def flatten(d, reducer='tuple', inverse=False, enumerate_types=()):
    """Flatten `Mapping` object.

    Parameters
    ----------
    d : dict-like object
        The dict that will be flattened.
    reducer : {'tuple', 'path', Callable}
        The key joining method. If a `Callable` is given, the `Callable` will be
        used to reduce.
        'tuple': The resulting key will be tuple of the original keys.
        'path': Use `os.path.join` to join keys.
    inverse : bool
        Whether you want invert the resulting key and value.
    enumerate_types : Sequence[type]
        Flatten these types using `enumerate`.
        For example, if we set `enumerate_types` to ``(list,)``,
        `list` indices become keys: ``{'a': ['b', 'c']}`` -> ``{('a', 0): 'b', ('a', 1): 'c'}``.

    Returns
    -------
    flat_dict : dict
    """
    enumerate_types = tuple(enumerate_types)
    flattenable_types = (Mapping,) + enumerate_types
    if not isinstance(d, flattenable_types):
        raise ValueError("argument type %s is not in the flattenalbe types %s"
                         % (type(d), flattenable_types))

    if isinstance(reducer, str):
        reducer = REDUCER_DICT[reducer]
    flat_dict = {}

    def _flatten(d, parent=None):
        key_value_iterable = enumerate(d) if isinstance(d, enumerate_types) else six.viewitems(d)
        for key, value in key_value_iterable:
            flat_key = reducer(parent, key)
            if isinstance(value, flattenable_types):
                _flatten(value, flat_key)
            else:
                if inverse:
                    flat_key, value = value, flat_key
                if flat_key in flat_dict:
                    raise ValueError("duplicated key '{}'".format(flat_key))
                flat_dict[flat_key] = value

    _flatten(d)
    return flat_dict


def nested_set_dict(d, keys, value):
    """Set a value to a sequence of nested keys

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


def unflatten(d, splitter='tuple', inverse=False):
    """Unflatten dict-like object.

    Parameters
    ----------
    d : dict-like object
        The dict that will be unflattened.
    splitter : {'tuple', 'path', Callable}
        The key splitting method. If a Callable is given, the Callable will be
        used to split.
        'tuple': Use each element in the tuple key as the key of the unflattened dict.
        'path': Use `pathlib.Path.parts` to split keys.
    inverse : bool
        Whether you want to invert the key and value before flattening.

    Returns
    -------
    unflattened_dict : dict
    """
    if isinstance(splitter, str):
        splitter = SPLITTER_DICT[splitter]

    unflattened_dict = {}
    for flat_key, value in six.viewitems(d):
        if inverse:
            flat_key, value = value, flat_key
        key_tuple = splitter(flat_key)
        nested_set_dict(unflattened_dict, key_tuple, value)

    return unflattened_dict
