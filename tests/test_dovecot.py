##
## dovecot tests (py.test)
##
def test_dovecot_is_installed(host):
    assert host.package("dovecot").is_installed

def test_user_is_present(host):
    assert 'dovecot' in host.user('dovecot').name

def test_serverpem_exists(host):
    assert host.file("/etc/dovecot/ssl/server.pem").exists

def test_serverkey_exists(host):
    assert host.file("/etc/dovecot/ssl/server.key").exists

def test_dhpem_exists(host):
    assert host.file("/etc/dovecot/ssl/dh.pem").exists


