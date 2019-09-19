# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:25:56 2018

@author: Claudio
"""
import requests
import folium
from folium.plugins import MarkerCluster
import helper_functions as h
import textile

def sites_marker_list(*checkUrl):
    """
        get all the lTER sites return MarkerCluster
        (to be added to a folium map.)
        Input: checkLnk [0|1]
        by default (if no argument is provided, we assume the value "False", 
        hence the url provided from ameriflux are considered valid.
        If checkLnk is "True", ech station url is checked for response "200 OK"
    """
    checkLnk = False
    if (len(checkUrl)):
        checkLnk = checkUrl
    
    # get the data through the api from DEIMS
    url = "https://deims.org/geoserver/deims/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=deims:ilter_all_formal&outputFormat=application%2Fjson"
    #lterAfrica
    #lterAmericas
    #lterEurope
    
    r = requests.get(url)
    lter = r.json()
    
    # Now loop throuth the stations and add them to the MarkerCluster
    
    mc = MarkerCluster()    
    
    for station in lter['features']:
        # extract the location 
        lat = station['properties']['field_coordinates_lat']
        lon = station['properties']['field_coordinates_lon']
        
        
        if (   
            'field_coordinates_lat' in station['properties'] and 
            'field_coordinates_lon' in station['properties']
            ):  
            
            lat = station['properties']['field_coordinates_lat']
            lon = station['properties']['field_coordinates_lon']
            
            
            # check validity of lat, lon 
            if (h.is_number(lat) and h.is_number(lon)):
                #create the markers
                msg = "<table border=0>"
                msg += "<tr><td>Network: </td><td>"+ station['properties']['network'] + "</td></tr>"
                msg += "<tr><td>Name: </td><td>" + srcLink(station, checkLnk) +"</td></tr>"                         
                msg += "<tr><td>Latitude: </td><td>" + str(lat) +"</td></tr>"
                msg += "<tr><td>Longitude: </td><td>" + str(lon) +"</td></tr>"
                msg += "</table>"                    
                msg = textile.textile(msg)
                
                #create a marker and add to cluster
                m = folium.Marker(location=[float(lat), float(lon)],popup=msg)
                m.add_child(h.getIcon('lter'))
                m.add_to(mc)
    
    return mc


def srcLink(station, checkLnk):
    """
        Assemble a string as http src link with the nenon station code
        The result should be a valid link to the 'landing page of the"
        site.
        The link is checked for validity (http return 200)
    """
    
    # create a link to the stations landing page
    # as fall back solution a static "general" link is provided, in 
    # case the station landing page can not be reached
    
    generalLink = 'https://deims.org/map/'
    link ='https://deims.org/' + station['properties']['deimsid']
    
    # if checkLnk ist true, we check the webserver response
    # for OK 200, otherwise we trust, that the provided link is valid.
    
    if(checkLnk):        
        r = requests.head(link)
        if (r.ok == False):
            link = generalLink
            
    src = '<a href="' + link + '" target="_blank">' + station['properties']['name'] + '</a>'
    return src
    
#---EOF DEF----------------------------------------------------------
                

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                