"""Package initialization."""

from ._git_version import get_versions  # noqa
from ._version import __version__  # noqa

__git_version__ = get_versions()["version"]
del get_versions
