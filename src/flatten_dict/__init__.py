from importlib.metadata import version

from .flatten_dict import flatten, unflatten  # noqa: F401

__all__ = ["flatten", "unflatten", "splitter"]

__version__ = version("flatten-dict")
