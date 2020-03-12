#!/usr/passagens_agent/python
# encoding=utf8

import paho.mqtt.client as mqtt
from varnish import VarnishManager
import logging
import sys
from logging.handlers import SysLogHandler
import time
from passagens_agent.wp_command import WpCommand

sys.path.append('/opt/passagens-agent/conf')
import config

from service import find_syslog, Service

CERTFILE = "/etc/ssl/certs/ca-bundle.trust.crt"

servers = [config.VARNISH_CONFIG['server']]
manager = VarnishManager(servers)


class PiManager(Service):
    def __init__(self, *args, **kwargs):
        super(PiManager, self).__init__(*args, **kwargs)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),
                               facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.INFO)
        self.wpcmd= WpCommand('wordpress')

    def run(self):

        f = open(config.VARNISH_CONFIG['secret_file'])
        varnishsecret = f.read().rstrip('\n')
        # The callback for when the client receives a CONNACK response from the server.

        def on_connect(client, userdata, flags, rc):
            self.logger.info("Connected with result code " + str(rc))

            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("passagens/varnish")

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            banurl = msg.payload
            self.logger.info("purging: {0}".format(banurl))
            self.logger.info("Clean object Cache")
            self.wpcmd.run("total-cache flush object")

            # print '%s: %s' % (m, m.get_body())
            manager.run('ban', 'req.url == /', secret=varnishsecret)
            manager.run('ban.url', banurl, secret=varnishsecret)
            manager.run('ban', 'req.url == %s' % banurl, secret=varnishsecret)
            self.logger.info("Purged page {0}".format(banurl))
            self.logger.info(msg.topic + " " + str(msg.payload))

        client = mqtt.Client()
        client.tls_set(CERTFILE)
        client.on_connect = on_connect
        client.on_message = on_message

        client.username_pw_set(config.QUEUE_CONFIG['user'], password=config.QUEUE_CONFIG['password'])
        client.connect(config.QUEUE_CONFIG['host'], config.QUEUE_CONFIG['port'], 60)
        client.loop_start()
        while not self.got_sigterm():
            time.sleep(5)

        client.loop_stop()
        client.disconnect()


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND' % sys.argv[0])

    cmd = sys.argv[1].lower()
    service = PiManager('passagens-agent', pid_dir='/var/run')

    if cmd == 'start':
        service.start()
    elif cmd == 'stop':
        service.stop()
    elif cmd == 'status':
        if service.is_running():
            print "Service is running."
        else:
            print "Service is not running."
    else:
        sys.exit('Unknown command "%s".' % cmd)
