from _typeshed import Incomplete

logger: Incomplete
FORMAT: str
unicode = str

class Schema:
    namespaces: Incomplete
    fingerprint: Incomplete
    ttl: Incomplete
    _DIR: str
    def __init__(
        self, client, fingerprint: Incomplete | None = ..., ttl: int = ...
    ) -> None: ...
    def __getitem__(self, key): ...
    def read_namespace_member(self, namespace, member): ...
    def iter_namespace(self, namespace): ...
    def get_help(self, namespace, member): ...

def get_package(server_info, client): ...
