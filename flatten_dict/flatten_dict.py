from collections import Mapping

import six

from .reducer import tuple_reducer, path_reducer


REDUCER_DICT = {
    'tuple': tuple_reducer,
    'path': path_reducer,
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

