from flask import Flask
import json

app = Flask(__name__, static_url_path='')

import re

## Use beaker to save search (cache). See documentation on http://beaker.readthedocs.org/en/latest/caching.html
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


from dickens.keywords import Keywords
from dickens.clusters import Clusters
from dickens.concordance_new import Concordancer_New

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
    print args

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

@app.route('/concordance/',methods=['GET'])
def concordance():
    args = request.args
    print args

    concordance_result = fetchConcordance(args)
    concordance = json.dumps(concordance_result)

    return render_template('concordance.html', concordance=concordance)


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

@cache.cache('concordance', expire=3600)
def fetchConcordance(args):

    concordancer = Concordancer_New()
    args = processArgs(args, "concordances")
    concordancelist = concordancer.create_concordances(args[0], args[1], args[2])

    return {'concordancelist' : concordancelist}

def processArgs(args, method):


    methodArgs = []
    testMod = str(args["testIdxMod"])

    if not method == 'concordance':
        Group = str(args["testIdxGroup"])
        book_collection = [args["testCollection"]]
        testIdxName = "{0}-{1}".format(testMod, Group)
        methodArgs.insert(0, testIdxName)
        methodArgs.insert(1, book_collection)


    if method == 'keywords':

        refMod = str(args["refIdxMod"])
        refbook_collection = [args["refCollection"]]

        refIdxName = "{0}-{1}".format(refMod, Group)

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

    elif method == 'concordance':

        testIdxName = testMod + '-idx'
        wordWindow = str(args["wordWindow"])

        methodArgs.insert(0, str(args["terms"]))
        methodArgs.insert(1, testIdxName)
        methodArgs.insert(2, wordWindow)

        return methodArgs


    return methodArgs

def processCollections(args,collectionName):

  collection = []


  for i, w in enumerate(args.keys()):
    if w == collectionName:
      collection.append(args[i])

    if re.match('^vol',w)
      collection.append(args[i])
      break
  return collection
