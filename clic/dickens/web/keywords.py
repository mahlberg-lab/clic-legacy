## this is a wsgi-compatible script, receiving request from browser and uWSGI

from webob import Request, Response

from clic.dickens.keywords import Keywords


def application(env, start_response):
    req = Request(env)
    resp = Response()
    form = req.params
    ## Get idx Group: 3gram etc
    testIdxGroup = form.get('testIdxGroup', 'idx')
    ## Get idx Mod: quote, non-quote etc.
    testIdxMod = form.get('testIdxMod', '')
    ## idx Name is a combination of Mod and Group (in that order)
    testIdxName = "{0}-{1}".format(testIdxMod, testIdxGroup)
    if testIdxName == '-idx': ## if no Mod or Group is defined use sentence idx as default
        testIdxName = 'sentence-idx'
    testMaterials = form.getall('testMaterial')
    # Get rafe values as above
    refIdxGroup = form.get('refIdxGroup', 'idx')
    refIdxMod = form.get('refIdxMod', '')
    refIdxName = "{0}-{1}".format(refIdxMod, refIdxGroup)
    if refIdxName == '-idx':
        refIdxName = 'sentence-idx'
    refMaterials = form.getall('refMaterial')
    
    keyworder = Keywords()
#     resp.json = keyworder.list_keywords(testIdxName, testMaterials,
#                                         refIdxName, refMaterials
#                                         )
    resp.json = keyworder.list_keywords('quote-3gram-idx', ['dickens'],
                                        'non-quote-3gram-idx', ['dickens']
                                        )
    return resp(env, start_response)

    
