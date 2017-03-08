# -*- coding: utf-8 -*-

'''
This file is an extension of index.py. It generates the raw json API that
the keywords, cluster, and concordances use(d).

It needs to be refactored.
'''


from __future__ import absolute_import  ## help python find modules within clic package (see John H email 09.04.2014)
from flask import Blueprint, request, Response, jsonify
import json
import urllib

api = Blueprint('api_endpoints', __name__)

from clic.concordance import Concordance
from clic.chapter_repository import ChapterRepository

@api.app_errorhandler(500)
def handle_500(error):
    response = jsonify(dict(error=str(error)))
    response.status_code = 500
    return response

'''
API endpoints
'''
@api.route('/concordances/', methods=['GET'])
def concordances():
    args = request.args
    concordances_result = fetchConcordance(args)
    concordances = json.dumps(concordances_result)
    return concordances

@api.route('/concordance-warm/', methods=['GET'])
def concordance_warm():
    concordancer = Concordance()
    return Response(concordancer.warm_cache(), mimetype='text/plain')

def fetchConcordance(args):
    concordancer = Concordance()
    args = processArgs(args, 'concordances')
    concordances = concordancer.create_concordance(args[0], args[1], args[2], args[3])
    return {'concordances' : concordances}

def processArgs(args, method):
    methodArgs = []

    if method == 'concordances':

        testMod = str(args["testIdxMod"])
        testIdxName = testMod + '-idx'
        #wordWindow = str(args['wordWindow']) ## activate when in future wordWindow is in search options
        book_collection = args.getlist('testCollection')
        select_words = str(args['selectWords'])

        methodArgs.insert(0, str(args['terms']))
        methodArgs.insert(1, testIdxName)
        #methodArgs.insert(2, wordWindow)
        methodArgs.insert(2, book_collection)
        methodArgs.insert(3, select_words)


    return methodArgs
