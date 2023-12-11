#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 
#   FILE: extract_subset.py
#   REVISION: April, 2023
#   CREATION DATE: April, 2023
#   AUTHOR: David W. McDonald
#
#   Testing GeoJSON access and extracting a subset of the larger file
#   
#   Copyright by Author. All rights reserved. Not for reuse without express permissions.
#

import sys, json

# once we got the streaming reader working this made searching the big ass file easier
from wildfire.Reader import Reader

#
#   This was extracted from a Wikipedia page that lists large CA wildfires
#.  The idea was to try and find unique names - this took a little playing around
#
BIG_CA_FIRES_BY_NAME = {
    "cedar" : {
            "year":     2003,
            "acres":    273246,
            "hectares": 110579
        },
#    "rush" : {
#            "year":     2012,
#            "acres":    271911,
#            "hectares": 110038
#        },
    "mendocino complex": {
            "year":     2018,
            "acres":    459123,
            "hectares": 185800
        },
    "matilija" : {
            "year":     1932,
            "acres":    220000,
            "hectares": 89000
        },
    "zaca" : {
            "year":     2007,
            "acres":    240207,
            "hectares": 97208
        },
    "carr" : {
            "year":     2018,
            "acres":    229651,
            "hectares": 92936
        },
    "monument" : {
            "year":     2021,
            "acres":    223124,
            "hectares": 90295
        },
    "north complex" : {
            "year":     2020,
            "acres":    318935,
            "hectares": 129068
        },   
    "river complex" : {
            "year":     2021,
            "acres":    199343,
            "hectares": 80671
        },   
    "klamath theater complex" : {
            "year":     2008,
            "acres":    192038,
            "hectares": 77715
        },
    "santiago canyon" : {
            "year":     1889,
            "acres":    300000,
            "hectares": 120000
        }
}



#
#   From the data description at: https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81
#   
#   Based on the "merged" data file, ... "Polygons were then processed in order of Tier (1-8) so that 
#   overlapping polygons in the same year and Tier were dissolved together. Overlapping polygons in subsequent 
#   Tiers were removed from the dataset. Attributes from the original datasets of all intersecting polygons in 
#   the same year across all Tiers were also merged so that all attributes from all Tiers were included, but 
#   only the polygons from the highest ranking Tier were dissolved to form the fire polygon. The resulting 
#   product (the combined dataset) has only one fire per year in a given area with one set of attributes.
#
#   The 'combined' file is smaller, 2.27 GB - this is probably the most reliable.
#
WILDFIRE_FNAME = "/Users/dwmc/datasets/wildfire_data/GeoJSON Exports/USGS_Wildland_Fire_Combined_Dataset.json"
#
#   This is probably not the one we want. According to the docuentation this one probably had duplicate
#   fire data that has not be geographically 'combined'. This file is much larger - 11.38 GB
#
#WILDFIRE_FNAME = "/Users/dwmc/datasets/wildfire_data/GeoJSON Exports/USGS_Wildland_Fire_Merged_Dataset.json"

#
#   This will be what we call our extracted data file
#
SAMPLE_FNAME = "extraction_sample.json"


def streaming_load_feature_count(fname=None,show_features=False):
    print(f"Attempting to open '{fname}'")
    wf_reader = Reader(fname)
    
    # get the header of the file
    header = wf_reader.header()
    
    # dump the header as output
    print("HEADER DICT")
    print(json.dumps(header,indent=4))
    
    # now try to load the whole thing - one feature at a time - streaming
    feature_count = 0
    feature = wf_reader.next()
    while feature:
        feature_count += 1
        if show_features:
            print(json.dumps(feature,indent=4))
        if (feature_count % 1000) == 0:
            print(f"Loaded {feature_count} features")
        
        feature = wf_reader.next()
    
    print(f"Loaded a total of {feature_count} features")
    return
    

def extract_samples_by_name(fname=None):
    print(f"Attempting to open '{fname}'")
    wf_reader = Reader(fname)
    
    feature_list = list()
    
    found_count = 0
    feature_count = 0
    feature = wf_reader.next()
    while feature:
        feature_count += 1
        if (feature_count % 1000) == 0:
            print(f"Loaded {feature_count} features")
        
        attributes = feature['attributes']
        
        listed_names = attributes["Listed_Fire_Names"].lower()
        
        for name in BIG_CA_FIRES_BY_NAME:
            n = str(name)
            if n in listed_names:
                if attributes['Fire_Year'] == BIG_CA_FIRES_BY_NAME[name]['year']:
                    fire_type = attributes['Assigned_Fire_Type'].lower()
                    if "wildfire" in fire_type:
                        print(f"MAYBE FOUND FIRE: {n}")
                        print(json.dumps(attributes,indent=4))
                        print(json.dumps(BIG_CA_FIRES_BY_NAME[name],indent=4))
                        feature_list.append(feature)
                        found_count += 1
        
        feature = wf_reader.next()
    
    print(f"Loaded a total of {feature_count} features")
    print(f"Possibly found {found_count} named fires")

    header = wf_reader.header()
    header['features'] = feature_list
    
    f = open(SAMPLE_FNAME,"w")
    json.dump(header,f)
    f.close()
    return





##
#   
#   python3 extract_subset.py 
#
#
def main(argv):
    #
    # try to read and count the whole thing
    #streaming_load_feature_count(WILDFIRE_FNAME)
    #
    # try to read and count the extraction
    #streaming_load_feature_count(SAMPLE_FNAME)
    streaming_load_feature_count(SAMPLE_FNAME,True)
    #
    # try to create a small subset
    #extract_samples_by_name(WILDFIRE_FNAME)    
    
    return

if __name__ == '__main__':
    main(sys.argv)   



