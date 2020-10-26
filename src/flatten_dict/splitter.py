"""`flatten_dict.splitter` is deprecated in favor of `flatten_dict.splitters`."""
import warnings

from .splitters import *  # noqa: F401, F403

warnings.warn(
    "`flatten_dict.splitter` is deprecated in favor of `flatten_dict.splitters`.",
    FutureWarning,
)
