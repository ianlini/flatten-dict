import sys

from .flatten_dict import flatten, unflatten  # noqa: F401


__all__ = ["flatten", "unflatten", "splitter"]

if sys.version_info >= (3, 8):
    # for Python >= 3.8
    from importlib.metadata import version
else:
    # for Python < 3.8, the package importlib-metadata will be installed
    from importlib_metadata import version

__version__ = version("flatten-dict")
