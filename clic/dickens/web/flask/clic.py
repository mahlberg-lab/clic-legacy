from flask import Flask
import json

app = Flask(__name__, static_url_path='')

import re

## User beaker to save search (cache). See documentation on http://beaker.readthedocs.org/en/latest/caching.html
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from keywords import Keywords
from clusters import Clusters

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
    keywords = json.dumps(keyword_result)

    return render_template('keywords.html', keywords=keywords)

@app.route("/clusters/", methods=["GET"])
def clusters():
    args = request.args
    args = processArgs(args)
    clusters_result = fetchClusters(args)
    clusters = json.dumps(clusters_result)

    return render_template('clusters.html', clusters=clusters)





@cache.cache('keyword', expire=3600) ## expires after 3600 secs
## get keywords from dickens/keywords.py
def fetchKeywords(args):

    keyworder = Keywords()
    args = processArgs(args, "keywords")
    keywords = keyworder.list_keywords(args[0], args[1], args[2], args[3])
    return {"keywords":keywords}

@cache.cache('cluster', expire=3600)
def fetchClusters(args):

    cluster = Clusters()
    args = processArgs(args, "clusters")
    clusterlist = cluster.list_clusters(args[0], args[1])

    return {'clusterlist' : clusterlist}

def processArgs(args, method):

    methodArgs = []
    testMod = str(args["testIdxMod"])
    Group = str(args["testIdxGroup"])
    testIdxName = "{0}-{1}".format(testMod, Group)
    book_collection = [args["testCollection"]]


    if method == 'keywords':


        testMod = str(args["testIdxMod"])
        Group = str(args["testIdxGroup"])
        refMod = str(args["refIdxMod"])

        book_collection = [args["testCollection"]]
        refbook_collection = [args["refCollection"]]

        testIdxName = "{0}-{1}".format(testMod, Group)
        refIdxName = "{0}-{1}".format(refMod, Group)
        methodArgs.insert(0, testIdxName)

        ## if no ngram is specified the index is specific to Mod. If Mod is not specified default to sentence idx
        if not re.match('\dgram-idx', Group):
            if not args["testIdxMod"] == '':
                testIdxName = testMod + '-idx'
                refIdxName = refMod + '-idx'

        else:
            testIdxName = 'sentence-idx'
            refIdxName = 'sentence-idx'


        methodArgs.insert(2, refIdxName)



        methodArgs.insert(3, refbook_collection)

    methodArgs.insert(1, book_collection)
    return methodArgs
