"""`flatten_dict.reducer` is deprecated in favor of `flatten_dict.reducers`."""
import warnings

from .reducers import *  # noqa: F401, F403

warnings.warn(
    "`flatten_dict.reducer` is deprecated in favor of `flatten_dict.reducers`.",
    FutureWarning,
)
