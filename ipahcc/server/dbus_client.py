import json
import logging
import typing

import dbus
import dbus.mainloop.glib

from ipahcc import hccplatform

from .hccapi import APIError, APIResult

__all__ = ("check_host", "register_domain", "update_domain")

logger = logging.getLogger("dbus-client")


def _dbus_getmethod(
    method_name: str, bus: typing.Optional[dbus.Bus] = None
) -> typing.Callable:  # pragma: no cover
    """Get method wrapper from HCC D-Bus service"""
    if bus is None:
        bus = dbus.SystemBus()
    obj = bus.get_object(
        hccplatform.HCC_DBUS_NAME, hccplatform.HCC_DBUS_OBJ_PATH
    )
    iface = dbus.Interface(obj, hccplatform.HCC_DBUS_IFACE_NAME)
    return getattr(iface, method_name)


def _dbus_call(method_name: str, *args, **kwargs) -> APIResult:
    method = _dbus_getmethod(method_name, kwargs.get("bus"))
    logger.info("D-Bus call: %s%s", method_name, args)
    try:
        result = method(*args)
    except dbus.exceptions.DBusException:
        logger.exception(
            "D-Bus service %s failed with an internal error",
            hccplatform.HCC_DBUS_NAME,
        )
        raise

    # convert from D-Bus types to Python types
    tmp = APIResult(*result)
    rid = tmp.id
    status_code = int(tmp.status_code)
    reason = str(tmp.reason)
    url = str(tmp.url) if tmp.url else None
    assert tmp.headers
    headers = {str(k).lower(): str(v) for k, v in tmp.headers.items()}
    if headers.get("content-type") == "application/json":
        assert isinstance(tmp.body, str)
        body = json.loads(tmp.body)
    else:
        body = str(tmp.body)
    exit_code = int(tmp.exit_code)
    exit_message = str(tmp.exit_message)

    result = APIResult(
        rid, status_code, reason, url, headers, body, exit_code, exit_message
    )
    if result.exit_code == 0:
        return result
    else:
        raise APIError(result)


def check_host(
    domain_id: str,
    inventory_id: str,
    rhsm_id: str,
    fqdn: str,
    bus: typing.Optional[dbus.Bus] = None,
) -> APIResult:
    return _dbus_call(
        "check_host", domain_id, inventory_id, rhsm_id, fqdn, bus=bus
    )


def register_domain(
    domain_id: str, token: str, bus: typing.Optional[dbus.Bus] = None
) -> APIResult:
    return _dbus_call("register_domain", domain_id, token, bus=bus)


def update_domain(
    update_server_only: bool = False, bus: typing.Optional[dbus.Bus] = None
) -> APIResult:
    return _dbus_call("update_domain", update_server_only, bus=bus)


def status_check(bus: typing.Optional[dbus.Bus] = None) -> APIResult:
    return _dbus_call("status_check", bus=bus)
