import re

from webob import Request, Response

from clic.dickens.concordancer import Concordancer

def paramHandler(params):
    form = params
    print vars(form)
    
    ## NOTE: No idxGroup, search based on phrase defined by user
    idxMod = form.get('idxMod', '')
    
    args = []
    if not idxMod == '':
        idxName = idxMod + '-idx'
    else:
        idxName = 'sentence-idx'
    args.insert(0, idxName)
    
    book_collection = []
    for i, w in enumerate(form.keys()):
        if w == 'testCollection':
            book_collection.append(form.values()[i])
    
    args.insert(1, book_collection)
    
    return args