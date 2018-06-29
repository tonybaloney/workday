Authentication
==============


WS-Security with x509 signed requests is not currently working because of a bug in zeep.

openssl req -out csr.csr -new -newkey rsa:2048 -nodes -keyout privatekey.key

openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout privatekey.key -out certificate.crt