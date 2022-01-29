FROM alpine:latest
RUN apk add --update --no-cache dovecot
RUN mkdir /etc/dovecot/ssl && chown -R dovecot:dovecot /etc/dovecot/ssl 
RUN mkdir /var/run/dovecot && chown -R dovecot /var/run/dovecot
RUN mkdir /var/lib/dovecot && chown -R dovecot /var/lib/dovecot
RUN apk add --update --no-cache bash sudo vim
USER root 
WORKDIR /var/run/dovecot
ADD files/dovecot.conf files/users /etc/dovecot
ADD files/10-master.conf files/10-ssl.conf /etc/dovecot/conf.d
ENV HOSTNAME mail.gturn.xyz
EXPOSE 993
LABEL version=2.3.17.1
CMD ["/usr/sbin/dovecot", "-F"]
