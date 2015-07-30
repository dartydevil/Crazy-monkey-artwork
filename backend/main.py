#!/usr/bin/env python
# -*- coding: utf-8 -*-
import werkzeug.wrappers as werkwrappers
import werkzeug.serving

import api
import database
import achievements

header = """
<div style="text-align:center;">
    <a id="profileLink" href="">Profile</a>
    <a id="scoreboardLink" href="scoreboard.html?count=10">Leaders</a>
    <a id="mapLink" href="">Go</a>
    <button id="loginlogout"></button>
    <input type="text" id="idInput"/>
    <br/>
</div>

<script src="api.js"></script>
<script type="text/javascript">
    function updateLinks()
    {
        var profile = document.getElementById("profileLink")
        var map = document.getElementById("mapLink")
        
        var user = localStorage["userid"]
        
        if (user == undefined || user == null)
        {
            profile.href = base
            map.href = base
        } else
        {
            profile.href = base + "profile.html?user=" + user
            map.href = base + "map.html"
        }
    }
    
    function updateButtonText()
    {
        var loggedIn = localStorage["userid"] != undefined
        
        var idInput = document.getElementById("idInput")
        
        idInput.disabled = loggedIn
        
        if (loggedIn)
        {
            document.getElementById("loginlogout").innerHTML = "Logout"
            idInput.value = "Logged in as " + localStorage["userid"]
        } else
        {
            document.getElementById("loginlogout").innerHTML = "Login"
        }
    }
    
    document.getElementById("loginlogout").addEventListener("click", function ()
    {
        var idInput = document.getElementById("idInput")
        
        if (localStorage["userid"] == undefined)
        {
            var user = idInput.value
            
            if (getUserInfo(user) != null)
            {
                localStorage["userid"] = idInput.value
            } else
            {
                alert("Unable to log in as \\\"\" + user + \"\\\"")
            }
        } else
        {
            localStorage.removeItem("userid")
            window.location = base;
        }
        
        updateButtonText()
        updateLinks()
    });
    
    updateButtonText()
    updateLinks()
</script>
"""

data = database.Database()

@werkwrappers.Request.application
def main(request):
    path = request.path
    
    if path == "/api":
        action = request.args["action"]
        
        return werkwrappers.Response(api.handleAction(data, action, request.args))
    
    if path == "/profile.html":
        userinfo = data.get_user_info(request.args["user"])
        
        if request.args.get("updown", "False") == "True":
            updown = True
        else:
            updown = False
        
        content = """<!DOCTYPE html>
<html style="height:100%;">
    <meta charset="UTF-8">
"""
        
        content += header
        
        content += "<div style=\"text-align:center;\">\n<h1>Name</h1>"
        
        content += """%s %s<br/>%s<br/>""" % (userinfo["first_name"],
                                              userinfo["last_name"],
                                              request.args["user"])
        
        content += """<h1>Score</h1>"""
        
        content += "%d" % (userinfo["score"])
        
        content += """<h1>Achievements</h1></div>"""
        
        content += achievements.generate_achievements_html(userinfo["achievements"],
                                                           updown)
        
        content += "</html>"
        
        return werkwrappers.Response(content, mimetype="text/html")
    elif path == "/scoreboard.html":
        scoreboard = data.get_scoreboard(int(request.args["count"]))
        
        content = """<!DOCTYPE html>
<html style="height:100%s;margin:0px 0px">
    <meta charset="UTF-8">
    <body>
    %s
    <table style="width:100%s">
    <tr>
        <th>User</th>
        <th>Score</th>
    </tr>
""" % ("%", header, "%")
        
        for user in scoreboard:
            score = data.get_user_info(user)["score"]
            
            content += "<tr><th>%s</th><th>%d</th></tr>" % (user, score)
        
        content += " </table>\n</body>\n</html>\n"
        
        return werkwrappers.Response(content, mimetype="text/html")
    elif path in ["/index.html", "/"]:
        return werkwrappers.Response("""<!DOCTYPE html>
<html style="height:100%s">
    <meta charset="UTF-8">
    %s
</html>
""" % ("%", header), mimetype="text/html")
    
    try:
        with open("../client"+path, "r") as f:
            return werkwrappers.Response(f.read().replace("!!insertheader!!", header), mimetype="text/html")
    except IOError:
        with open("../client/404.html", "r") as f:
            return werkwrappers.Response(f.read().replace("!!insertheader!!", header), status=404, mimetype="text/html")

if __name__ == '__main__':
    werkzeug.serving.run_simple('localhost', 4000, main)
