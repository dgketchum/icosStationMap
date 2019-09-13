# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:25:56 2018

@author: Claudio
"""
import requests
import folium
from folium.plugins import MarkerCluster
import textile
from bs4 import BeautifulSoup

def sites_marker_list(*checkUrl):
    """
        get all the asiaflux sites return MarkerCluster
        (to be added to a folium map.)
        Input: checkLnk [0|1]
        by default (if no argument is provided, we assume the value "False", 
        hence the url provided .
        If checkLnk is "True", ech station url is checked for response "200 OK"
    """
    checkLnk = False
    if (len(checkUrl)):
        checkLnk = checkUrl
    
    url = 'http://asiaflux.net/index.php?'
    url = url+'action=multidatabase_view_main_init&visible_item=1000&multidatabase_id=8&block_id=2346'
    
    r = requests.get(url)    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    tables = soup.find_all("table",{"class":"mdb_metadata_table"})

    asiaflux = []
    for t in tables:
        output_rows = []
        for table_row in t.findAll('tr'):  
            detail = []
            for column in table_row:
                detail.append(column.text)
            output_rows.append(detail)
        asiaflux.append(output_rows)
    
    # Now loop through the stations and add them to the MarkerCluster
    
    mc = MarkerCluster()
    
    for station in asiaflux:
        # extract the location 
        
        lat = float(station[2][1])
        lon = float(station[3][1])
        
        #create the popup entry
        msg = '<table border=0>'
        msg += '<tr><td>Network:</td><td>Asiaflux</td></tr>'
        for i in range(len(station)-1):
            msg += '<tr><td>' + station[i][0] + '</td><td>' + station[i][1]+'</td></tr>'
        
        # add the url link
        msg += "<tr><td>url</td><td>" + srcLink(station[7][1], checkLnk) +"</td></tr>"        
        msg += "</table>"                    
        msg = textile.textile(msg)
        
        
        #create a marker and add to cluster
        m = folium.Marker(
                location=[lat, lon],
                popup=msg)
        #m.add_child(folium.Icon(icon='atom'))
        m.add_child(folium.Icon(color = 'gray', icon='tint'))
        m.add_to(mc)                
    
    return mc


def srcLink(link, checkLnk):
    """
        Assemble a string as http src link with the nenon station code
        The result should be a valid link to the 'landing page of the"
        site.
        The link is checked for validity (http return 200)
    """
    
    # create a link to the stations landing page
    generalLink = 'http://asiaflux.net/?page_id=22'        
    
    # if checkLnk ist true, we check the webserver response
    # for OK 200, otherwise we trust, that the provided link is valid.
    
    if(checkLnk):        
        r = requests.head(link)
        if (r.ok == False):
            link = generalLink
            
    src = '<a href="' + link + '" target="_blank">' + link + '</a>'
    return src
    
#---EOF DEF----------------------------------------------------------
                

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                