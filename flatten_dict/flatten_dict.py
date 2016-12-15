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

def flatten(d, reducer='tuple', inverse=False):
    if isinstance(reducer, str):
        reducer = REDUCER_DICT[reducer]

    def _flatten(d, parent=None):
        flat_dict = {}
        for key, val in six.viewitems(d):
            flat_key = reducer(parent, key)
            if isinstance(val, MutableMapping):
                flat_dict.update(_flatten(val, flat_key))
            elif inverse:
                if val in flat_dict:
                    raise ValueError("duplicated key '{}'".format(val))
                flat_dict[val] = flat_key
            else:
                flat_dict[flat_key] = val
        return flat_dict

    return _flatten(d)

