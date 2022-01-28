#!/usr/bin/env python

from imapclient import IMAPClient
from ssl import SSLCertVerificationError

def test_imap_tls(host, port):
    try:
        server = IMAPClient(host, port)
        print(f"{server.host} {server.port} Connection OK")

    except SSLCertVerificationError as error:
        print(f"{host} {port} {error}")

    except ConnectionRefusedError as error:
        print(f"{host} {port} {error}")

    except Exception as error:
        print(f"{type(error)} {error}")    

test_imap_tls('localhost', '2993')
test_imap_tls('mail.gturn.xyz', '993')
test_imap_tls('localhost', '993')
