from annoying.decorators import render_to
from harken.main.models import Response, add_to_solr
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from pysolr import Solr, SolrError


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
        r = Response.objects.create(
            url=request.POST['url'][:200],
            status=int(request.POST.get('status','200')),
            content_type=request.POST.get('content_type', ''),
            body=request.POST.get('body', ''),
            )
        add_to_solr(r)
        return HttpResponse("OK")
    return HttpResponse("POST only")


@render_to('main/response.html')
def response(request, id):
    r = Response.objects.get(id=id)
    return dict(response=r)

def extract_response(result):
    return Response.objects.get(id=result['id'].split(":")[1])
    

@render_to('main/search.html')
def search(request):
    query = request.GET.get('q', '')
    if not query:
        return dict(query=query)
    conn = Solr('http://worker.thraxil.org:8080/solr/')
    results = [extract_response(r) for r in conn.search(query)]
    return dict(query=query, responses=results)
