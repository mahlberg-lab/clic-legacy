# -*- coding: utf-8 -*-

'''
This file is an extension of index.py. It generates the raw json API that
the keywords, cluster, and concordances use(d).

It needs to be refactored.
'''


from __future__ import absolute_import  ## help python find modules within clic package (see John H email 09.04.2014)
from flask import Blueprint, request, jsonify
import json
import urllib

api = Blueprint('api_endpoints', __name__)

## Use beaker to save search (cache). See documentation on http://beaker.readthedocs.org/en/latest/caching.html
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from clic.concordance import Concordance
from clic.chapter_repository import ChapterRepository

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

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

@cache.cache('concordances')
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
