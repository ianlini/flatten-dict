from collections import MutableMapping

import six


def tuple_reducer(k1, k2):
    if k1 is None:
        return (k2,)
    else:
        return k1 + (k2,)

REDUCER_DICT = {
    'tuple': tuple_reducer,
}

def flatten(d, reducer='tuple'):
    def _flatten(d, reducer='tuple', parent=None):
        flat_dict = {}
        for key, val in six.viewitems(d):
            flat_key = reducer(parent, key)
            if isinstance(d, MutableMapping):
                flat_dict.update(flatten(d, reducer, flat_key))
            else:
                flat_dict[flat_key] = val
        return flat_dict

    if isinstance(reducer, str):
        reducer = REDUCER_DICT[reducer]

    return _flatten(d, reducer)

