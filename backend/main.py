#!/usr/bin/env python
# -*- coding: utf-8 -*-
import werkzeug.wrappers as werkwrappers
import werkzeug.serving

import api
import database
import achievements

data = database.Database()

@werkwrappers.Request.application
def main(request):
    if request.path == "/api":
        action = request.args["action"]
        
        return werkwrappers.Response(api.handleAction(data, action, request.args))
    
    if request.path == "/":
        path = "/index.html"
    else:
        path = request.path
    
    if path == "/achievements.html":
        userinfo = data.get_user_info(request.args["user"])
        
        if request.args.get("updown", "True") == "True":
            updown = True
        else:
            updown = False
        
        content = achievements.generate_achievements_page(userinfo["achievements"],
                                                          updown)
        
        return werkwrappers.Response(content, mimetype="text/html")
    elif path == "/scoreboard.html":
        scoreboard = data.get_scoreboard(int(request.args["count"]))
        
        content = """<!DOCTYPE html>
<html style="height:100%;margin:0px 0px">
    <meta charset="UTF-8">
    <body>
    <table style="width:100%">
    <tr>
        <th>User</th>
        <th>Score</th>
    </tr>
"""
        
        for user in scoreboard:
            score = data.get_user_info(user)["score"]
            
            content += "<tr><th>%s</th><th>%d</th></tr>" % (user, score)
        
        content += " </table>\n</body>\n</html>\n"
        
        return werkwrappers.Response(content, mimetype="text/html")
    
    try:
        with open("../client"+path, "r") as f:
            return werkwrappers.Response(f.read(), mimetype="text/html")
    except IOError:
        with open("../client/404.html", "r") as f:
            return werkwrappers.Response(f.read(), status=404, mimetype="text/html")

if __name__ == '__main__':
    werkzeug.serving.run_simple('localhost', 4000, main)

"""<html>
<body style="text-align:center;">
<table style="width:100%">
<tr>
    <th><a href="google.com">Triumphs</a></th>
    <th><a href="google.com">Leaders</a></th>
    <th><a href="google.com">Go</a></th>
</tr>
</table>
</body>
</html>"""
