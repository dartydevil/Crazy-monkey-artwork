# -*- coding: utf-8 -*-
# This is where any country specific code will go.
import math

def miles(km):
    return km * 0.621

def distance_lat_long(lat1, long1, lat2, long2):
    long1 = math.radians(long1)
    lat1 = math.radians(lat1)
    long2 = math.radians(long2)
    lat2 = math.radians(lat2)
    
    #haversine formula
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return miles(km)

def format_uk(id_):
    return "uk%s" % (id_)

def get_street_info_uk(streets, id_):
    info = streets[id_]
    
    return {"country": "uk",
            "label": info["label"],
            "longitude": info["longitude"],
            "latitude": info["latitude"],
            "num_crimes": info["num_crimes"]}

def get_street_info(streets, id_):
    if id_.startswith("uk"):
        return get_street_info_uk(streets, id_)
    else:
        return {"country": "unknown", "label": "Unknown", "longitude": 0.0, "latitude": 0.0, "num_crimes": 0}

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
                           "id": crime["street_id"],
                           "num_crimes": info["num_crimes"]})
    
    return places

def get_score_for_street(streets, id_):
    info = streets[id_]
    
    return info["num_crimes"]
