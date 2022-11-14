#!/bin/sh
set -e

SITE_PACKAGES=$(python3 -c 'from sys import version_info as v; print(f"/usr/lib/python{v.major}.{v.minor}/site-packages")')

if [ -f /usr/share/ipa/schema.d/85-consoledot.ldif -a -f /usr/share/ipa/updates/85-consoledot.update ]; then
    NEEDS_UPGRADE=0;
else
    NEEDS_UPGRADE=1;
fi

cp schema.d/85-consoledot.ldif /usr/share/ipa/schema.d/
cp updates/85-consoledot.update /usr/share/ipa/updates/

mkdir -p -m 755 /usr/share/ipa/ui/js/plugins/consoledotconfig
cp ui/js/plugins/consoledotconfig/consoledotconfig.js /usr/share/ipa/ui/js/plugins/consoledotconfig/
mkdir -p -m 755 /usr/share/ipa/ui/js/plugins/consoledothost
cp ui/js/plugins/consoledothost/consoledothost.js /usr/share/ipa/ui/js/plugins/consoledothost/

cp ipaserver/plugins/*.py ${SITE_PACKAGES}/ipaserver/plugins/
python3 -m compileall ${SITE_PACKAGES}/ipaserver/plugins/

cp wsgi/consoledot.py /usr/share/ipa/
cp apache/consoledot.conf /etc/httpd/conf.d/99-consoledot.conf

if [ $NEEDS_UPGRADE = 1 ]; then
    ipa-server-upgrade
else
    ipa-ldap-updater \
        -S /usr/share/ipa/schema.d/85-consoledot.ldif \
        /usr/share/ipa/updates/85-consoledot.update
    systemctl restart httpd.service
fi

echo "NOTE: $0 is a hack for internal development."
echo "Some changes require a proper ipa-server-upgrade or ipactl restart."
