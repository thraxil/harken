from django.core.management.base import BaseCommand
from harken.main.models import Url, Term, UrlTerm

class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **kwargs):
        for url in Url.objects.all():
            print url.url
            for t in url.terms():
                term, _ = Term.objects.get_or_create(term=t[:200])
                urlterm, _ = UrlTerm.objects.get_or_create(term=term, url=url)
