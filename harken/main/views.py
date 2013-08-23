from annoying.decorators import render_to
from harken.main.models import Response, Url, Domain
from harken.main.models import Term
from harken.main.tasks import add_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from pysolr import Solr
import calendar


@login_required
@render_to('main/index.html')
def index(request, page=1):
    response_list = Response.objects.all()
    p = Paginator(response_list, 200)
    try:
        responses = p.page(page)
    except PageNotAnInteger:
        responses = p.page(1)
    except EmptyPage:
        responses = p.page(p.num_pages)
    return dict(responses=responses.object_list,
                paginator=responses)


def add(request):
    if request.method == "POST":
        add_response.delay(
            url=request.POST.get('url', ''),
            body=request.POST.get('body', ''),
            content_type=request.POST.get('content_type', ''),
        )
        return HttpResponse("OK")
    return HttpResponse("POST only")


@login_required
@render_to('main/response.html')
def response(request, id):
    r = Response.objects.get(id=id)
    return dict(response=r)


@login_required
@render_to('main/response_year_archive.html')
def response_year_archive(request, year=2012):
    responses = Response.objects.filter(visited__year=year)
    month_names = ["January", "February", "March", "April",
                   "May", "June", "July", "August", "September",
                   "October", "November", "December"]
    months = []
    for i, m in enumerate(month_names):
        months.append(
            dict(
                count=responses.filter(visited__month=i + 1).count(),
                month=i + 1,
                name=m))
    return dict(responses=responses, months=months, year=year)


@login_required
@render_to('main/response_month_archive.html')
def response_month_archive(request, year=2012, month=1):
    responses = Response.objects.filter(
        visited__year=year,
        visited__month=month,
    )
    days = []
    for day in calendar.Calendar().itermonthdays(int(year), int(month)):
        if day == 0:
            continue
        days.append(
            dict(
                day=day,
                count=responses.filter(visited__day=day).count(),
            ))
    return dict(responses=responses, days=days, month=month, year=year)


@login_required
@render_to('main/response_day_archive.html')
def response_day_archive(request, year=2012, month=1, day=1):
    responses = Response.objects.filter(
        visited__year=year,
        visited__month=month,
        visited__day=day,
    )
    return dict(responses=responses, year=year, month=month, day=day)


@login_required
def response_raw(request, id):
    r = Response.objects.get(id=id)
    return HttpResponse(r.body(), content_type="text/plain")


@login_required
def response_patch(request, id):
    r = Response.objects.get(id=id)
    return HttpResponse(r.get_patch(), content_type="text/plain")


@login_required
def delete_response(request, id):
    if request.method == "POST":
        r = Response.objects.get(id=id)
        conn = Solr(settings.SOLR_BASE)
        conn.delete("result:%d" % r.id)
        r.delete()
    return HttpResponseRedirect("/")


@login_required
def delete_url(request, id):
    if request.method == "POST":
        u = Url.objects.get(id=id)
        for r in u.response_set.all():
            conn = Solr(settings.SOLR_BASE)
            conn.delete("result:%d" % r.id)
            r.delete()
        u.delete()
    return HttpResponseRedirect("/")


@login_required
def delete_domain(request, id):
    d = Domain.objects.get(id=id)
    if request.method == "POST":
        for u in d.url_set.all():
            for r in u.response_set.all():
                conn = Solr(settings.SOLR_BASE)
                conn.delete("result:%d" % r.id)
                r.delete()
            u.delete()
        d.delete()
    return HttpResponseRedirect("/")


@login_required
@render_to('main/url.html')
def url_view(request, id):
    u = Url.objects.get(id=id)
    return dict(url=u)


@login_required
@render_to('main/domain.html')
def domain(request, id):
    d = Domain.objects.get(id=id)
    return dict(domain=d)


@login_required
@render_to('main/domains.html')
def domain_index(request):
    return dict(domains=Domain.objects.all())


def extract_response(result):
    try:
        return Response.objects.get(id=result['id'].split(":")[1])
    except Response.DoesNotExist:
        return None


@login_required
@render_to('main/search.html')
def search(request):
    query = request.GET.get('q', '')
    if not query:
        return dict(query=query)
    conn = Solr(settings.SOLR_BASE)
    results = [res for res in [extract_response(r) for r in conn.search(query)]
               if res is not None]
    return dict(query=query, responses=results)


@login_required
@render_to('main/term.html')
def term(request, id):
    d = Term.objects.get(id=id)
    return dict(term=d)


@login_required
@render_to('main/terms.html')
def term_index(request):
    return dict(terms=Term.objects.all())


@login_required
def delete_term(request, id):
    t = Term.objects.get(id=id)
    if request.method == "POST":
        t.urlterm_set.all().delete()
        t.delete()
    return HttpResponseRedirect("/term/")
