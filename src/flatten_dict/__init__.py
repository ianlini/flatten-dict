from .flatten_dict import flatten, unflatten  # noqa: F401
from importlib.metadata import version

__all__ = ["flatten", "unflatten", "splitter"]

__version__ = version("flatten-dict")
