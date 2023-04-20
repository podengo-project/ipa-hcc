from ipalib import errors as errors
from ipalib.base import check_name as check_name
from ipalib.constants import (
    CONFIG_SECTION as CONFIG_SECTION,
    DEL_ERROR as DEL_ERROR,
    OVERRIDE_ERROR as OVERRIDE_ERROR,
    SET_ERROR as SET_ERROR,
    TLS_VERSIONS as TLS_VERSIONS,
    TLS_VERSION_DEFAULT_MAX as TLS_VERSION_DEFAULT_MAX,
    TLS_VERSION_DEFAULT_MIN as TLS_VERSION_DEFAULT_MIN,
)

unicode = str

class Env:
    def __init__(self, **initialize) -> None: ...
    def __lock__(self) -> None: ...
    def __islocked__(self): ...
    def __setattr__(self, name, value) -> None: ...
    def __setitem__(self, key, value) -> None: ...
    def __getitem__(self, key): ...
    def __delattr__(self, name) -> None: ...
    def __contains__(self, key): ...
    def __len__(self): ...
    def __iter__(self): ...