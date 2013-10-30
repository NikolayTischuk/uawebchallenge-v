# -*- coding: utf-8 -*-
# @author: ntischuk


from django.http import Http404
from django.template import TemplateDoesNotExist
from django.views.generic.simple import direct_to_template

from app.service.render import render_json, render_to
from unused.service.grabbing import Pages, Website


def home(request):
    try:
        return direct_to_template(request, template="unused/home.html")
    except TemplateDoesNotExist:
        raise Http404()

@render_to('unused/task.html')
def task(request):
    return {}

@render_to('unused/pages.html')
def _pages(request):
    result = {}
    if request.method == 'POST':
        unused = {}
        links  = request.POST.getlist('link')
        unused = Pages().grabbing(links)
        if len(unused) > 0:
            result.update({'type':type, 'result':True, 'unused':unused})
    
    return result

@render_to('unused/website.html')
def _website(request):
    result = {}
    if request.method == 'POST':
        unused = {}
        links  = request.POST.getlist('link')
        unused = Pages().grabbing(links)
        if len(unused) > 0:
            result.update({'type':type, 'result':True, 'unused':unused})
    
    return result