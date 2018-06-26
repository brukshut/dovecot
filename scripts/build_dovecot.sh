#!/bin/bash -x

##
## build_dovecot.sh
## we will build dovecot ourselves, rather than use debian packages.
## we don't need exim4 and mysql to use dovecot.
##
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
NAME=dovecot
VERSION=2.3.1
URL=https://dovecot.org/releases/2.3/dovecot-2.3.1.tar.gz
CC=/usr/bin/gcc
CXX=/usr/bin/g++
LD=/usr/bin/ld
AS=/usr/bin/as
AR=/usr/bin/ar
CFLAGS="-I/usr/local/include -I/usr/local/include/openssl"
LDFLAGS="-Wl,-L/usr/local/lib -Wl,-rpath=/usr/local/lib"
export PATH CC LD AS AR CFLAGS LDFLAGS

## fetch and unpack tarball
wget $URL
tar xvf ${URL##*/}
cd ${NAME}-${VERSION}
./configure --prefix=/usr/local \
--localstatedir=/var/dovecot \
--sysconfdir=/etc \
--with-ssl=openssl \
--with-gnu-ld \
--with-pam \
--with-shadow \
--localstatedir=/var
/usr/bin/make
sudo /usr/bin/make install

## create dovecot users
sudo groupadd -g 143 dovecot
sudo useradd -u 143 -g dovecot -d /usr/local/share/dovecot -s /bin/false dovecot
sudo groupadd -g 144 dovenull
sudo useradd -u 144 -g dovenull -d /nonexistent -s /bin/false dovenull

## create configuration directory
## copy base configuration files
sudo mkdir /etc/dovecot
sudo rsync -av /usr/local/share/doc/dovecot/example-config/ /etc/dovecot/

## dovecot configuration
sudo mv /tmp/dovecot.conf /etc/dovecot/dovecot.conf
sudo mv /tmp/10-ssl.conf /etc/dovecot/conf.d/10-ssl.conf

## ssl certificate
sudo mkdir -p /data/ssl/dovecot
sudo mv /tmp/dovecot.pem /data/ssl/dovecot/dovecot.pem

## create state folder
sudo mkdir /var/dovecot
sudo chown dovecot:dovecot /var/dovecot

## cleanup
cd ..
rm ${URL##*/}
rm -rf ${NAME}-${VERSION}


