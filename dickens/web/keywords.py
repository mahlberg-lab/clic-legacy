## this is a wsgi-compatible script, receiving request from browser and uWSGI

import re

## User beaker to save search (cache). See documentation on http://beaker.readthedocs.org/en/latest/caching.html
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

from webob import Request, Response

from clic.dickens.keywords import Keywords

def paramHandler(params):
    form = params
    print vars(form)
    ## IdxGroup 1-gram, 3-6-gram. IdxGroup is the same for test and ref (name testIdxGroup for now)
    testIdxGroup = form.get('testIdxGroup', 'idx') ## from url request: http://127.0.0.1:8080/?testIdxGroup=3gram-idx&testIdxMod=quote&testCollection[]=dickens&testCollection[]=dickens

    testIdxMod = form.get('testIdxMod', '')
    refIdxMod = form.get('refIdxMod', '')
    ## IdxNames assuming both Group (3-gram etc.) and Mod is selected
    testIdxName = "{0}-{1}".format(testIdxMod, testIdxGroup)
    refIdxName = "{0}-{1}".format(refIdxMod, testIdxGroup)

    args = []
    ## if no ngram is specified the index is specific to Mod. If Mod is not specified default to sentence idx
    if not re.match('\dgram-idx', testIdxGroup):
        if not testIdxMod == '':
            testIdxName = testIdxMod + '-idx'
            refIdxName = refIdxMod + '-idx'
        else:
            testIdxName = 'sentence-idx'
            refIdxName = 'sentence-idx'
    args.insert(0, testIdxName)
    args.insert(2, refIdxName)

    book_collection = []
    refbook_collection = []

    ## run loop along the search parameters. each key represents search category
    for i, w in enumerate(form.keys()):
        if w == 'testCollection':
            book_collection.append(form.values()[i])
        if w == 'refCollection':
            refbook_collection.append(form.values()[i])
        if re.match('^vol',w)
            book_collection.append(form.values()[i])
            break

    args.insert(1, book_collection)
    args.insert(3, refbook_collection)

    return args

def application(env, start_response):
    req = Request(env)
    resp = Response()

    args = paramHandler(req.params)

    resp.json =  fetchKeywords(args)

    return resp(env, start_response)



@cache.cache('keyword', expire=3600) ## expires after 3600 secs
def fetchKeywords(args):

    keyworder = Keywords()

    keywords = keyworder.list_keywords(args[0], args[1], args[2], args[3])

    return {"keywords":keywords}
