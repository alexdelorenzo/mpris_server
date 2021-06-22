# Python 3.10+
try:
  from typing import \
    Protocol, runtime_checkable, Final, TypedDict, TypeAlias, \
    get_origin, GenericAlias, _GenericAlias

# Python 3.7 - 3.9
except ImportError:
  from typing_extensions import \
    Protocol, runtime_checkable, Final, TypedDict, TypeAlias, \
    get_origin, GenericAlias, _GenericAlias

from typing import Union


GenericAliases = Union[GenericAlias, _GenericAlias]
