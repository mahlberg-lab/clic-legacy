
import cgitb
import os
import re
import smtplib
import sys
import time
import traceback
import sys
import urllib

# Import mod_python stuffs
from mod_python import apache, Cookie
from mod_python.util import FieldStorage

from crypt import crypt

# import Cheshire3/PyZ3950 stuff
from cheshire3.baseObjects import Session
from cheshire3.document import StringDocument
import cheshire3.exceptions
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer

# C3 web search utils
from cheshire3.web.www_utils import *

# separate file containing display configs + some HMTL for table rows etc.
from clic.dickens.web.dickensWebConfig import *
from clic.dickens.web.dickensSearchHandler import SearchHandler
from clic.dickens.web.dickensBrowseHandler import BrowseHandler

cheshirePath = os.environ.get('HOME', '/home/cheshire')

logPath = os.path.join(cheshirePath, 'clic', 'www', databaseName, 'logs', 'searchHandler.log')
htmlPath = os.path.join(cheshirePath, 'clic', 'www', databaseName, 'html')

session = Session()
session.environment = 'apache'
session.user = None
serv = SimpleServer(session, os.path.join(cheshire3Root, 'configs', 'serverConfig.xml'))

session.database = 'db_dickens'
db = serv.get_object(session, session.database)
authStore = db.get_object(session, 'authStore')


# Discover objects...
def handler(req):
    global db, htmlPath, logPath, cheshirePath, xmlp, recordStore
    form = FieldStorage(req)
    try:
        dir = req.uri[1:].rsplit('/')[1]
    except IndexError:
        return apache.HTTP_NOT_FOUND
    remote_host = req.get_remote_host(apache.REMOTE_NOLOOKUP)
    lgr = FileLogger(logPath, remote_host) 
#    lgr.log(req.uri)
#    lgr.log('directory is %s' % dir)
#    if dir == 'index.html' :
#        page = read_file(os.path.join(cheshirePath, 'clic', 'www', 'dickens', 'html', 'index.html'))
#        req.write(page)
#        #req.sendfile(os.path.join(cheshirePath, 'clic', 'www', 'dickens', 'html' + dir))
#        return apache.OK
    if dir in ['css', 'js', 'img', 'images']:
        #raise ValueError(os.path.join(cheshirePath, 'clic', 'www' + req.uri))
        req.sendfile(os.path.join(cheshirePath, 'clic', 'www' + req.uri))
        return apache.OK
    else:        
        try:
            remote_host = req.get_remote_host(apache.REMOTE_NOLOOKUP)     # get the remote host's IP for logging
            os.chdir(htmlPath)                                            # cd to where html fragments are
            lgr = FileLogger(logPath, remote_host)
            # Determine whether to use a sub-handler      
            if form.get('operation', None) =='search':
                handler = SearchHandler(lgr)                                # initialise handler - with logger for this request
            elif form.get('operation', None) =='browse':
                handler = BrowseHandler(lgr)
            else:
                req.content_type = "text/html"
                page = read_file('dickensInterface.html')
                req.write(page)
                #return apache.HTTP_NOT_FOUND
                return apache.OK
            # Handle request
            try:
                handler.handle(req)
            finally:
                # Clean-up
                # Flush all logged strings to disk
                try:
                    lgr.flush()
                except:
                    pass
                # Delete handler to ensure no state info is retained
                del lgr, handler
        except:
            req.content_type = "text/html"
            cgitb.Hook(file = req).handle()                               # give error info
            return apache.HTTP_INTERNAL_SERVER_ERROR
        else:
            return apache.OK
    
#- end handler()

#def authenhandler(req):
#    global session, authStore
#                                              # build the architecture
#    pw = req.get_basic_auth_pw()
#    un = req.user
#    try: session.user = authStore.fetch_object(session, un)
#    except: return apache.HTTP_UNAUTHORIZED    
#    if (session.user and session.user.password == crypt(pw, pw[:2])):
#        return apache.OK
#    else:
#        return apache.HTTP_UNAUTHORIZED
#    #- end authenhandler()
