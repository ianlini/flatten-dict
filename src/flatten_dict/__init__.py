import pkg_resources
from .flatten_dict import flatten, unflatten  # noqa: F401


__all__ = ['flatten_dict', 'reducer', 'splitter']
__version__ = pkg_resources.get_distribution("flatten-dict").version
