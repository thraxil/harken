from django.db import models
from pysolr import Solr
from django.conf import settings
import diff_match_patch
import nltk
import re
from topia.termextract import extract
import hashlib
import os.path
import os
import gzip
import boto
from boto.s3.key import Key
from cStringIO import StringIO
from gzip import GzipFile


def path_from_hash(sha1):
    """ convert from
    "8b7e052215635bfc2774e23dcb5c7aaadf81b42b"
    to
    "8b/7e/05/22/15/63/5b/fc/27/74/e2/3d/cb/5c/7a/aa/df/81/b4/2b"
    """
    return os.path.join(*["%s%s" % (a, b) for (a, b)
                          in zip(sha1[::2], sha1[1::2])])


def add_to_solr(response, body):
    conn = Solr(settings.SOLR_BASE)
    conn.add([
            dict(
                id="response:%d" % response.id,
                name=response.url.url,
                text=body.encode('utf-8'),
                )
            ])


class Domain(models.Model):
    domain = models.CharField(max_length=256, db_index=True)

    def get_absolute_url(self):
        return "/domain/%d/" % self.id


def allow_term(t):
    if len(t) < 3:
        return False
    if len(t) > 32:
        return False
    t = t.decode('utf-8', 'ignore')
    disallowed = [
        u"\u2019", u'\u201c', u'\u201d', u'\u2014',
        '/', '"', ')', ';', '\\', '|', '$',
        '+', '(', '[', ']', '{', '}', '@',
        '&', '%', '=', '*', '#',
        ]
    for c in disallowed:
        if c in t:
            return False

    if t == 'class':
        return False
    return True


def normalize_term(term):
    return term[0].lower()


def sha1hash(content):
    sha1 = hashlib.sha1()
    sha1.update(content.encode('utf-8'))
    return sha1.hexdigest()


def terms(content):
    raw = nltk.clean_html(content.encode('utf-8'))
    extractor = extract.TermExtractor()
    all_terms = list(reversed(sorted([t for t in extractor(raw)
                                      if allow_term(t[0])],
                                     key=lambda x: x[1])))
    return [normalize_term(t) for t in all_terms][:20]


class GZipper(object):
    def __init__(self, obj):
        self.obj = obj

    def write_gzip(self, content):
        p = self.obj.path()
        try:
            os.makedirs(os.path.dirname(p))
        except:
            pass
        f = gzip.open(p, 'wb')
        f.write(content.encode('utf-8'))
        f.close()

        # upload to S3 as well
        conn = boto.connect_s3(
            settings.AWS_ACCESS_KEY,
            settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket(self.obj.s3_bucket_name())
        k = Key(bucket)
        k.key = self.obj.s3_key()
        sio = StringIO()
        gzf = GzipFile(fileobj=sio, mode='wb')
        gzf.write(content.encode('utf-8'))
        gzf.close()
        k.set_contents_from_file(sio.getvalue())

    def read_gzip(self):
        p = self.obj.path()
        f = gzip.open(p, 'rb')
        file_content = f.read()
        f.close()
        return file_content


class Url(models.Model):
    url = models.URLField(db_index=True)
    content_type = models.CharField(max_length=256, blank=True, default="")
    domain = models.ForeignKey(Domain)
    sha1hash = models.CharField(max_length=64)

    def get_absolute_url(self):
        return "/url/%d/" % self.id

    def get_content(self):
        return self.read_gzip()

    def get_patch(self, content=""):
        """ return a text patch of the supplied content against
        existing content """
        dmp = diff_match_patch.diff_match_patch()
        return dmp.patch_toText(
            dmp.patch_make(
                self.get_content().decode('utf-8'),
                content.encode('ascii', 'xmlcharrefreplace'),
                )
            )

    def path(self):
        return os.path.join(
            settings.MEDIA_ROOT,
            path_from_hash(self.sha1hash),
            "content.gz"
            )

    def write_gzip(self, content):
        GZipper(self).write_gzip(content)

    def read_gzip(self):
        return GZipper(self).read_gzip()

    def s3_bucket_name(self):
        return "thraxil-harken-urls"

    def s3_key(self):
        return "%s/content.gz" % self.sha1hash


class Term(models.Model):
    term = models.CharField(max_length=256, db_index=True)

    class Meta:
        ordering = ['term', ]

    def get_absolute_url(self):
        return "/term/%d/" % self.id


class UrlTerm(models.Model):
    url = models.ForeignKey(Url)
    term = models.ForeignKey(Term)


class Response(models.Model):
    url = models.ForeignKey(Url)
    length = models.IntegerField(default=0)
    visited = models.DateTimeField(auto_now_add=True)
    sha1hash = models.CharField(max_length=64)

    class Meta:
        ordering = ["-visited"]

    def get_absolute_url(self):
        return "/response/%d/" % self.id

    def is_html(self):
        return self.url.content_type.startswith("text/html")

    def as_markdown(self):
        try:
            return nltk.clean_html(self.body())
        except Exception, e:
            return "[error converting HTML to Text: %s]" % str(e)

    def clean_text(self):
        text = nltk.clean_html(self.body())
        return re.sub(r'\s{2,}', '\n\n', text)

    def get_patch(self):
        return self.read_gzip()

    def body(self):
        dmp = diff_match_patch.diff_match_patch()
        return dmp.patch_apply(
            dmp.patch_fromText(self.get_patch().decode('utf-8')),
            self.url.get_content().decode('utf-8'))[0]

    def path(self):
        return os.path.join(
            settings.MEDIA_ROOT,
            path_from_hash(self.sha1hash),
            "patch.gz"
            )

    def write_gzip(self, content):
        GZipper(self).write_gzip(content)

    def read_gzip(self):
        return GZipper(self).read_gzip()

    def s3_bucket_name(self):
        return "thraxil-harken-responses"

    def s3_key(self):
        return "%s/patch.gz" % self.sha1hash
