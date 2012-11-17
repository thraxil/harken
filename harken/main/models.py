from django.db import models
from html2text import wrapwrite, html2text
from pysolr import Solr, SolrError
import diff_match_patch

def add_to_solr(response):
    conn = Solr('http://worker.thraxil.org:8080/solr/')
    conn.add([
            dict(
                id="response:%d" % response.id,
                name=response.url.url,
                text=response.body,
                )
            ])

class Url(models.Model):
    url = models.URLField(db_index=True)
    content = models.TextField(blank=True, null=True, default="")
    content_type = models.CharField(max_length=256, blank=True, default="")

    def get_patch(self, content=""):
        """ return a text patch of the supplied content against
        existing content """
        dmp = diff_match_patch.diff_match_patch()
        return dmp.patch_toText(dmp.patch_make(self.content, content))


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
            return html2text(self.body,self.url.url)
        except Exception, e:
            return "[error converting HTML to Text: %s]" % str(e)

    def substantial(self):
        return self.length > 1024
