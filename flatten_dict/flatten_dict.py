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


def flatten(d, reducer='tuple', inverse=False):
    """Flatten dict-like object.

    Parameters
    ----------
    d: dict-like object
        The dict that will be flattened.
    reducer: {'tuple', 'path', function} (default: 'tuple')
        The key joining method. If a function is given, the function will be
        used to reduce.
        'tuple': The resulting key will be tuple of the original keys
        'path': Use ``os.path.join`` to join keys.
    inverse: bool (default: False)
        Whether you want invert the resulting key and value.

    Returns
    -------
    flat_dict: dict
    """
    if isinstance(reducer, str):
        reducer = REDUCER_DICT[reducer]
    flat_dict = {}

    def _flatten(d, parent=None):
        for key, val in six.viewitems(d):
            flat_key = reducer(parent, key)
            if isinstance(val, Mapping):
                _flatten(val, flat_key)
            elif inverse:
                if val in flat_dict:
                    raise ValueError("duplicated key '{}'".format(val))
                flat_dict[val] = flat_key
            else:
                flat_dict[flat_key] = val

    _flatten(d)
    return flat_dict


def recursively_set_dict(d, keys, value):
    """
    Parameters
    ----------
    d: Mapping
    keys: Sequence[str]
    value: Any
    """
    assert keys
    if len(keys) == 1:
        d[keys[0]] = value
        return
    d = d.setdefault(keys[0], {})
    recursively_set_dict(d, keys[1:], value)


def unflatten(d, splitter='tuple', inverse=False):
    """Unflatten dict-like object.

    Parameters
    ----------
    d: dict-like object
        The dict that will be unflattened.
    splitter: {'tuple', 'path', function} (default: 'tuple')
        The key splitting method. If a function is given, the function will be
        used to split.
        'tuple': Use each element in the tuple key as the key of the unflattened dict.
        'path': Use ``pathlib.Path.parts`` to split keys.
    inverse: bool (default: False)
        Whether you want invert the key and value before flattening.

    Returns
    -------
    unflattened_dict: dict
    """
    if isinstance(splitter, str):
        splitter = SPLITTER_DICT[splitter]

    unflattened_dict = {}
    for flat_key, value in six.viewitems(d):
        if inverse:
            flat_key, value = value, flat_key
        key_tuple = splitter(flat_key)
        recursively_set_dict(unflattened_dict, key_tuple, value)

    return unflattened_dict
