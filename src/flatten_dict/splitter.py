from pathlib2 import PurePath


def tuple_splitter(flat_key):
    return flat_key


def path_splitter(flat_key):
    keys = PurePath(flat_key).parts
    return keys


def dot_splitter(flat_key):
    keys = tuple(flat_key.split('.'))
    return keys


def underscore_splitter(flat_key):
    keys = tuple(flat_key.split("_"))
    return keys


def make_splitter(delimiter):
    """Create a splitter with a custom delimiter.

    :param delimiter: delimiter to use to split keys. 
    :return: callable: callable that can be passed to ``unflatten``'s ``splitter`` argument.
    """
    def f(flat_key):
        keys = tuple(flat_key.split(delimiter))
        return keys
    return f
