import abc
from _typeshed import Incomplete
from collections.abc import Generator, MutableMapping
from ipapython.dn import DN as DN, RDN as RDN
from ipapython.dnsutil import DNSName as DNSName
from ipapython.ipautil import CIDict as CIDict, format_netloc as format_netloc
from ipapython.kerberos import Principal as Principal

unicode = str
logger: Incomplete
SASL_GSSAPI: Incomplete
SASL_GSS_SPNEGO: Incomplete
AUTOBIND_AUTO: int
AUTOBIND_ENABLED: int
AUTOBIND_DISABLED: int
TRUNCATED_SIZE_LIMIT: Incomplete
TRUNCATED_TIME_LIMIT: Incomplete
TRUNCATED_ADMIN_LIMIT: Incomplete
DIRMAN_DN: Incomplete

def realm_to_serverid(realm_name): ...
def realm_to_ldapi_uri(realm_name): ...
def ldap_initialize(uri, cacertfile: Incomplete | None = ...): ...

class _ServerSchema:
    server: Incomplete
    schema: Incomplete
    retrieve_timestamp: Incomplete
    def __init__(self, server, schema) -> None: ...

class SchemaCache:
    servers: Incomplete
    def __init__(self) -> None: ...
    def get_schema(self, url, conn, force_update: bool = ...): ...
    def flush(self, url) -> None: ...

schema_cache: Incomplete

class LDAPEntry(MutableMapping):
    __hash__: Incomplete
    def __init__(
        self,
        _conn,
        _dn: Incomplete | None = ...,
        _obj: Incomplete | None = ...,
        **kwargs,
    ) -> None: ...
    @property
    def conn(self): ...
    @property
    def dn(self): ...
    @dn.setter
    def dn(self, value) -> None: ...
    @property
    def raw(self): ...
    @property
    def single_value(self): ...
    def copy(self): ...
    def __setitem__(self, name, value) -> None: ...
    def __getitem__(self, name): ...
    def __delitem__(self, name) -> None: ...
    def clear(self) -> None: ...
    def __len__(self): ...
    def __contains__(self, name): ...
    def has_key(self, name): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def reset_modlist(self, other: Incomplete | None = ...) -> None: ...
    def generate_modlist(self): ...
    def __iter__(self): ...

class LDAPEntryView(MutableMapping, metaclass=abc.ABCMeta):
    def __init__(self, entry) -> None: ...
    def __delitem__(self, name) -> None: ...
    def clear(self) -> None: ...
    def __iter__(self): ...
    def __len__(self): ...
    def __contains__(self, name): ...
    def has_key(self, name): ...

class RawLDAPEntryView(LDAPEntryView):
    def __getitem__(self, name): ...
    def __setitem__(self, name, value) -> None: ...

class SingleValueLDAPEntryView(LDAPEntryView):
    def __getitem__(self, name): ...
    def __setitem__(self, name, value) -> None: ...

class LDAPClient:
    MATCH_ANY: str
    MATCH_ALL: str
    MATCH_NONE: str
    SCOPE_BASE: Incomplete
    SCOPE_ONELEVEL: Incomplete
    SCOPE_SUBTREE: Incomplete
    time_limit: Incomplete
    size_limit: int
    ldap_uri: Incomplete
    def __init__(
        self,
        ldap_uri,
        start_tls: bool = ...,
        force_schema_updates: bool = ...,
        no_schema: bool = ...,
        decode_attrs: bool = ...,
        cacert: Incomplete | None = ...,
        sasl_nocanon: bool = ...,
    ) -> None: ...
    @classmethod
    def from_realm(cls, realm_name, **kwargs): ...
    @classmethod
    def from_hostname_secure(
        cls, hostname, cacert=..., start_tls: bool = ..., **kwargs
    ): ...
    @classmethod
    def from_hostname_plain(cls, hostname, **kwargs): ...
    def modify_s(self, dn, modlist): ...
    @property
    def conn(self): ...
    @property
    def protocol(self): ...
    def get_attribute_type(self, name_or_oid): ...
    def has_dn_syntax(self, name_or_oid): ...
    def get_attribute_single_value(self, name_or_oid): ...
    def encode(self, val): ...
    def decode(self, val, attr): ...
    def error_handler(
        self, arg_desc: Incomplete | None = ...
    ) -> Generator[None, None, None]: ...
    @staticmethod
    def handle_truncated_result(truncated) -> None: ...
    @property
    def schema(self): ...
    def get_allowed_attributes(
        self, objectclasses, raise_on_unknown: bool = ...
    ): ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_value, traceback) -> None: ...
    def close(self) -> None: ...
    def simple_bind(
        self,
        bind_dn,
        bind_password,
        server_controls: Incomplete | None = ...,
        client_controls: Incomplete | None = ...,
        insecure_bind: bool = ...,
    ) -> None: ...
    def external_bind(
        self,
        server_controls: Incomplete | None = ...,
        client_controls: Incomplete | None = ...,
    ) -> None: ...
    def gssapi_bind(
        self,
        server_controls: Incomplete | None = ...,
        client_controls: Incomplete | None = ...,
    ) -> None: ...
    def unbind(self) -> None: ...
    def make_dn_from_attr(
        self, attr, value, parent_dn: Incomplete | None = ...
    ): ...
    def make_dn(
        self,
        entry_attrs,
        primary_key: str = ...,
        parent_dn: Incomplete | None = ...,
    ): ...
    def make_entry(
        self,
        _dn: Incomplete | None = ...,
        _obj: Incomplete | None = ...,
        **kwargs,
    ): ...
    @classmethod
    def combine_filters(cls, filters, rules: str = ...): ...
    @classmethod
    def make_filter_from_attr(
        cls,
        attr,
        value,
        rules: str = ...,
        exact: bool = ...,
        leading_wildcard: bool = ...,
        trailing_wildcard: bool = ...,
    ): ...
    @classmethod
    def make_filter(
        cls,
        entry_attrs,
        attrs_list: Incomplete | None = ...,
        rules: str = ...,
        exact: bool = ...,
        leading_wildcard: bool = ...,
        trailing_wildcard: bool = ...,
    ): ...
    def get_entries(
        self,
        base_dn,
        scope=...,
        filter: Incomplete | None = ...,
        attrs_list: Incomplete | None = ...,
        get_effective_rights: bool = ...,
        **kwargs,
    ): ...
    def find_entries(
        self,
        filter: Incomplete | None = ...,
        attrs_list: Incomplete | None = ...,
        base_dn: Incomplete | None = ...,
        scope=...,
        time_limit: Incomplete | None = ...,
        size_limit: Incomplete | None = ...,
        paged_search: bool = ...,
        get_effective_rights: bool = ...,
    ): ...
    def find_entry_by_attr(
        self,
        attr,
        value,
        object_class,
        attrs_list: Incomplete | None = ...,
        base_dn: Incomplete | None = ...,
    ): ...
    def get_entry(
        self,
        dn,
        attrs_list: Incomplete | None = ...,
        time_limit: Incomplete | None = ...,
        size_limit: Incomplete | None = ...,
        get_effective_rights: bool = ...,
    ): ...
    def add_entry(self, entry) -> None: ...
    def move_entry(self, dn, new_dn, del_old: bool = ...) -> None: ...
    def update_entry(self, entry) -> None: ...
    def delete_entry(self, entry_or_dn) -> None: ...
    def entry_exists(self, dn): ...

def get_ldap_uri(
    host: str = ...,
    port: int = ...,
    cacert: Incomplete | None = ...,
    ldapi: bool = ...,
    realm: Incomplete | None = ...,
    protocol: Incomplete | None = ...,
): ...

class CacheEntry:
    entry: Incomplete
    attrs_list: Incomplete
    exception: Incomplete
    all: Incomplete
    def __init__(
        self,
        entry: Incomplete | None = ...,
        attrs_list: Incomplete | None = ...,
        exception: Incomplete | None = ...,
        get_effective_rights: bool = ...,
        all: bool = ...,
    ) -> None: ...

class LDAPCache(LDAPClient):
    cache: Incomplete
    def __init__(
        self,
        ldap_uri,
        start_tls: bool = ...,
        force_schema_updates: bool = ...,
        no_schema: bool = ...,
        decode_attrs: bool = ...,
        cacert: Incomplete | None = ...,
        sasl_nocanon: bool = ...,
        enable_cache: bool = ...,
        cache_size: int = ...,
        debug_cache: bool = ...,
    ) -> None: ...
    @property
    def hit(self): ...
    @property
    def miss(self): ...
    @property
    def max_entries(self): ...
    def emit(self, msg, *args, **kwargs) -> None: ...
    def copy_entry(self, dn, entry, attrs=...): ...
    def add_cache_entry(
        self,
        dn,
        attrs_list: Incomplete | None = ...,
        get_all: bool = ...,
        entry: Incomplete | None = ...,
        exception: Incomplete | None = ...,
    ) -> None: ...
    def clear_cache(self) -> None: ...
    def cache_status(self, type) -> None: ...
    def remove_cache_entry(self, dn) -> None: ...
    def add_entry(self, entry) -> None: ...
    def update_entry(self, entry) -> None: ...
    def delete_entry(self, entry_or_dn) -> None: ...
    def move_entry(self, dn, new_dn, del_old: bool = ...) -> None: ...
    def modify_s(self, dn, modlist): ...
    def get_entry(
        self,
        dn,
        attrs_list: Incomplete | None = ...,
        time_limit: Incomplete | None = ...,
        size_limit: Incomplete | None = ...,
        get_effective_rights: bool = ...,
    ): ...
