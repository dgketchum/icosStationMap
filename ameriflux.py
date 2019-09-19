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
        get all the ameriflux sites return MarkerCluster
        (to be added to a folium map.)
        Input: checkLnk [0|1]
        by default (if no argument is provided, we assume the value "False", 
        hence the url provided from ameriflux are considered valid.
        If checkLnk is "True", ech station url is checked for response "200 OK"
    """
    checkLnk = False
    if (len(checkUrl)):
        checkLnk = checkUrl
    
    # get the data through the neon api
    url = "https://ameriflux-data.lbl.gov/AmeriFlux/SiteSearch.svc/SiteMapData/AmeriFlux"
    r = requests.get(url)
    ameriflux = r.json()
    
    # Now loop throuth the stations and add them to the MarkerCluster
    
    mc = MarkerCluster()
    
    for station in ameriflux:
        # extract the location 
        aflocation = station['GRP_LOCATION']
        
        if (   
            'LOCATION_LAT' in aflocation and 
            'LOCATION_LONG' in aflocation
            ):  
            
            #print(station['locationName'])
            # check if lat, lon exist and are numbers, otherwise skip the station
            if (
                    h.is_number(aflocation['LOCATION_LAT']) and
                    h.is_number(aflocation['LOCATION_LONG'])
                ):
                #create the markers
                msg = "<table border=0>"
                msg += "<tr><td>Network: </td><td>AMERIFLUX</td></tr>"
                msg += "<tr><td>Code: </td><td>" + srcLink(station, checkLnk) +"</td></tr>"
                msg += "<tr><td>Name: </td><td>" + station['SITE_NAME'] +"</td></tr>"            
                msg += "<tr><td>Latitude: </td><td>" + str(aflocation['LOCATION_LAT']) +"</td></tr>"
                msg += "<tr><td>Longitude: </td><td>" + str(aflocation['LOCATION_LONG']) +"</td></tr>"
                msg += "</table>"                    
                msg = textile.textile(msg)
                
                
                #create a marker and add to cluster
                m = folium.Marker(
                        location=[float(aflocation['LOCATION_LAT']),                        
                        float(aflocation['LOCATION_LONG'])],
                        popup=msg)
                m.add_child(h.getIcon('ameriflux'))
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
    
    generalLink = 'https://ameriflux.lbl.gov/sites/site-list-and-pages/'
    link = station['URL_AMERIFLUX']
    
    # if checkLnk ist true, we check the webserver response
    # for OK 200, otherwise we trust, that the provided link is valid.
    
    if(checkLnk):        
        r = requests.head(link)
        if (r.ok == False):
            link = generalLink
            
    src = '<a href="' + link + '" target="_blank">' + station['SITE_ID'] + '</a>'
    return src
    
#---EOF DEF----------------------------------------------------------
                

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                