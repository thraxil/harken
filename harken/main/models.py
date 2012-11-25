from django.db import models
from html2text import html2text
from pysolr import Solr
import diff_match_patch
import nltk
import re
from topia.termextract import extract


def add_to_solr(response, body):
    conn = Solr('http://worker.thraxil.org:8080/solr/')
    conn.add([
            dict(
                id="response:%d" % response.id,
                name=response.url.url,
                text=body,
                )
            ])


class Domain(models.Model):
    domain = models.CharField(max_length=256, db_index=True)

    def get_absolute_url(self):
        return "/domain/%d/" % self.id


def allow_term(t):
    if u"\u2019" in t[0]:
        return False
    if u'\u201c' in t[0]:
        return False
    if u'\u201d' in t[0]:
        return False
    if u'\u2014' in t[0]:
        return False
    if '/' in t[0]:
        return False
    if '"' in t[0]:
        return False
    if ')' in t[0]:
        return False
    if ';' in t[0]:
        return False
    if '\\' in t[0]:
        return False
    if '\xe2' in t[0]:
        return False
    if '|' in t[0]:
        return False
    if len(t[0]) < 3:
        return False
    if len(t[0]) > 32:
        return False
    if t[0] == 'class':
        return False
    return True


def normalize_term(term):
    return term[0].lower()


class Url(models.Model):
    url = models.URLField(db_index=True)
    content = models.TextField(blank=True, null=True, default="")
    content_type = models.CharField(max_length=256, blank=True, default="")
    domain = models.ForeignKey(Domain)

    def get_absolute_url(self):
        return "/url/%d/" % self.id

    def get_patch(self, content=""):
        """ return a text patch of the supplied content against
        existing content """
        dmp = diff_match_patch.diff_match_patch()
        return dmp.patch_toText(dmp.patch_make(self.content, content))

    def terms(self):
        raw = nltk.clean_html(self.content)
        extractor = extract.TermExtractor()
        all_terms = list(reversed(sorted([t for t in extractor(raw)
                            if allow_term(t)],
                           key=lambda x: x[1])))
        return [normalize_term(t) for t in all_terms][:20]


class Term(models.Model):
    term = models.CharField(max_length=256, db_index=True)

    class Meta:
        ordering = ['term',]

    def get_absolute_url(self):
        return "/term/%d/" % self.id


class UrlTerm(models.Model):
    url = models.ForeignKey(Url)
    term = models.ForeignKey(Term)


class Response(models.Model):
    url = models.ForeignKey(Url)
    status = models.IntegerField(default=200)
    patch = models.TextField(blank=True, null=True, default="")
    length = models.IntegerField(default=0)
    visited = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-visited"]

    def get_absolute_url(self):
        return "/response/%d/" % self.id

    def is_html(self):
        return self.url.content_type.startswith("text/html")

    def as_markdown(self):
        try:
            return nltk.clean_html(self.body())
#            return html2text(self.body(), self.url.url)
        except Exception, e:
            return "[error converting HTML to Text: %s]" % str(e)

    def clean_text(self):
        text = nltk.clean_html(self.body())
        return re.sub(r'\s{2,}', '\n\n', text)
        

    def body(self):
        dmp = diff_match_patch.diff_match_patch()
        return dmp.patch_apply(dmp.patch_fromText(self.patch),
                               self.url.content)[0]
