## this is a wsgi-compatible script, receiving request from browser and uWSGI

from webob import Request, Response

from clic.dickens.keywords import Keywords


def application(env, start_response):
    req = Request(env)
    resp = Response()
    form = req.params
    testIdxGroup = form.get('testIdxGroup', 'idx')
    testIdxMod = form.get('testIdxMod', '')
    testIdxName = "{0}-{1}".format(testIdxMod, testIdxGroup)
    if testIdxName == '-idx':
        testIdxName = 'sentence-idx'
    testMaterials = form.getall('testMaterial')
    # Get rafe values as above
    keyworder = Keywords()
    resp.json = keyworder.list_keywords(testIdxName, testMaterials,
                                        refIdxName, refMaterials
                                        )
    return resp(env, start_response)

    
