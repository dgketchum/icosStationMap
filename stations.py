# -*- coding: utf-8 -*-
"""
running this script saves a html file in the current
directory with a map based on leaflet.js. 
The map contains all ICOS NEON AMERIFLUC and LTER/DEIMS stations
dynamically loaded from their respective webservices.

@author: Claudio D'Onofrio
"""

__version__ = "0.1.0"

#--------------------------------------------------------------
import sys
import helper_functions as h

# set the list of necessary modules to run the code
modules = ['os', 'webbrowser', 'folium', 'icos', 'neon', 'ameriflux', 'lter', 'fluxnet']

# check if the modules are available and load them, otherwise stop execution
if not h.checklib(modules):
    sys.exit('module dependencies are not fulfilled')

else:
    import os
    import webbrowser
    import folium            
    import icos
    import neon
    import ameriflux
    import lter
    import fluxnet
    import asiaflux
    from tqdm import tqdm

dbg = True

networklist = {'icos', 'neon','ameriflux','lter','fluxnet','asiaflux'}

mcList = [] # Marker Cluster List
for n in tqdm(networklist):
    # get the marker cluster
    h.debugPrint(dbg, ''.join(['processing ',n]))
    mcList.append(eval(n+'.sites_marker_list()'))

#-----------------------------------------------------------------
# create a map with all stations
# define the initinal paramters of centre point and zoom
h.debugPrint(dbg,'creating map with markers')


Center = [43, 5]
Zoom = 4

#create the map
myMap = folium.Map(
        location=Center,
        zoom_start=Zoom,
        no_wrap=True
        )

#---------------------------------------------------------------
# add tiles, to see what kind of basemap you like
# tile layers will be displayed in the top right 
# menu. You can easyly switch 

folium.TileLayer('openstreetmap').add_to(myMap)
folium.TileLayer('cartodbpositron').add_to(myMap)
folium.TileLayer('cartodbdark_matter').add_to(myMap)
folium.TileLayer('stamenwatercolor').add_to(myMap)
folium.TileLayer('stamentoner').add_to(myMap)
folium.TileLayer('stamenterrain').add_to(myMap)
folium.TileLayer('Mapbox Control Room').add_to(myMap)
folium.TileLayer('Mapbox Bright').add_to(myMap)

#---------------------------------------------------------------
# create the feature groups and add control
# feature groups will be displayed as well in the
# top right menu. You can easly switch on/off 
# the different layers.

#fgList = []
for i, n in tqdm(enumerate(networklist)):
    f = eval(''.join(['folium.FeatureGroup(name="',n,'")']))
    eval('f.add_child(mcList[i]).add_to(myMap)')

#for i, f in enumerate(fgList):
#    eval('f.add_child(mcList[i]).add_to(myMap)')

folium.LayerControl().add_to(myMap)
#---------------------------------------------------------------
# now choose a name and safe the map to your local computer
mapname = 'stations.html'
myMap.save(mapname)

url = os.path.abspath(mapname)
h.debugPrint(dbg,('map saved to: ' + url))
# open the saved html with default browser

# the html file is now saved to the directory where your code is
# let's try to open your default browser with the map.
webbrowser.open(url, new=2)


#----end of file -----------------------------------------------

