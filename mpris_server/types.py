try:
  # Python 3.10+
  from typing import \
    Protocol, runtime_checkable, Final, TypedDict, TypeAlias

except ImportError:
  # Python 3.7 - 3.9
  from typing_extensions import \
    Protocol, runtime_checkable, Final, TypedDict, TypeAlias
