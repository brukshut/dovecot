#!/usr/bin/env python

from decouple import config
from imapclient import IMAPClient
from ssl import SSLCertVerificationError
import unittest

class IMAPProbe:
    ''' Probe IMAP server for testing purposes. '''

    def __init__(self):
        self.host   = config('IMAP_HOST')
        self.port   = config('IMAP_PORT')
        self.user   = config('IMAP_USER')
        self.passwd = config('IMAP_PASSWD')

    def verify_tls(self):
        try:
            server = IMAPClient(self.host, self.port)
            print(f"{server.host} {server.port} Connection OK")
            server.shutdown()
            return True

        except SSLCertVerificationError as error:
            print(f"{self.host} {self.port} {error}")
            return False

        except ConnectionRefusedError as error:
            print(f"{self.host} {self.port} {error}")
            return False
   
        except Exception as error:
            print(f"{type(error)} {error}")    
            return False

    def verify_auth(self):
        try:
            server = IMAPClient(self.host, self.port)
            server.login(self.user, self.passwd)
            server.shutdown()
            print(f"{server.host} {server.port} Login OK")

        except:
            server.shutdown()


class TestImapConnections(unittest.TestCase):

    def setUp(self):
        print(f"\nstart: {self.shortDescription()}")

    def tearDown(self):
        print(f"end: {self.shortDescription()}")

    def test_tls(self):
        """test imap tls"""
        server = IMAPProbe()
        self.assertTrue(server.verify_tls())

    def test_auth(self):
        """test imap auth"""
        server = IMAPProbe()
        self.assertFalse(server.verify_auth())

if __name__ == '__main__':
    unittest.main()
