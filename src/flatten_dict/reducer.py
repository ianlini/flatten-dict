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


def make_reducer(delimiter):
    """Create a reducer with a custom delimiter.

    :param delimiter: delimiter to use to join keys.
    :return: callable: callable that can be passed to ``flatten``'s ``reducer`` argument.
    """

    def f(k1, k2):
        if k1 is None:
            return k2
        else:
            return f"{k1}{delimiter}{k2}"

    return f
