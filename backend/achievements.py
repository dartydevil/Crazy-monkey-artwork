# -*- coding: utf-8 -*-

def award(condition, user, achievement):
    if condition and not achievement in user["achievements"]:
        user["achievements"].append(achievement)

def update_achievements(user, place):
    award(user["score"] >= 1, user, "1")
    award(user["score"] >= 10, user, "10")
    award(user["score"] >= 50, user, "50")
    award(user["score"] >= 100, user, "100")
    award(user["score"] >= 1000, user, "1000")
