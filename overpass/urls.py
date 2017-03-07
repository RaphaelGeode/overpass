from django.conf.urls import url
from django.contrib import admin

from overpass.views import *

urlpatterns = [
    url(r'^location/', overpass.views.location, name='location'),
    url(r'^location_geom/', overpass.views.location_geom, name='location_geom'),
    url(r'^location_id/', overpass.views.location_id, name='location_id'),
]
