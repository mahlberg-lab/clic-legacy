from __future__ import absolute_import  ## help python find modules within clic package (see John H email 09.04.2014)
from flask import Flask
import json

app = Flask(__name__,static_url_path='')

import re

## Use beaker to save search (cache). See documentation on http://beaker.readthedocs.org/en/latest/caching.html
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


from clic.dickens.keywords import Keywords
from clic.dickens.clusters import Clusters
from clic.dickens.concordance_new import Concordancer_New

from flask import request
from flask import render_template


cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

@app.route('/keywords/',methods=['GET'])
def keywords():
    args = request.args
    # put keywords into json
    keyword_result = fetchKeywords(args)
    #print keyword_result
    keywords = json.dumps(keyword_result)
    return keywords

## ajax route: for splitting screen
@app.route('/ajax-keywords',methods=['GET'])
def ajax_keyords():
    args = request.args
    #return json.dumps(fetchKeywords(args))


@app.route('/clusters/', methods=['GET'])
def clusters():
    args = request.args
    
    clusters_result = fetchClusters(args)    
    clusters = json.dumps(clusters_result)
    return clusters

@app.route('/concordances/',methods=['GET'])
def concordances():
    args = request.args  

    concordances_result = fetchConcordance(args)
    concordances = json.dumps(concordances_result)
    return concordances


@cache.cache('keyword', expire=3600) ## expires after 3600 secs
def fetchKeywords(args):

    keyworder = Keywords()
    args = processArgs(args, 'keywords')
    print args
    keywords = keyworder.list_keywords(args[0], args[1], args[2], args[3], args[4])
    return {'keywords':keywords}

@cache.cache('cluster', expire=3600)
def fetchClusters(args):

    cluster = Clusters()
    
    args = processArgs(args, 'clusters')
 
    clusterlist = cluster.list_clusters(args[0], args[1])

    return {'clusters' : clusterlist}

#@cache.cache('concordances', expire=3600)
def fetchConcordance(args):

    concordancer = Concordancer_New()
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
        #testMod = str(args["testIdxMod"])
        Group = str(args['testIdxGroup']) 
        if not str(args["testIdxMod"]) == 'chapter':
            testMod = str(args["testIdxMod"])            
            testIdxName = "{0}-{1}".format(testMod, Group)
        else:
            testMod = ''
            testIdxName = "{0}".format(Group)
#         Group = str(args['testIdxGroup']) ## testGroup not used in concordances
#         testIdxName = "{0}-{1}".format(testMod, Group)
        methodArgs.insert(0, testIdxName)
        book_collection = args.getlist('testCollection') ## args is a multiDictionary: use .getlist() to access individual books
        methodArgs.insert(1, book_collection)

        refbook_collection = args.getlist('refCollection') 
        if not str(args["refIdxMod"]) == 'chapter':
            refMod = str(args['refIdxMod'])            
            refIdxName = "{0}-{1}".format(refMod, Group)
        else:
            refMod = ''
            refIdxName = "{0}".format(Group)

        ## if no ngram is specified the index is specific to Mod. If Mod is not specified default to sentence idx
        ## THERE WILL BE DEFAULT SELECT IN INTERFACE
#         if not re.match('\dgram-idx', Group):
#             if not args['testIdxMod'] == '':
#                 testIdxName = testMod + '-idx'
#                 refIdxName = refMod + '-idx'
# 
#         else:
#             testIdxName = 'sentence-idx'
#             refIdxName = 'sentence-idx'

        pValue = str(args['pValue'])
        
        methodArgs.insert(2, refIdxName)
        methodArgs.insert(3, refbook_collection)
        methodArgs.insert(4, pValue)

    elif method == 'concordances':

        testMod = str(args["testIdxMod"])
        testIdxName = testMod + '-idx'
        #wordWindow = str(args['wordWindow'])
        book_collection = args.getlist('testCollection')
        select_words = str(args['selectWords'])

        methodArgs.insert(0, str(args['terms']))
        methodArgs.insert(1, testIdxName)
        #methodArgs.insert(2, wordWindow) ## wordwindow set to 10 by default
        methodArgs.insert(2, book_collection)    
        methodArgs.insert(3, select_words)  


    return methodArgs

