#!/usr/bin/env python

from decouple import config
from imapclient import IMAPClient
import mailbox
import os
import pexpect
import re
import sys
import shutil
from ssl import SSLCertVerificationError
import unittest
import testinfra

class IMAPTool:
    """Tool for testing IMAP."""

    def __init__(self):
        self.host   = config('IMAP_HOST')
        self.port   = config('IMAP_PORT')
        self.user   = config('IMAP_USER')
        self.passwd = config('IMAP_PASSWD')

    def test_dovecot_cert(host, port):
        openssl = "/usr/local/Cellar/openssl@1.1/1.1.1m/bin/openssl"
        cmd_opts = f"-brief -crlf -verify_return_error -verify_quiet -connect {host}:{port}"
        child = pexpect.spawn(f"openssl s_client {cmd_opts}")
        index = child.expect(['OK(.*)Dovecot ready(.*)', pexpect.EOF, pexpect.TIMEOUT])

        if index == 0:
            child.sendline('QUIT')
            print(f"{child.before.decode('utf-8')} {child.after.decode('utf-8')}")
            return

        if index == 1:
            resp = child.before.decode('utf-8')
            connect_err = re.compile('\r\nconnect:errno=.*\r\n')
            verify_err = re.compile('\r\nverify error:.*\r\n')

            if connect_err.findall(resp):        
                print(resp)
                return

            if verify_err.findall(resp):
                print(resp)
                return

        if index == 2:
            print("host timeout")


    def verify_tls(self):
        """Verify that IMAP TLS is working."""
        try:
            server = IMAPClient(self.host, self.port, ssl=True)
            print(server.welcome)
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
        """Verify that IMAP Auth is working."""
        try:
            server = IMAPClient(self.host, self.port, ssl=True)
            server.login(self.user, self.passwd)
            print(server.welcome)
            server.shutdown()
            return True

        except:
            server.shutdown()
            return False


    def verify_maildir(self):
        self.test_home = f"home/{config('IMAP_USER')}"
        shutil.rmtree(self.test_home, ignore_errors=True)
        os.makedirs(self.test_home)
        mailbox.Maildir(f"{self.test_home}/Maildir", create=True)
        server = IMAPClient(self.host, self.port, ssl=True)
        server.login(self.user, self.passwd)
        print(server.welcome)
        server.shutdown()
        return True


class IMAPTestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):
        print(f"\n>> start: {self.shortDescription()}")

    def tearDown(self):
        print(f">> end: {self.shortDescription()}\n")

    def test_tls(self):
        """test imap tls"""
        server = IMAPTool()
        self.assertTrue(server.verify_auth())

    def test_auth(self):
        """test imap auth"""
        server = IMAPTool()
        self.assertTrue(server.verify_auth())

    def test_maildir(self):
        """test imap maildir"""
        server = IMAPTool()
        self.assertTrue(server.verify_maildir())


class DovecotTestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):
        self.host = testinfra.get_host(f"docker://{config('CONTAINER_ID')}")
        print(f"\n>> start: {self.shortDescription()}")

    def tearDown(self):
        print(f">> end: {self.shortDescription()}\n")

    def test_dovecot_config(self):
        """test dovecot config"""
        self.assertEqual(self.host.run("/usr/sbin/dovecot -n").rc, 0)

    def test_dovecot_is_installed(self):
        """test if dovecot package is installed"""
        self.assertTrue(self.host.package("dovecot").is_installed)

    def test_user_is_present(self):
        """test if dovecot user exists"""
        self.assertTrue('dovecot' in self.host.user('dovecot').name)

    def test_serverpem_exists(self):
        """test if /etc/dovecot/ssl/server.pem exists"""
        pem = '/etc/dovecot/ssl/server.pem'
        if self.host.file(pem).content.decode('utf8'):
            print(self.host.file(pem).content.decode('utf8'))
        self.assertTrue(self.host.file(pem).exists)

    def test_serverkey_exists(self):
        """test if /etc/dovecot/ssl/server.key exists"""
        key = '/etc/dovecot/ssl/server.key'
        self.assertTrue(self.host.file(key).exists)
        if self.host.file(key).content.decode('utf8'):
            print(self.host.file(key).content.decode('utf8'))

    def test_dhpem_exists(self):
        """test if /etc/dovecot/ssl/dh.pem exists"""
        pem = '/etc/dovecot/ssl/dh.pem'
        self.assertTrue(self.host.file(pem).exists)
        print(self.host.file(pem).content.decode('utf8'))


if __name__ == '__main__':
    unittest.main()
