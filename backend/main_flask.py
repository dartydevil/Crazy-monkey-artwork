#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask 
import werkzeug.wrappers as werkwrappers
import werkzeug.serving


import api
import database

@app.route('/')
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
    
    try:
        with open("../client"+path, "r") as f:
            return werkwrappers.Response(f.read())
    except IOError:
        with open("../client/404.html", "r") as f:
            return werkwrappers.Response(f.read(), status=404)

if __name__ == '__main__':
    werkzeug.serving.run_simple('localhost', 4000, main)
