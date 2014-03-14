from webob import Request, Response

from clic.dickens.clusters import Clusters

def application(env, start_response):
    req = Request(env) ## interpret request coming in
    resp = Response() ## set up response to be made
    form = req.params ## return paramaters in request form
    ## Get index group: 3-gram etc.
    IdxGroup = form.get('IdxGroup', 'idx')
    ## Get index mode: quote etc.
    IdxMod = form.get('IdxMod', '')
    IdxName = "{0}-{1}".format(IdxMod, IdxGroup)
    ## set default idx to sentence if not group idx is given
    if IdxName == '-idx':
        IdxName = 'sentence-idx'
    ## Get material: All Dickens, specified books etc.
    Materials = form.getall('Material')
    cluster = Clusters()
    ## return cluster analysis based on specified IdxName and Materials
    resp.json = cluster.list_clusters(IdxName, Materials)
    return resp(env, start_response)