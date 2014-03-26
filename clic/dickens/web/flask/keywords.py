from flask import Flask
import json

app = Flask(__name__)

import re

## User beaker to save search (cache). See documentation on http://beaker.readthedocs.org/en/latest/caching.html
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options



from clic.dickens.keywords import Keywords

from flask import request


cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

@app.route('/',methods=['GET'])
def index():
    args = request.args

    # put keywords into json
    keyword_result = fetchKeywords(args)
    keywords = json.dumps(keyword_result)

    return render_template('keywords.html', keywords=keywords)

#@cache.cache('keyword', expire=3600) ## expires after 3600 secs
## get keywords from dickens/keywords.py
def fetchKeywords(args):

    keyworder = Keywords()
    args = processArgs(args)
    keywords = keyworder.list_keywords(args[0], args[1], args[2], args[3])
    print keywords


    return {"keywords":keywords}



def processArgs(args):

    keywordArgs = []
    testMod = str(args["testIdxMod"])
    Group = str(args["testIdxGroup"])
    refMod = str(args["refIdxMod"])



    testIdxName = "{0}-{1}".format(testMod, Group)
    refIdxName = "{0}-{1}".format(refMod, Group)

    ## if no ngram is specified the index is specific to Mod. If Mod is not specified default to sentence idx
    if not re.match('\dgram-idx', Group):
        if not args["testIdxMod"] == '':
#             testIdxName = args["testIdxMod"] + '-idx'
#             refIdxName = args["refIdxMod"] + '-idx'
            testIdxName = testMod + '-idx'
            refIdxName = refMod + '-idx'

        else:
            testIdxName = 'sentence-idx'
            refIdxName = 'sentence-idx'

    keywordArgs.insert(0, testIdxName)
    keywordArgs.insert(2, refIdxName)

    book_collection = [args["testCollection"]]
    refbook_collection = [args["refCollection"]]


    keywordArgs.insert(1, book_collection)
    keywordArgs.insert(3, refbook_collection)

    return keywordArgs
