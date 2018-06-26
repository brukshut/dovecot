#!/bin/bash

##
## build openssl
##
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
NAME=openssl
VERSION=1.0.2o
URL=https://www.openssl.org/source/${NAME}-${VERSION}.tar.gz
CC=/usr/bin/gcc
CXX=/usr/bin/g++
LD=/usr/bin/ld
AS=/usr/bin/as
AR=/usr/bin/ar
CFLAGS=-fPIC
export CFLAGS PATH CC CXX LD AS AR

## fetch and unpack
wget $URL
tar xzvf ${URL##*/}

## compile
cd ${NAME}-${VERSION}
./config --prefix=/usr/local shared
/usr/bin/make
sudo /usr/bin/make install

## cleanup
cd ..
rm ${URL##*/}
rm -rf ${NAME}-${VERSION}
