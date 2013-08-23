from .models import Url, Response, Term, UrlTerm, Domain
from .models import add_to_solr, sha1hash
from .models import terms
from urlparse import urlparse
from celery import task


@task()
def add_response(url, body, content_type):
    url = url[:200]
    if len(body) < 1024:
        # ignore small ones
        return
    q = Url.objects.filter(url=url)
    u = None
    if q.count() == 0:
        netloc = urlparse(url).netloc.lower()
        d = None
        q2 = Domain.objects.filter(domain=netloc)
        if q2.count() == 0:
            d = Domain.objects.create(domain=netloc)
        else:
            d = q2[0]
        u = Url.objects.create(
            url=url,
            content_type=content_type,
            domain=d,
            sha1hash=sha1hash(body)
        )
        u.write_gzip(body)
        for t in terms(body):
            term, _ = Term.objects.get_or_create(term=t[:200])
            urlterm, _ = UrlTerm.objects.get_or_create(term=term, url=u)
    else:
        u = q[0]
    patch = u.get_patch(body)
    r = Response.objects.create(
        url=u,
        length=len(body),
        sha1hash=sha1hash(patch),
    )
    r.write_gzip(patch)
    add_to_solr(r, body)
