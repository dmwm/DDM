from django.template import Context, loader, RequestContext
from django.http import HttpResponse

def index(request):
    tmpl = loader.get_template("victorinterface/index.html")
    #cont = Context()
    cont = RequestContext(request)
    return HttpResponse(tmpl.render(cont))
