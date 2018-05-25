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
        for key, value in six.viewitems(d):
            flat_key = reducer(parent, key)
            if isinstance(value, Mapping):
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
    d: Mapping
    keys: Sequence[str]
    value: Any
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
        nested_set_dict(unflattened_dict, key_tuple, value)

    return unflattened_dict
