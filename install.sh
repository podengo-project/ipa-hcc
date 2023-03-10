#!/bin/sh
set -ex

SITE_PACKAGES=$(python -c 'from sys import version_info as v; print("/usr/lib/python{}.{}/site-packages".format(v.major, v.minor))')

## phase 1, handled by RPM package

# user and group
getent group ipaapi >/dev/null || groupadd -f -r ipaapi
getent passwd ipahcc >/dev/null || useradd -r -g ipaapi -s /sbin/nologin -d /usr/share/ipa-hcc -c "IPA Hybrid Cloud Console enrollment service" ipahcc

# directories, cache directory must be writeable by user
mkdir -p /etc/ipa/hcc
mkdir -p /usr/share/ipa-hcc
mkdir -p /usr/libexec/ipa-hcc
mkdir -p /var/cache/ipa-hcc
chmod 750 -R /var/cache/ipa-hcc
chown ipahcc:ipaapi -R /var/cache/ipa-hcc
chmod 750 -R /etc/ipa/hcc
chown ipahcc:root -R /etc/ipa/hcc
semanage fcontext -a -f a -s system_u -t httpd_cache_t -r 's0' '/var/cache/ipa-hcc(/.*)?' || :
restorecon -R /var/cache/ipa-hcc || :

cp etc/ipa/hcc.conf /etc/ipa/

# WSGI app and configuration
cp wsgi/hcc_registration_service.py /usr/share/ipa-hcc/
cp etc/apache/ipa-hcc.conf /etc/httpd/conf.d/ipa-hcc.conf
# cp refresh_token /etc/ipa/hcc || true

# Mock API WSGI app
cp etc/apache/ipa-hcc-mockapi.conf /etc/httpd/conf.d/
cp wsgi/hcc_mockapi.py /usr/share/ipa-hcc/

# CA certs
cp rhsm/redhat-candlepin-bundle.pem /usr/share/ipa-hcc/redhat-candlepin-bundle.pem
mkdir -p /usr/share/ipa-hcc/cacerts
cp rhsm/cacerts/* /usr/share/ipa-hcc/cacerts/

# gssproxy
cp etc/gssproxy/85-ipa-hcc.conf /etc/gssproxy/
systemctl restart gssproxy.service

# IPA plugins, UI, schema, and update
cp schema.d/85-hcc.ldif /usr/share/ipa/schema.d/
cp updates/85-hcc.update /usr/share/ipa/updates/

mkdir -p -m 755 /usr/share/ipa/ui/js/plugins/hccconfig
cp ui/js/plugins/hccconfig/hccconfig.js /usr/share/ipa/ui/js/plugins/hccconfig/
mkdir -p -m 755 /usr/share/ipa/ui/js/plugins/hcchost
cp ui/js/plugins/hcchost/hcchost.js /usr/share/ipa/ui/js/plugins/hcchost/

cp ipaserver/plugins/*.py ${SITE_PACKAGES}/ipaserver/plugins/
cp ipaserver/install/*.py ${SITE_PACKAGES}/ipaserver/install/
cp ipaserver/install/plugins/*.py ${SITE_PACKAGES}/ipaserver/install/plugins/
cp ipaplatform/*.py ${SITE_PACKAGES}/ipaplatform
python3 -m compileall ${SITE_PACKAGES}/ipaserver/plugins/ ${SITE_PACKAGES}/ipaserver/install/plugins ${SITE_PACKAGES}/ipaplatform
cp server/ipa-hcc /usr/sbin/

exit 0

# run updater
ipa-ldap-updater \
    -S /usr/share/ipa/schema.d/85-hcc.ldif \
    /usr/share/ipa/updates/85-hcc.update \
    /usr/share/ipa/updates/86-hcc-enrollment-service.update
killall -9 httpd
systemctl restart httpd.service

echo "NOTE: $0 is a hack for internal development."
echo "Some changes require a proper ipa-server-upgrade or ipactl restart."
