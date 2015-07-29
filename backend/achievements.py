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

def add_achievement(content, achievement):
    return content +\
           "<img src=\"https://raw.githubusercontent.com/dartydevil/Crazy-monkey-artwork/master/client/images/achieve%s.png\"/>\n" % (achievement)

def generate_achievements_page(achievements, updown):
    content = """<!DOCTYPE html>
<html style="height:100%;margin:0px 0px">
    <meta charset="UTF-8">
"""
    
    if "1000" in achievements:
        content = add_achievement(content, "1000")
        
        content += "<br/>\n" if updown else ""
    
    if "100" in achievements:
        content = add_achievement(content, "100")
        
        content += "<br/>\n" if updown else ""
    
    if "50" in achievements:
        content = add_achievement(content, "50")
        
        content += "<br/>\n" if updown else ""
    
    if "10" in achievements:
        content = add_achievement(content, "10")
        
        content += "<br/>\n" if updown else ""
    
    if "1" in achievements:
        content = add_achievement(content, "1")
        
        content += "<br/>\n" if updown else ""
    
    content += "</html>\n"
    
    return content
