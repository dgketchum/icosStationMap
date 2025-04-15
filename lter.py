import requests
import folium
from folium.plugins import MarkerCluster
import helper_functions as h
import textile


def sites_marker_list():
    # ['network', 'lat', 'lon', 'country', 'sid', 'pi', 'desc']

    url = "https://deims.org/geoserver/deims/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=deims:ilter_all_formal&outputFormat=application%2Fjson"

    r = requests.get(url)
    lter = r.json()
    datatable = []

    for station in lter['features']:
        lat = station['properties']['field_coordinates_lat']
        lon = station['properties']['field_coordinates_lon']

        sid = station['properties']['name']

        if (h.is_number(lat) and h.is_number(lon)):
            l = ['lter']
            l += [float(lat)]
            l += [float(lon)]
            l += ['']
            l += [sid]
            l += ['']
            l += ['']

            assert len(l) == 7

            datatable.append(l)

    return datatable
