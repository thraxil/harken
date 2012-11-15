from django.db import models
from html2text import wrapwrite, html2text


class Response(models.Model):
    url = models.URLField()
    status = models.IntegerField(default=200)
    content_type = models.CharField(max_length=256, blank=True, default="")
    body = models.TextField(blank=True, null=True, default="")
    visited = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-visited"]

    def get_absolute_url(self):
        return "/response/%d/" % self.id

    def as_markdown(self):
        try:
            return html2text(self.body,self.url)
        except:
            return ""

    def substantial(self):
        return len(self.body) > 1024
