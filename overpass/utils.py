import json
import requests

from django.contrib.gis.geos import Point, LinearRing, Polygon, MultiPolygon, GEOSGeometry

def osm_get_all_location(country="België - Belgique - Belgien", lev=8):
    url = 'http://overpass-api.de/api/interpreter'
    query = '[out:json];area[name="'+str(country)+'"];(rel[admin_level='+str(lev)+'][boundary=administrative](area););out;'
    payload = {'data':query}
    r = requests.post(url, payload)

    if r.status_code == 200:
        r.encoding = 'utf-8'
        try:
            recup = json.loads(r.text)
            towns = []
            for el in recup.get('elements'):
                towns.append(el.get('tags').get('name'))
            return towns
        except Exception as e:
            print('Decoding JSON has failed')
            print(str(e))
    return False

def osm_get_node_id_for_location(location, country="Belgium"):
    url = 'http://overpass-api.de/api/interpreter'
    query = '[out:json];node["is_in:country"="'+str(country)+'"][name="'+str(location)+'"];out ids;'
    payload = {'data':query}
    r = requests.post(url, payload)

    if r.status_code == 200:
        r.encoding = 'utf-8'
        try:
            recup = json.loads(r.text)
            if len(recup.get('elements')) == 1:
                return recup.get('elements')[0]['id']
            else:
                return False
        except Exception as e:
            print('Decoding JSON has failed')
            print(str(e))
    return False

def osm_get_multipolygon_for_location(location, country="België - Belgique - Belgien", level=8):

    url = 'http://overpass-api.de/api/interpreter'
    query = '[out:json];area[name="'+str(country)+'"];(rel[name="'+str(location)+'"][admin_level='+str(level)+'][boundary=administrative](area););out geom;'
    payload = {'data':query}
    r = requests.post(url, payload)

    if r.status_code == 200:
        r.encoding = 'utf-8'
        try:
            recup = json.loads(r.text)
            if 'elements' in recup.keys():
                elements = recup.get('elements')
                for el in elements:
                    if 'members' in el.keys():
                        members = el.get('members')
                        ways = []
                        for m in members:
                            if 'geometry' in m.keys() and m.get("type") == "way":
                                ways.append(m.get('geometry'))
                        points = order_ways(ways)
                        points.append(points[0])
                        line = LinearRing(points)

                        return Polygon(line)


            print("Location found but can't make the boundary")
            print("Query sent to OSM : {}".format(query))
            print("OSM response : {}".format(recup))
            return False
        except Exception as e:
            print('osm_get_multipolygon_for_location() : Decoding JSON has failed')
            print(str(e))
    else:
        print("Query sent to OSM : {}".format(query))
        print('HTTP {} status code'.format(r.status_code))
        print("No data found")

    return False

def osm_get_multipolygon_for_location_general(location, country="Belgium", level=8):

    url = 'http://overpass-api.de/api/interpreter'
    query = '[out:json];node["is_in:country"="'+str(country)+'"][name="'+location+'"];<;out geom;'
    payload = {'data':query}
    r = requests.post(url, payload)

    if r.status_code == 200:
        r.encoding = 'utf-8'
        try:
            recup = json.loads(r.text)
            if 'elements' in recup.keys():
                elements = recup.get('elements')
                for el in elements:
                    if 'tags' in el.keys():
                        tags = el.get('tags')
                        if 'admin_level' in tags:
                            if tags.get('admin_level') == level:
                                if 'members' in el.keys():
                                    members = el.get('members')
                                    ways = []
                                    for m in members:
                                        if 'geometry' in m.keys() and m.get("type") == "way":
                                            ways.append(m.get('geometry'))
                                    points = order_ways(ways)
                                    points.append(points[0])
                                    line = LinearRing(points)
                                    polygon = Polygon(line)
                                    multipolygon = MultiPolygon(polygon)
                                    return multipolygon

            print("Location found but can't make the boundary")
            return False
        except Exception as e:
            print('osm_get_multipolygon_for_location_general() : Decoding JSON has failed')
            print(str(e))
    else:
        print("No data found")

    return False

def osm_get_multipolygon_for_rel_id(id, level=8):
    url = 'http://overpass-api.de/api/interpreter'
    query = '[out:json];rel('+str(id)+');out geom;'
    payload = {'data':query}
    r = requests.post(url, payload)
    info = []
    if r.status_code == 200:
        r.encoding = 'utf-8'
        try:
            recup = json.loads(r.text)
            if 'elements' in recup.keys():
                elements = recup.get('elements')
                for el in elements:
                    if 'tags' in el.keys():
                        tags = el.get('tags')
                        if 'admin_level' in tags:
                            if tags.get('admin_level') == str(level):
                                info.append(str(tags.get('name')))
                                if 'members' in el.keys():
                                    members = el.get('members')
                                    ways = []
                                    for m in members:
                                        if 'geometry' in m.keys() and m.get("type") == "way":
                                            ways.append(m.get('geometry'))
                                    points = order_ways(ways)
                                    points.append(points[0])
                                    line = LinearRing(points)
                                    info.append(Polygon(line))
                                    return info

            print("Town found but can't make the boundary")
            return False
        except Exception as e:
            print('osm_get_multipolygon_for_rel_id(id) : Decoding JSON has failed')
            print(str(e))
    else:
        print("No data found id")

    return False

def osm_get_subarea_id_for_location_level(location, country="Belgium", level=8):

    url = 'http://overpass-api.de/api/interpreter'
    query = '[out:json];node["is_in:country"="'+str(country)+'"][name="'+location+'"];<;out geom;'
    payload = {'data':query}
    r = requests.post(url, payload)

    area = []

    if r.status_code == 200:
        r.encoding = 'utf-8'
        try:
            recup = json.loads(r.text)
            if 'elements' in recup.keys():
                elements = recup.get('elements')
                for el in elements:
                    if 'tags' in el.keys():
                        tags = el.get('tags')
                        if 'admin_level' in tags:
                            if tags.get('admin_level') == str(level):
                                if 'members' in el.keys():
                                    members = el.get('members')

                                    for m in members:
                                        if 'role' in m.keys() and m.get("role") == "subarea" and 'ref' in m.keys():
                                            area.append(m.get('ref'))
                                    return area

            print("Location found but can't find elements in it")
            return area
        except Exception as e:
            print('osm_get_subarea_id_for_location_level() : Decoding JSON has failed')
            print(str(e))
    else:
        print("No data found")

    return area


#return a array of Point ordered
def order_ways(ways):
    ways2 = ways.copy()
    waystmp = []

    pstart = Point(ways[0][0].get('lon'), ways[0][0].get('lat'))
    p0 = Point(ways[0][0].get('lon'), ways[0][0].get('lat'))

    while len(ways) > 0:
        for way in ways:
            p1 = Point(way[0].get('lon'), way[0].get('lat'))
            p2 = Point(way[-1].get('lon'), way[-1].get('lat'))

            if p0 == p1:
                for point in way:
                    p = Point(point.get('lon'), point.get('lat'))
                    waystmp.append(p)
                ways2.remove(way)
                p0 = p2
            elif p0 == p2:
                for point in reversed(way):
                    p = Point(point.get('lon'), point.get('lat'))
                    waystmp.append(p)
                ways2.remove(way)
                p0 = p1

            ways = ways2.copy()

    return waystmp
