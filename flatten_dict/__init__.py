import pkg_resources
from .flatten_dict import flatten  # noqa: F401


__all__ = ['flatten_dict', 'reducer']
__version__ = pkg_resources.get_distribution("flatten-dict").version
