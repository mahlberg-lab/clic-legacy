# -*- coding: utf-8 -*-

'''
Created on Tue Jul  7 12:20:40 2015

@author: https://gist.github.com/shreyansb/86b74ae47719a27bbb25

'''

'''
This module provides a simple WSGI profiler middleware for finding
bottlenecks in web application. It uses the profile or cProfile
module to do the profiling and writes the stats to the stream provided

To use, run `flask_profiler.py` instead of `app.py`

see: http://werkzeug.pocoo.org/docs/0.9/contrib/profiler/
and: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-debugging-testing-and-profiling
'''

from werkzeug.contrib.profiler import ProfilerMiddleware
from index import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])
app.run(debug = True)
