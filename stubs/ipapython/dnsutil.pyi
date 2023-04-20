import dns.reversename
import dns.resolver
from _typeshed import Incomplete
from ipapython.ipautil import UnsafeIPAddress as UnsafeIPAddress

unicode = str
logger: Incomplete
ipa_resolver: Incomplete

def get_ipa_resolver(): ...
def resolve(*args, **kwargs): ...
def resolve_address(*args, **kwargs): ...
def zone_for_name(*args, **kwargs): ...
def reset_default_resolver() -> None: ...

class DNSResolver(dns.resolver.Resolver):
    resolve: Incomplete
    resolve_address: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    timeout: Incomplete
    lifetime: Incomplete
    use_search_by_default: bool
    def reset_ipa_defaults(self) -> None: ...
    def reset(self) -> None: ...
    def read_resolv_conf(self, *args, **kwargs) -> None: ...
    nameserver_ports: Incomplete
    # def nameservers(self, nameservers) -> None: ...

class DNSZoneAlreadyExists(dns.exception.DNSException):
    supp_kwargs: Incomplete
    fmt: str

class DNSName(dns.name.Name):
    labels: Incomplete
    @classmethod
    def from_text(cls, labels, origin: Incomplete | None = ...): ...
    def __init__(self, labels, origin: Incomplete | None = ...) -> None: ...
    def __bool__(self): ...
    __nonzero__: Incomplete
    def __copy__(self): ...
    def __deepcopy__(self, memo): ...
    def ToASCII(self): ...
    def canonicalize(self): ...
    def concatenate(self, other): ...
    def relativize(self, origin): ...
    def derelativize(self, origin): ...
    def choose_relativity(
        self, origin: Incomplete | None = ..., relativize: bool = ...
    ): ...
    def make_absolute(self): ...
    def is_idn(self): ...
    def is_ip4_reverse(self): ...
    def is_ip6_reverse(self): ...
    def is_reverse(self): ...
    def is_empty(self): ...

EMPTY_ZONES: Incomplete

def assert_absolute_dnsname(name) -> None: ...
def is_auto_empty_zone(zone): ...
def inside_auto_empty_zone(name): ...
def related_to_auto_empty_zone(name): ...
def has_empty_zone_addresses(hostname): ...
def resolve_rrsets(fqdn, rdtypes): ...
def resolve_ip_addresses(fqdn): ...
def check_zone_overlap(zone, raise_on_error: bool = ...) -> None: ...
def sort_prio_weight(records): ...
def query_srv(qname, resolver: Incomplete | None = ..., **kwargs): ...
