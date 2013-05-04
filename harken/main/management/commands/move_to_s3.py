from django.core.management.base import BaseCommand
from harken.main.models import Url, Response
import boto
from boto.s3.key import Key
from django.conf import settings


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        conn = boto.connect_s3(
            settings.AWS_ACCESS_KEY,
            settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket("thraxil-harken-urls")
        total = Url.objects.all().count()
        cnt = 0
        for url in Url.objects.all():
            print "[%d/%d] %s " % (cnt, total, url.url)
            try:
                k = Key(bucket)
                k.key = url.s3_key()
                k.set_contents_from_filename(url.path())
            except Exception, e:
                print "error uploading: %s" % str(e)
            cnt += 1
        bucket = conn.get_bucket("thraxil-harken-responses")
        total = Response.objects.all().count()
        cnt = 0
        for response in Response.objects.all():
            print "[%d/%d] %d" % (cnt, total, response.id)
            try:
                k = Key(bucket)
                k.key = response.s3_key()
                k.set_contents_from_filename(url.path())
            except Exception, e:
                print "error uploading: %s" % str(e)
            cnt += 1
