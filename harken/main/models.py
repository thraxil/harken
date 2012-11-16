from django.db import models
from html2text import wrapwrite, html2text
from pysolr import Solr, SolrError

def add_to_solr(response):
    conn = Solr('http://worker.thraxil.org:8080/solr/')
    conn.add([
            dict(
                id="response:%d" % response.id,
                name=response.url,
                text=response.body,
                )
            ])

class Response(models.Model):
    url = models.URLField()
    status = models.IntegerField(default=200)
    content_type = models.CharField(max_length=256, blank=True, default="")
    body = models.TextField(blank=True, null=True, default="")
    length = models.IntegerField(default=0)
    visited = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-visited"]

    def get_absolute_url(self):
        return "/response/%d/" % self.id

    def is_html(self):
        return self.content_type.startswith("text/html")

    def as_markdown(self):
        try:
            return html2text(self.body,self.url)
        except:
            return "[error converting HTML to Text]"

    def substantial(self):
        return self.length > 1024
