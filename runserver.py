"""
This script runs the application using a development server.
"""
# -*- coding: utf-8 -*-
from os import environ
from app.controller import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080

    app.run(HOST, PORT, debug = True) 