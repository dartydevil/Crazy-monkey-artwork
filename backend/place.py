# -*- coding: utf-8 -*-
# This is where any country specific code will go.
import math

def miles(km):
    return km * 0.621

def distance_lat_long(lat0, long0, lat1, long1):
    R = 6371000
    lat = math.radians(lat0)
    long_ = math.radians(long0)
    dlat = math.radians(lat1 - lat0)
    dlong = math.radians(long1 - long0)
    
    a = math.sin(dlat / 2.0) * math.sin(dlat / 2.0) +\
        math.cos(lat) * math.cos(long_) *\
        math.sin(dlong / 2.0) * math.sin(dlong / 2.0)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    
    return miles(R * c)

def format_uk(id_):
    return "uk%s" % (id_)

def get_street_info_uk(streets, id_):
    info = streets[id_]
    
    return {"country": "uk",
            "label": info["label"],
            "longitude": info["longitude"],
            "latitude": info["latitude"]}

def get_street_info(streets, id_):
    if id_.startswith("uk"):
        return get_street_info_uk(streets, id_)
    else:
        return {"country": "unknown", "label": "Unknown", "longitude": 0.0, "latitude": 0.0}

def find_places(streets, crime_data, longitude, latitude, radius):
    places = []
    
    for crime in crime_data["crimes"]:
        if distance_lat_long(crime["latitude"],
                             crime["longitude"],
                             latitude,
                             longitude) < radius:
            info = get_street_info(streets, crime["street_id"])
            
            places.append({"country": info["country"],
                           "label": info["label"],
                           "longitude": info["longitude"],
                           "latitude": info["latitude"],
                           "id": crime["street_id"]})
    
    return places

def get_score_for_street(streets, id_):
    info = streets[id_]
    
    return info["num_crimes"]
