import zmq
from json import loads
from django.core.management.base import BaseCommand
from restclient import POST

PUB_SOCKET = "tcp://localhost:6666"
HARKEN_SERVER = "http://harken.thraxil.org/add/"


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
                print message['content_type'], message['url']
                r = POST(HARKEN_SERVER, params=message, async=False)
                if r != "OK":
                    with open("/tmp/error.html", "w") as outfile:
                        outfile.write(r)
                        print "wrote out error"
            except ValueError:
                pass
