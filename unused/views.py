# -*- coding: utf-8 -*-
# @author: ntischuk


from django.http import Http404
from django.template import TemplateDoesNotExist
from django.views.generic.simple import direct_to_template

from app.service.render import *
from unused.service.grabbing import Pages, Website


def home(request):
    try:
        return direct_to_template(request, template="unused/home.html")
    except TemplateDoesNotExist:
        raise Http404()

@render_to('unused/task.html')
def task(request):
    return {}

@render_json
def get(request, type):
    result = {'result':False}
    if request.method == 'POST':
        unused = {}
        if type == 'website':
            link  = request.POST.get('url', None)
            depth = request.POST.get('depth', 0)
            unused = Website().grabbing(link, depth)
        elif type == 'pages':
            links = request.POST.getlist('links[]')
            unused = Pages().grabbing(links)
            
        if len(unused) > 0:
            result.update({'type':type, 'result':True, 'unused':unused})
    
    return result