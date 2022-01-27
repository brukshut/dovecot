#!/usr/bin/env python

import sys
import re
import pexpect

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


test_dovecot_cert('localhost', 2993)
test_dovecot_cert('mail.gturn.xyz', 993)
test_dovecot_cert('mail.gturn.xyz', 3993)
test_dovecot_cert('localhost', 3993)
    

