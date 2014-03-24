import re

from webob import Request, Response

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

from clic.dickens.clusters import Clusters

def paramHandler(params):
    form = params
    print vars(form)
    
    idxGroup = form.get('idxGroup', 'idx')
    idxMod = form.get('idxMod', '')
    idxName = "{0}-{1}".format(idxMod, idxGroup)
    
    args = []
    ## if no ngram is specified the index is specific to Mod. If Mod is not specified default to sentence idx
    if not re.match('\dgram-idx', idxGroup):
        if not idxMod == '':
            idxName = idxMod + '-idx'
        else:
            idxName = 'sentence-idx'
    args.insert(0, idxName)
    
    book_collection = []
    ## run loop along the search parameters. each key represents search category
    for i, w in enumerate(form.keys()):
        if w == 'testCollection':
            book_collection.append(form.values()[i])
    
    args.insert(1, book_collection)

def application(env, start_response):
    req = Request(env) ## interpret request coming in
    resp = Response() ## set up response to be made
    
    args = paramHandler(req.params)
    
    resp.json = fetchClusters(args)
    
    return resp(env, start_response)

@cache.cache('keyword', expire=3600)
def fetchClusters(args):
    
    cluster = Clusters()

    return cluster.list_clusters(args[0], args[1])