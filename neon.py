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
        get all the neon sites and return MarkerCluster
        (to be added to a folium map.)
    """
    
    checkLnk = False
    if (len(checkUrl)):
        checkLnk = checkUrl

    
    
    # get the data through the neon api
    url = "http://data.neonscience.org/api/v0/locations/sites"
    r = requests.get(url)
    neonsites = r.json()
    
    # Now loop throuth the NEON stations and add them to the MarkerCluster
    mc = MarkerCluster()
    for station in neonsites['data']:
        if (   
            'locationDecimalLatitude' in station and 
            'locationDecimalLongitude' in station 
            ):
            # check if lat, lon exist and are numbers, otherwise skip the station
            if (
                    h.is_number(station['locationDecimalLatitude']) and
                    h.is_number(station['locationDecimalLongitude'])
                ):
                #create the markers
                msg = "<table border=0>"
                msg += "<tr><td>Network: </td><td>NEON</td></tr>"        
                msg += "<tr><td>Code: </td><td>" + srcLink(station['locationName'],checkLnk) +"</td></tr>"                   
                msg += "<tr><td>Name: </td><td>" + station['locationDescription'] +"</td></tr>"            
                msg += "<tr><td>Latitude: </td><td>" + str(station['locationDecimalLatitude']) +"</td></tr>"
                msg += "<tr><td>Longitude: </td><td>" + str(station['locationDecimalLongitude']) +"</td></tr>"
                msg += "</table>"                    
                msg = textile.textile(msg)                
                
                #create a marker and add to cluster
                m = folium.Marker(
                        location = [float(station['locationDecimalLatitude']), float(station['locationDecimalLongitude'])],
                        popup=msg)
                m.add_child(h.getIcon('neon'))
                m.add_to(mc)                    
    return mc


def srcLink(stationCode, checkLnk):
    """
        Assemble a string as http src link with the nenon station code
        The result should be a valid link to the 'landing page of the"
        site.
        The link is checked for validity (http return 200)
    """
    
    # create a link to the stations landing page
    generalLink = "https://www.neonscience.org/field-sites/field-sites-map/"
    link = generalLink + stationCode + "/"
    
    if(checkLnk):        
        r = requests.head(link)
        if (r.ok == False):
            link = generalLink
    
    src = '<a href="' + link + '" target="_blank">' + stationCode + '</a>'
    return src

#---EOF DEF----------------------------------------------------------
                

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                