# -*- coding: utf-8 -*-
# This is where any country specific code will go.

def format_uk(id_):
    return "uk%d" % (id_)

def find_places(longitude, latitude, radius):
    #TODO
    #NOTE: This should only include crimes with a "violent-crime" category.
    return []

def get_street_info_uk(id_):
    #TODO
    #NOTE: Use data generated from a police crime data.
    return {"country": "uk", "label": "Unknown", "longitude": 0.0, "latitude": 0.0}

def get_street_info(id_):
    if id_.startswith("uk"):
        return get_street_info_uk(id_[2:])
    else:
        return {"country": "unknown", "label": "Unknown", "longitude": 0.0, "latitude": 0.0}

def get_score_for_street(id_):
    #TODO
    return 0
