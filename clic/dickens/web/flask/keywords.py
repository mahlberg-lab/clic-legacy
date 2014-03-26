from flask import Flask

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
    fetchKeywords(args)
    return "<span style='color:red'>I am app 1</span>"


@cache.cache('keyword', expire=3600) ## expires after 3600 secs
def fetchKeywords(args):

    keyworder = Keywords()
    args = processArgs(args)
    keywords = keyworder.list_keywords(args[0], args[1], args[2], args[3])

    return {"keywords":keywords}

def processArgs(args):

  ## if no ngram is specified the index is specific to Mod. If Mod is not specified default to sentence idx
  if not re.match('\dgram-idx', args["testIdxGroup"]):
      if not testIdxMod == '':
          testIdxName = args["testIdxMod"] + '-idx'
          refIdxName = args["refIdxMod"] + '-idx'
      else:
          testIdxName = 'sentence-idx'
          refIdxName = 'sentence-idx'
  args.insert(0, testIdxName)
  args.insert(2, refIdxName)


  book_collection = [args["testCollection"]]
  refbook_collection = [args["refCollection"]]


  args.insert(1, book_collection)
  args.insert(3, refbook_collection)

  return args
