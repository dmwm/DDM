from django.template import loader, RequestContext
from django.http import HttpResponse
from Apps.popCommon.database import popCommonDB
from Apps.popCommon.utils.confSettings import confSettings

#----------------------------------------------------------
# RENDERING VIEWS
#----------------------------------------------------------
popsettings = confSettings()
DBUSER = popsettings.getSetting("popularity", "DBUSER")


# This is a generic method to render an html template 
def renderTemplate(request, tmplPath='', contextRequests = {}):
    tmpl = loader.get_template(tmplPath)
    cont = RequestContext(request, contextRequests)
    return HttpResponse(tmpl.render(cont))

def tablesDoc(request):
    tmpl = loader.get_template("popularity/docexample.html")
    cont = RequestContext(request)
    return HttpResponse(tmpl.render(cont))    
