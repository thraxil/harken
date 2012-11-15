import sys
import zmq
from json import loads
from django.core.management.base import BaseCommand
from django.conf import settings
import os
import os.path
from datetime import datetime, timedelta
from restclient import POST

PUB_SOCKET = "tcp://localhost:6666"
HARKEN_SERVER = "http://localhost:9999/add/"

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(PUB_SOCKET)
socket.setsockopt(zmq.SUBSCRIBE, "")


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        while True:
            d = socket.recv()
            try:
                message = loads(d)
                if message['status'] == 200:
                    print message['status'], message['content_type'], message['url']
                else:
                    print message['status'], message['url']
                r = POST(HARKEN_SERVER,params=message, async=False)
                if r != "OK":
                    with open("/tmp/error.html", "w") as outfile:
                        outfile.write(r)
                        print "wrote out error"
            except ValueError:
                print "json error: "
                print str(d)
