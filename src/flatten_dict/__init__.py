from .flatten_dict import flatten, unflatten  # noqa: F401


__all__ = ["flatten", "unflatten", "splitter"]

try:
    # for Python >= 3.8
    from importlib.metadata import version
except ImportError:
    # for Python < 3.8, the package importlib-metadata will be installed
    from importlib_metadata import version

__version__ = version("flatten-dict")
