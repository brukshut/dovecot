#!/bin/bash

##
## install_packages.sh
##
PATH=/bin:/sbin:/usr/bin:/usr/sbin

## functions
function install_apt {
  DEBIAN_FRONTEND="noninteractive"
  apt-get update -y
  for pkg in python3 build-essential sudo rsync vim libssl-dev libpam0g-dev; do
    apt-get install $pkg -y
  done
}

function install_apk {
  for pkg in bash sudo vim rsync openssl; do
    apk add $pkg --update --no-cache
  done
}
## end functions

## main
[[ -e /etc/alpine-release ]] && install_apk
[[ -e /etc/debian_version ]] && install_apt
