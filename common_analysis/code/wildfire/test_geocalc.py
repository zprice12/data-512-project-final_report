#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 
#   FILE: test_geocalc.py
#   REVISION: April, 2023
#   CREATION DATE: April, 2023
#   AUTHOR: David W. McDonald
#
#   Working with some geo calculations - seeing if I understand how to calculate geodesic distances
#   
#   Copyright by Author. All rights reserved. Not for reuse without express permissions.
#

import sys, datetime, json, copy

# start using the reader - after getting the streaming reader to work
from wildfire.Reader import Reader


#   The GeoJSON data is in "ESRI:102008 NAD 1983 Albers North America" format and we want "EPSG:4326 (WGS84)" format
#   The conversion requires a "projection" to sit in the right space
#   
#   This is a place that will transform one point at a time
#   https://epsg.io/transform#s_srs=102008&t_srs=4326&x=NaN&y=NaN

#   The python module pyproj should be able to perform the conversion
#   https://pyproj4.github.io/pyproj/stable/
#
#   An example of how to perform the conversion is at:
#   https://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/
#
#   One 'helpful' stack overflow post was:
#   https://gis.stackexchange.com/questions/304231/converting-nad83-epsg4269-to-wgs84-epsg4326-using-pyproj
#   
import pyproj
from pyproj import Transformer, Geod


#Standard Reference Systems (SRS)
#
#   "ESRI:104602" "NAD83" - basis is meters?
#   "ESRI:102008" "NAD 1983" Albers North American
#

#.  Some distances
#   New York to portland 3,925.26 km    (4013037.318)
#   Boston to portland 4088 km          (4164192.708)

#   A single lat,lon location for testing
REDDING_CA = [40.5865, -122.3917]
#   A list of dictionaries for testing
CITY_LOCATIONS = [ 
    {'Anchorage, AK'       : [61.2176, -149.8997] }, 
    {'Ocean Shores, WA'    : [47.0074, -124.1614] }, 
    {'Seaside, OR'         : [45.9932, -123.9226] }, 
    {'Crescent City, CA'   : [41.7558, -124.2026] }, 
    {'Tomales, CA'         : [38.2463, -122.9056] }, 
    {'San Luis Obispo, CA' : [35.2828, -120.6596] }, 
    {'Encinitas, CA'       : [33.0370, -117.2920] } 
]


#
#   A sample extraction - this has 13 features based on an extraction that used names of "big" California
#   wildfires. Of course, some of the names are not that specific - so there are probably fires that were
#   not in California. I'm using this to test the distance calculations. Want to know the distance from a
#   city lat,long and a fire perimiter. ... Lets see how we can make this work.
#
SAMPLE_FNAME = "Wildfire_short_sample.json"


def distance_calc_test():

    #g = Geod(ellps='clrk66')       # Use Clarke 1866 ellipsoid.
    g = Geod(ellps='WGS84')         # Use WGS84 ellipsoid.
    # specify the lat/lons of some cities.
    boston_lat = 42.+(15./60.); boston_lon = -71.-(7./60.)
    portland_lat = 45.+(31./60.); portland_lon = -123.-(41./60.)
    newyork_lat = 40.+(47./60.); newyork_lon = -73.-(58./60.)
    london_lat = 51.+(32./60.); london_lon = -(5./60.)

    print("USING 'WGS84' ellipsoid")
    az12,az21,dist = g.inv(boston_lon,boston_lat,portland_lon,portland_lat)
    print(f"Boston, MA -> Portland, OR distance: {dist}")
    
    az12,az21,dist = g.inv(newyork_lon,newyork_lat,portland_lon,portland_lat)
    print(f"New York, NY -> Portland, OR distance: {dist}")


    print("USING 'clrk66' ellipsoid")
    g = Geod(ellps='clrk66')       # Use Clarke 1866 ellipsoid.
    az12,az21,dist = g.inv(boston_lon,boston_lat,portland_lon,portland_lat)
    print(f"Boston, MA -> Portland, OR distance: {dist}")
    
    az12,az21,dist = g.inv(newyork_lon,newyork_lat,portland_lon,portland_lat)
    print(f"New York, NY -> Portland, OR distance: {dist}")
    
    return




##
#   
#   python3 test_geocalc.py 
#
#
def main(argv):
    
    distance_calc_test()
    
    print(f"Attempting to open '{SAMPLE_FNAME}'")
    wf_reader = Reader(SAMPLE_FNAME)

    # just get one feature first
    feature = wf_reader.next()

    geom = feature['geometry']
    
    largest_ring = geom['rings'][0]
    
    largest_ring_converted = list()
    to_wgs84 = Transformer.from_crs("ESRI:102008","EPSG:4326")
    for coord in largest_ring:
        lat,lon = to_wgs84.transform(coord[0],coord[1])
        new_coord = lat,lon
        largest_ring_converted.append(new_coord)
        #print(f"coord:{coord} lat,lon:{lat},{lon}")
        #print(f"coord:{coord} lat,lon:{new_coord[0]},{new_coord[1]}")
        
        
    # create coordinate reference systems for the conversion
    crs_context = dict()
    crs_context['to'] = pyproj.CRS.from_string("EPSG:4326")         #   This one is the most common lat, lon format
    #crs_context['from'] = pyproj.CRS.from_string("EPSG:102008")     #   This is a decimal
    crs_context['from'] = pyproj.CRS.from_string("ESRI:102008")     #   This is a decimal format for North America
    
    projector = Transformer.from_crs("ESRI:102008","EPSG:4326")
    
    print("Geometry:")
    print(len(geom['rings']))
    #c = 1
    #for ring in geom['rings']:
    #    print(f"Ring {c}:")
    #    print(json.dumps(ring,indent=4))
    #    c += 1

    #
    #   This is a list of lists
    largest_ring_in_102008 = geom['rings'][0]
    print(f"Largest ring points: {len(largest_ring_in_102008)}")
    #   This returns a list like iterable thing, not a scriptable list
    #ring_in_4326 = projector.itransform(largest_ring_in_102008)

    largest_ring_in_4326 = list()
    for xy in largest_ring_in_102008:
        lat,lon = projector.transform(xy[0],xy[1])
        elt = lat,lon
        largest_ring_in_4326.append(elt)
        #print(f"x,y:{xy} lat,lon:{lat},{lon}")
        print(f"x,y:{xy} lat,lon:{elt[0]},{elt[1]}")
    
    
    #for elt in largest_ring_in_4326:
    #    print(f"lat,lon:{elt[0]},{elt[1]}")

    
    print(json.dumps(largest_ring_in_4326[0],indent=4))
    print(json.dumps(largest_ring_in_4326[-1],indent=4))
    return

if __name__ == '__main__':
    main(sys.argv)   



