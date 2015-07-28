# -*- coding: utf-8 -*-
import json
import traceback

import place

def handleAction(data, action, args):
    try:
        if action == "userinfo":
            result = data.get_user_info(args["id"])
        elif action == "newuser":
            data.new_user(args["firstname"], args["lastname"], args["id"])
            result = {}
        elif action == "deleteuser":
            data.delete_user(args["id"])
            result = {}
        elif action == "findplaces":
            places = place.find_places(data.streets,
                                       data.crime_data,
                                       float(args["longitude"]),
                                       float(args["latitude"]),
                                       float(args["radius"]))
            
            result = {"places": places}
        elif action == "scoreboard":
            result = {"users": data.get_scoreboard(int(args["num"]))}
        elif action == "updateuser":
            data.update_user(args["user"], args["place"])
            
            result = {}
        
        result["success"] = True
    except Exception, e:
        print "ERROR: See error.txt"
        
        with open("error.txt", "w") as f:
            f.write(traceback.format_exc(e))
        
        result = {"success":False}
    
    return json.dumps(result)
