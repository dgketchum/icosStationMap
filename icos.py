# -*- coding: utf-8 -*-
"""
running this script saves a html file in the current
directory with a map based on leaflet.js. 
The map contains all ICOS stations and all NEON sites
dynamically loaded from their respective webservices.

@author: Claudio D'Onofrio
"""

#--------------------------------------------------------------
import sys
import helper_functions as h

# set the list of necessary modules to run the code
modules = ["requests", "folium", "textile"]

# check if the modules are available and load them, otherwise stop execution
if not h.checklib(modules):
    sys.exit("module dependencies are not fulfilled")

else:
    import textile
    import folium    
    from folium.plugins import MarkerCluster
    import requests

def sites_marker_list(*checkUrl):
    """
        get all the sites return MarkerCluster
        (to be added to a folium map.)
        Input: checkLnk [0|1]
        by default (if no argument is provided, we assume the value "False", 
        hence the url provided from ameriflux are considered valid.
        If checkLnk is "True", ech station url is checked for response "200 OK"
    """
    checkLnk = False
    if (len(checkUrl)):
        checkLnk = checkUrl
        
    # Query the ICOS SPARQL endpoint for a station list
    # output is an object "data" containing the results in JSON
    # the SPARQL query itself is in the helperFunctions...
    #------------------------------------------------------------------------
    # get ALL icos stations, see documentation in helper_functions
    
    url = 'https://meta.icos-cp.eu/sparql'
    r = requests.get(url, params={
        'format': 'json',
        'query': h.icos_stations()})
    
    data = r.json()
    #------------------------------------------------------------------------

    # convert the the result into a table
    # output is an array, where each row contains
    # information about the station
    
    cols = data['head']['vars']
    datatable = []
    
    for row in data['results']['bindings']:
        item = []
        for c in cols:
            item.append(row.get(c, {}).get('value'))
    
        datatable.append(item)
    
    # print the table if you want
    # icosdt = pd.DataFrame(datatable, columns=cols)
    # icosdt.head(5)
    
    # create a MarkerCluster for all the ICOS sites
    
    mc = MarkerCluster()   
       
    # loop through the ICOS datatable and create the markers
    for station in datatable:
    
        # check if lat, lon are numbers, otherwise skip the station
        if (h.is_number(station[0])) and (h.is_number(station[1])):
            #create the markers
            msg = '<table border=0>'
            msg += '<tr><td>Network: </td><td>ICOS</td></tr>'
            msg += '<tr><td>Country: </td><td>' + station[3] + '</td></tr>'
            msg += '<tr><td>Code: </td><td>' + srcLink(station, checkLnk) + '</td></tr>'
            msg += '<tr><td>Name: </td><td>' + station[5] + '</td></tr>'
            msg += '<tr><td>Theme: </td><td>' + station[2] + '</td></tr>'
            msg += '<tr><td>Latitude: </td><td>' + station[0] + '</td></tr>'
            msg += '<tr><td>Longitude: </td><td>' + station[1] + '</td></tr>'
            msg += '</table>'         
            msg = textile.textile(msg)
            
            #create a marker to display the station on the map
            marker = folium.Marker(                    
                    location=[float(station[0]), float(station[1])],
                    popup=msg).add_to(mc)
            
            # check which icon we should use
            if(station[2] == "AS"):
                marker.add_child(folium.Icon(color = 'lightblue', icon='cloud'))
            elif(station[2] == "ES"):
                marker.add_child(folium.Icon(color = 'green', icon='leaf'))
            elif(station[2] == "OS"):
                marker.add_child(folium.Icon(color = 'blue', icon='tint'))
                
            # add the marker to the "marker cluster"
            mc.add_child(marker)
    return mc
#---EOF DEF----------------------------------------------------------
            
            
def srcLink(station, checkLnk):
    """
        Assemble a string as http src link with the station code
        The result should be a valid link to the 'landing page of the site.
        The link is checked for validity (http return 200)
    """
    
    # create a link to the stations landing page
    
    generalLink = 'https://www.icos-cp.eu/stations/'
    link = 'https://meta.icos-cp.eu/resources/stations/' + station[2] + '_' + station[4]
    
    
    # if checkLnk ist true, we check the webserver response
    # for OK 200, otherwise we trust, that the provided link is valid.
    
    if(checkLnk):        
        r = requests.head(link)
        if (r.ok == False):
            link = generalLink
            
    src = '<a href="' + link + '" target="_blank">' + station[4] + '</a>'
    return src
    
#---EOF DEF----------------------------------------------------------
                


