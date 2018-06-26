#!/bin/bash

##
## install_packages.sh
## libsasl2-dev --> sasl2 headers
## libdb5.3-dev --> berkeley db headers
##

PATH=/bin:/sbin:/usr/bin:/usr/sbin
DEBIAN_FRONTEND="noninteractive"

## install required packages
apt-get update -y
apt-get install build-essential -y
apt-get install git -y
apt-get install rsync -y
apt-get install man -y
apt-get install vim -y
apt-get install wget -y
apt-get install sudo -y

## dovecot requires this
sudo apt-get install libpam0g-dev -y
