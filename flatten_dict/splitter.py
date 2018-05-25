from pathlib2 import PurePath


def tuple_splitter(flat_key):
    return flat_key


def path_splitter(flat_key):
    keys = PurePath(flat_key).parts
    return keys
