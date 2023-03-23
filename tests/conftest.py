import contextlib
import importlib
import logging
import io
import os
import sys
import unittest

from ipalib import api

from ipahcc import hccplatform
from ipahcc.server import schema

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
TESTDATA = os.path.join(BASEDIR, "tests", "data")

DOMAIN = "ipa-hcc.test"
REALM = DOMAIN.upper()
CLIENT_FQDN = "client.ipa-hcc.test"
SERVER_FQDN = "server.ipa-hcc.test"
DOMAIN_ID = hccplatform.TEST_DOMAIN_ID
CLIENT_RHSM_ID = "1ee437bc-7b65-40cc-8a02-c24c8a7f9368"
CLIENT_INVENTORY_ID = "1efd5f0e-7589-44ac-a9af-85ba5569d5c3"
SERVER_RHSM_ID = "e658e3eb-148c-46a6-b48a-099f9593191a"
SERVER_INVENTORY_ID = "f0468001-7632-4d3f-afd2-770c93825adf"
ORG_ID = "16765486"

# initialize first step of IPA API so server imports work
if not api.isdone("bootstrap"):
    api.bootstrap(
        host=CLIENT_FQDN,
        server=SERVER_FQDN,
        domain=DOMAIN,
        realm=REALM,
    )
else:  # pragma: no cover
    pass


try:
    import ipaclient.install  # noqa: F401
    import ipalib.install  # noqa: F401
except ImportError:
    HAS_IPA_INSTALL = False
else:
    HAS_IPA_INSTALL = True

try:
    import ipaserver.masters  # noqa: F401
except ImportError:
    HAS_IPASERVER = False
else:
    HAS_IPASERVER = True

try:
    import dbus.mainloop.glib  # noqa: F401
    import gi.repository  # noqa: F401
except ImportError:
    HAS_DBUS = False
else:  # pragma: no cover
    HAS_DBUS = True

try:
    from unittest import mock
except ImportError:
    try:
        import mock
    except ImportError:  # pragma: no cover
        mock = None

requires_ipa_install = unittest.skipUnless(
    HAS_IPA_INSTALL, "requires 'ipaclient.install' or 'ipalib.install'"
)
requires_ipaserver = unittest.skipUnless(
    HAS_IPASERVER, "requires 'ipaserver'"
)
requires_jsonschema = unittest.skipUnless(
    schema.jsonschema, "requires 'jsonschema'"
)
requires_dbus = unittest.skipUnless(
    HAS_DBUS, "requires 'dbus' and 'gi.repository'"
)
requires_mock = unittest.skipUnless(
    mock is not None, "requires 'unittest.mock' or 'mock'"
)


class CaptureHandler(logging.Handler):
    def __init__(self):
        super(CaptureHandler, self).__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


class IPABaseTests(unittest.TestCase):
    def log_capture_start(self):
        self.log_capture = CaptureHandler()
        self.log_capture.setFormatter(
            logging.Formatter("%(levelname)s:%(name)s:%(message)s")
        )

        root_logger = logging.getLogger(None)
        self._old_handlers = root_logger.handlers[:]
        self._old_level = root_logger.level
        root_logger.handlers = [self.log_capture]
        root_logger.setLevel(logging.DEBUG)
        self.addCleanup(self.log_capture_stop)

    def log_capture_stop(self):
        root_logger = logging.getLogger(None)
        root_logger.handlers = self._old_handlers
        root_logger.setLevel(self._old_level)

    def setUp(self):
        super(IPABaseTests, self).setUp()
        self.log_capture_start()

    def assert_cli_run(self, mainfunc, *args):
        try:
            with capture_output():
                mainfunc(list(args))
        except SystemExit as e:
            self.assertEqual(e.code, 0)
        else:  # pragma: no cover
            self.fail("SystemExit expected")


@contextlib.contextmanager
def capture_output():
    if hccplatform.PY2:
        out = io.BytesIO()
    else:
        out = io.StringIO()
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr
    sys.stdout = out
    sys.stderr = out
    try:
        yield out
    finally:
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr


def _fixup_ipaserver_import(name):
    path = os.path.join(BASEDIR, name.replace(".", os.sep))
    mod = importlib.import_module(name)
    mod.__path__.append(path)


if HAS_IPASERVER:
    _fixup_ipaserver_import("ipaserver.install.plugins")
    _fixup_ipaserver_import("ipaserver.plugins")