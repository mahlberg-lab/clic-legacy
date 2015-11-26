# -*- coding: utf-8 -*-

'''
This file is an extension of index.py. It generates the raw json API that
the keywords, cluster, and concordances use(d).

It needs to be refactored.
'''


from __future__ import absolute_import  ## help python find modules within clic package (see John H email 09.04.2014)
from flask import Blueprint, request
import json
import urllib

api = Blueprint('api_endpoints', __name__)

## Use beaker to save search (cache). See documentation on http://beaker.readthedocs.org/en/latest/caching.html
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from clic.keywords import Keywords
from clic.clusters import Clusters
from clic.concordance import Concordance
from clic.chapter_repository import ChapterRepository

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

'''
API endpoints
'''
@api.route('/keywords/', methods=['GET'])
def keywords():
    ## get search specifications (args):
    args = request.args
    ## put keywords into json:
    keyword_result = fetchKeywords(args) # get list of keywords
    keywords = json.dumps(keyword_result) # return keyword list as json
    return keywords

@api.route('/clusters/', methods=['GET'])
def clusters():
    args = request.args
    clusters_result = fetchClusters(args)
    clusters = json.dumps(clusters_result)
    return clusters

@api.route('/concordances/', methods=['GET'])
def concordances():
    args = request.args
    concordances_result = fetchConcordance(args)
    concordances = json.dumps(concordances_result)
    return concordances

@cache.cache('keywords') ## no expiry
def fetchKeywords(args):
    keyworder = Keywords()
    args = processArgs(args, 'keywords')
    keywordlist = keyworder.list_keywords(args[0], args[1], args[2], args[3], args[4])
    return keywordlist
    # return {'keywords' : keywords}

@cache.cache('clusters')
def fetchClusters(args):
    cluster = Clusters()
    args = processArgs(args, 'clusters')
    clusterlist = cluster.list_clusters(args[0], args[1])
    return clusterlist
    # return {'clusters' : clusterlist}

@cache.cache('concordances')
def fetchConcordance(args):
    concordancer = Concordance()
    args = processArgs(args, 'concordances')
    concordances = concordancer.create_concordance(args[0], args[1], args[2], args[3])
    return {'concordances' : concordances}

def processArgs(args, method):
    methodArgs = []

    if method == 'clusters':
        if not str(args["testIdxMod"]) == 'chapter':
            testMod = str(args["testIdxMod"])
            Group = str(args['testIdxGroup'])
            testIdxName = "{0}-{1}".format(testMod, Group)
        else:
            testMod = ''
            Group = str(args['testIdxGroup'])
            testIdxName = "{0}".format(Group)

        methodArgs.insert(0, testIdxName)
        book_collection = args.getlist('testCollection') ## args is a multiDictionary: use .getlist() to access individual books
        methodArgs.insert(1, book_collection)


    if method == 'keywords':
        Group = str(args['testIdxGroup'])
        if not str(args["testIdxMod"]) == 'chapter':
            testMod = str(args["testIdxMod"])
            testIdxName = "{0}-{1}".format(testMod, Group)
        else:
            testMod = ''
            testIdxName = "{0}".format(Group)

        methodArgs.insert(0, testIdxName)
        book_collection = args.getlist('testCollection')
        methodArgs.insert(1, book_collection) ## test corpus

        refbook_collection = args.getlist('refCollection')
        if not str(args["refIdxMod"]) == 'chapter':
            refMod = str(args['refIdxMod'])
            refIdxName = "{0}-{1}".format(refMod, Group)
        else:
            refMod = ''
            refIdxName = "{0}".format(Group)

        pValue = str(args['pValue'])

        methodArgs.insert(2, refIdxName)
        methodArgs.insert(3, refbook_collection) ## ref corpus
        methodArgs.insert(4, pValue)

    elif method == 'concordances':

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
