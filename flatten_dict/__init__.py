import pkg_resources
from .flatten_dict import flatten

__all__ = ['flatten_dict', 'reducer']
__version__ = pkg_resources.get_distribution("flatten-dict").version
