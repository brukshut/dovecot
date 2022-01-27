def test_dovecot_is_listening(host):
    sock = host.socket("tcp://0.0.0.0:2993").is_listening
