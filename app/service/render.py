# -*- coding: utf-8 -*-
# @author: ntischuk

import json
from functools import wraps

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def render_to(template):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0],
                            context_instance=RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output,
                            context_instance=RequestContext(request))
            elif output == None:
                return render_to_response(template, {},
                            context_instance=RequestContext(request))
            return output
        return wrapper
    return renderer

def render_json(func):
    def wrapper(request, *args, **kw):
        output = func(request, *args, **kw)
        if isinstance(output, (list, tuple, dict)):
            return HttpResponse(json.dumps(output, sort_keys=True),
                        mimetype='application/json')
        return output
    return wrapper