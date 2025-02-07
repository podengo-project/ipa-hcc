RHSM test certs
===============

The certificate in this directory is used to test the validity of
the bundled Candlepin CA certificate chain.  The cert is not
actually used for anything else in the test suite.

This cert will need to be updated annually (because the validity
duration of subscription certs is currently 1 year).  You can grab a
real (but throwaway) certificate from Subscription Manager on Stage:

```
hostnamectl hostname ipaclient1.hmsidm.test
subscription-manager config --server.hostname subscription.rhsm.stage.redhat.com
subscription-manager register --org 16764524 --activationkey $KEY
```
