def tuple_reducer(k1, k2):
    if k1 is None:
        return (k2,)
    return k1 + (k2,)


def path_reducer(k1, k2):
    import os.path

    # Coerce like underscore/dot reducers so enumerate_types int keys work.
    if k1 is None:
        return k2 if isinstance(k2, (str, bytes)) else str(k2)
    if not isinstance(k1, (str, bytes)):
        k1 = str(k1)
    if not isinstance(k2, (str, bytes)):
        k2 = str(k2)
    return os.path.join(k1, k2)


def dot_reducer(k1, k2):
    if k1 is None:
        return k2
    return "{}.{}".format(k1, k2)


def underscore_reducer(k1, k2):
    if k1 is None:
        return k2
    return "{}_{}".format(k1, k2)


def make_reducer(delimiter):
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

    def f(k1, k2):
        if k1 is None:
            return k2
        return "{}{}{}".format(k1, delimiter, k2)

    return f
