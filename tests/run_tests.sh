#!/bin/bash

##
## run dovecot tests
##
PATH=/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:

docker-compose up -d
export CONTAINER_ID=$(docker ps --filter name=dovecot_dovecot --format '{{.ID}}')
echo $CONTAINER_ID

/usr/bin/python3 -m unittest test_imap.py
docker-compose down
