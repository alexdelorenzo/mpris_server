try:
  # Python 3.8+
  from typing import \
    Protocol, runtime_checkable, Final, TypedDict

except ImportError:
  # Python 3.7
  from typing_extensions import \
    Protocol, runtime_checkable, Final, TypedDict
