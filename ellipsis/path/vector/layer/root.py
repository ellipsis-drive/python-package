from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse
import geopandas as gpd

from ellipsis.util import chunks
from ellipsis.util import loadingBar
from ellipsis.util.root import stringToDate

def add(pathId, name, token, properties = None, description = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    properties = sanitize.validObject('properties', properties, False)
    description = sanitize.validString('description', description, False)

    body = {'name':name, 'properties':properties, 'description':description}
    r = apiManager.post('/path/' + pathId + '/vector/layer', body, token)
    return r

def edit(pathId, layerId, token, description=None, name=None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    description = sanitize.validString('description', description, False)

    body = {'name':name,'description':description}
    r = apiManager.patch('/path/' + pathId + '/vector/layer/' + layerId, body, token)
    return r
    

def archive(pathId, layerId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    body = {'trashed':True}
    r = apiManager.put('/path/' + pathId + '/vector/layer/' + layerId + '/trashed', body, token)
    return r


def recover(pathId, layerId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    body = {'trashed':False}
    r = apiManager.put('/path/' + pathId + '/vector/layer/' + layerId + '/trashed', body, token)
    return r

def delete(pathId, layerId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    r = apiManager.delete('/path/' + pathId + '/vector/layer/' + layerId , None, token)
    return r
    
    
def getBounds(pathId, layerId, token = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    r = apiManager.get('/path/' + pathId + '/vector/layer/' + layerId + '/bounds' , None, token)

    r['id'] = 0
    r['properties'] = {}
    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union

    return r


def getChanges(pathId, layerId, token = None, pageStart = None, listAll = False, actions = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    pageStart = sanitize.validObject('pageStart', pageStart, False) 
    actions = sanitize.validObject('actions', actions, False)
    body = {'pageStart':pageStart}    
    def f(body):
        r = apiManager.get('/path/' + pathId + '/vector/layer/' + layerId + '/changelog' , body, token)
        return r
    
    r = recurse(f, body, listAll)
    r['result'] = [ {**x, 'date':stringToDate(x['date'])} for x in r['result'] ]
    return r

def editFilter(pathId, layerId, propertyFilter, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    propertyFilter = sanitize.validObject('propertyFilter', propertyFilter, True)
    
    body = {'filter': propertyFilter}
    r = apiManager.post('/path/' + pathId + '/vector/layer/' + layerId + '/filter' , body, token)
    return r


def getFeaturesByIds(pathId, layerId, featureIds, token = None, showProgress = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)
    
    id_chunks = chunks(featureIds, 10)

    r = {'size': 0 , 'result': [], 'nextPageStart' : None}
    ids = id_chunks[0]
    i=0
    for ids in id_chunks:
        body = {'geometryIds': ids}
        r_new = apiManager.get('/path/' + pathId + '/vector/layer/' + layerId + '/featuresByIds' , body, token)
        
        r['result'] = r['result'] + r_new['result']['features']
        r['size'] = r['size'] + r_new['size']
        if len(id_chunks) >0 and showProgress:
            loadingBar(i*10 + len(ids),len(featureIds))
        i=i+1

        
    sh = gpd.GeoDataFrame.from_features(r['result'])    
    r['result'] = sh
    return r
    

def getFeaturesByExtent(pathId, layerId, extent, propertyFilter = None, token = None, listAll = True, pageStart = None):
    bounds = extent
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    bounds = sanitize.validBounds('bounds', bounds, True)
    propertyFilter = sanitize.validObject('propertyFilter', propertyFilter, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False) 
    
    body = {'pageStart': pageStart, 'propertyFilter':propertyFilter, 'bounds':bounds}

    def f(body):
        return apiManager.get('/path/' + pathId + '/vector/layer/' + layerId + '/featuresByBounds' , body, token)
        
    r = recurse(f, body, listAll, 'features')

    sh = gpd.GeoDataFrame.from_features(r['result']['features'])
    r['result'] = sh
    return r


def listFeatures(pathId, layerId, token = None, listAll = True, pageStart = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False) 

    body = {'pageStart': pageStart}

    def f(body):
        return apiManager.get('/path/' + pathId + '/vector/layer/' + layerId + '/listFeatures' , body, token)

    r = recurse(f, body, listAll, 'features')

    
    sh = gpd.GeoDataFrame.from_features(r['result']['features'])    
    r['result'] = sh

    return r




