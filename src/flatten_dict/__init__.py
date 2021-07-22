from .flatten_dict import flatten, unflatten  # noqa: F401


__all__ = ["flatten", "unflatten", "splitter"]

try:
    from importlib.metadata import distribution
except ImportError:
    try:
        from importlib_metadata import distribution
    except ImportError:
        from pkg_resources import get_distribution as distribution

__version__ = distribution("flatten-dict").version
