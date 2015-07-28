# -*- coding: utf-8 -*-
import json

import place
import achievements

class Database(object):
    def __init__(self):
        with open("database.json") as f:
            self.data = json.load(f)
        
        with open("streets.json") as f:
            self.streets = json.load(f)
        
        with open("crime_data.json") as f:
            self.crime_data = json.load(f)
    
    def save(self):
        with open("database.json", "w") as f:
            json.dump(self.data, f)
    
    def get_user_info(self, id_):
        return self.data["users"][id_]
    
    def new_user(self, first_name, last_name, id_):
        if id_ in self.data["users"]:
            raise Exception()
        
        user = {"first_name": first_name,
                "last_name": last_name,
                "achievements": [],
                "score": 0,
                "places": []}
        
        self.data["users"][id_] = user
        
        self.save()
    
    def delete_user(self, user_id):
        if not user_id in self.data["users"]:
            raise Exception()
        
        del self.data["users"][user_id]
        
        self.save()
    
    def update_user(self, user_id, street_id):
        if not user_id in self.data["users"]:
            raise Exception()
        
        user = self.data["users"][user_id]
        
        for placedict in user["places"]:
            if placedict["id"] == street_id:
                return
        
        placedict = {"id": street_id}
        placedict.update(place.get_street_info(self.streets, street_id))
        
        user["places"].append(placedict)
        user["score"] += place.get_score_for_street(self.streets, street_id)
        
        achievements.update_achievements(user, placedict)
        
        self.save()
    
    def get_scoreboard(self, count):
        if count == 0:
            return []
        
        users = [item for item in self.data["users"].iteritems()]
        
        users = sorted(users, key=lambda user: user[1]["score"])
        
        if len(users) >= count:
            users = users[-count:]
        
        users.reverse()
        
        return [user[0] for user in users]
