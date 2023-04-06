from __future__ import absolute_import, print_function

import argparse
import logging
import sys
import uuid

import dbus.exceptions

from ipapython import admintool

from ipahcc import hccplatform
from . import dbus_client
from .hccapi import APIError

logger = logging.getLogger(__name__)


def uuidtype(v):
    uuid.UUID(v)
    return v


parser = argparse.ArgumentParser(
    prog="ipa-hcc",
    description="Register or update IPA domain in Hybrid Cloud Console",
    usage="\n".join(
        [
            "",
            "  %(prog)s [options] register DOMAIN_ID TOKEN",
            "  %(prog)s [options] update [--update-server-only]",
            "  %(prog)s [options] status",
            # undocumented option for debugging and testing
            # "%prog [options] check-host INVENTORY_ID RHSM_ID FQDN",
        ]
    ),
)
parser.add_argument(
    "--version",
    "-V",
    help="Show version number and exit",
    action="version",
    version="ipa-hcc {} (IPA {})".format(
        hccplatform.VERSION, hccplatform.IPA_VERSION
    ),
)
subparsers = parser.add_subparsers(dest="action")


def register_callback(result):
    print(result)


parser_register = subparsers.add_parser(
    "register", help="Register a domain with Hybrid Cloud Console"
)
parser_register.set_defaults(callback=register_callback)
parser_register.add_argument("domain_id", type=uuidtype)
parser_register.add_argument("token", type=str)


def update_callback(result):
    print(result)


parser_update = subparsers.add_parser(
    "update", help="Update domain information"
)
parser_update.set_defaults(callback=update_callback)
parser_update.add_argument("--update-server-only", action="store_true")


def status_callback(result):
    j = result.body
    nr = "<not registered>"
    print("domain name: {}".format(j["domain_name"]))
    print("domain id: {}".format(j.get("domain_id") or nr))
    print("org id: {}".format(j.get("org_id") or nr))
    print("servers:")
    for server in j[hccplatform.HCC_DOMAIN_TYPE]["servers"]:
        fqdn = server["fqdn"]
        has_hcc = "yes" if server["hcc_update_server"] else "no"
        print(
            "\t{fqdn} (HCC plugin: {has_hcc})".format(
                fqdn=fqdn, has_hcc=has_hcc
            )
        )


parser_status = subparsers.add_parser("status", help="Check status")
parser_status.set_defaults(callback=status_callback)

# undocumented debug helper


def check_host_callback(result):
    print(result)


parser_check_host = subparsers.add_parser("check-host")
parser_check_host.set_defaults(callback=check_host_callback)
parser_check_host.add_argument("domain_id", type=uuidtype)
parser_check_host.add_argument("inventory_id", type=uuidtype)
parser_check_host.add_argument("rhsm_id", type=uuidtype)
parser_check_host.add_argument("fqdn")


def main(args=None):
    args = parser.parse_args(args)
    # Python < 3.7 does not have required subparser
    if not getattr(args, "action", None):
        parser.error("action required\n")
    if not hccplatform.is_ipa_configured():
        print("IPA is not configured on this system.", file=sys.stderr)
        parser.exit(admintool.SERVER_NOT_CONFIGURED)
    try:
        if args.action == "check-host":
            result = dbus_client.check_host(
                args.domain_id,
                args.inventory_id,
                args.rhsm_id,
                args.fqdn,
            )
        elif args.action == "register":
            result = dbus_client.register_domain(args.domain_id, args.token)
        elif args.action == "update":
            result = dbus_client.update_domain(args.update_server_only)
        elif args.action == "status":
            result = dbus_client.status_check()
        else:  # pragma: no cover
            raise ValueError(args.action)
    except dbus.exceptions.DBusException as e:
        logger.exception("D-Bus call failed")
        print("D-Bus error: {e}".format(e=e), file=sys.stderr)
        parser.exit(255)
    except APIError as e:
        logger.error("API error: %s", e)
        print(e.result.exit_message, file=sys.stderr)
        parser.exit(e.result.exit_code)
    else:
        args.callback(result)
        if result.exit_code == 0:
            parser.exit(0)
        else:
            parser.exit(result.exit_code, result.exit_code + "\n")


if __name__ == "__main__":
    main()
