from django.http import HttpResponse
import json

from overpass.utils import *

def location(request):

    if request.method == 'POST':
        country = request.POST.get('country','')
        level = request.POST.get('level','')

    elif request.method == 'GET':
        country = request.GET.get('country','')
        level = request.GET.get('level','')

    if(country and level):
        result = osm_get_all_name(country, level)
        response = HttpResponse(json.dumps(result), content_type='application/json')
    else:
        context = {
            'status': '400', 'reason': 'Parameter country , level are required'
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400

    return response

def location_geom(request):

    if request.method == 'POST':
        location = request.POST.get('location','')
        country = request.POST.get('country','')
        level = request.POST.get('level','')

    elif request.method == 'GET':
        location = request.GET.get('location','')
        country = request.GET.get('country','')
        level = request.GET.get('level','')

    if(location and country and level):
        result = osm_get_multipolygon_for_location(location, country, level)
        response = HttpResponse(json.dumps(result), content_type='application/json')
    else:
        context = {
            'status': '400', 'reason': 'Parameter location , country , level are required'
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400

    return response


def location_id(request):

    if request.method == 'POST':
        location = request.POST.get('location','')
        country = request.POST.get('country','')

    elif request.method == 'GET':
        location = request.GET.get('location','')
        country = request.GET.get('country','')

    if(location and country and level):
        result = osm_get_node_id_for_location(location, country)
        response = HttpResponse(json.dumps(result), content_type='application/json')
    else:
        context = {
            'status': '400', 'reason': 'Parameter location , country are required'
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400

    return response
