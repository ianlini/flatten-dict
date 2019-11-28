def tuple_reducer(k1, k2):
    if k1 is None:
        return (k2,)
    else:
        return k1 + (k2,)


def path_reducer(k1, k2):
    import os.path
    if k1 is None:
        return k2
    else:
        return os.path.join(k1, k2)


def dot_reducer(k1, k2):
    if k1 is None:
        return k2
    else:
        return "{0}.{1}".format(k1, k2)


def underscore_reducer(k1, k2):
    if k1 is None:
        return k2
    else:
        return "{0}_{1}".format(k1, k2)
