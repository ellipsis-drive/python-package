from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse
import geopandas as gpd

def add(pathId, name, token, properties = None, description = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    properties = sanitize.validObject('properties', properties, False)
    description = sanitize.validString('description', description, False)

    body = {'name':name, 'properties':properties, 'description':description}
    r = apiManager.post('/path/' + pathId + '/layer', body, token)
    return r

def edit(pathId, layerId, description, name, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    description = sanitize.validString('description', description, False)

    body = {'name':name,'description':description}
    r = apiManager.patch('/path/' + pathId + '/layer/' + layerId, body, token)
    return r
    

def archive(pathId, layerId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    body = {'trashed':True}
    r = apiManager.patch('/path/' + pathId + '/layer/' + layerId + '/trashed', body, token)
    return r


def recover(pathId, layerId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    body = {'trashed':False}
    r = apiManager.patch('/path/' + pathId + '/layer/' + layerId + '/trashed', body, token)
    return r

def delete(pathId, layerId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    r = apiManager.delete('/path/' + pathId + '/layer/' + layerId , None, token)
    return r
    
    
def getBounds(pathId, layerId, token = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    r = apiManager.delete('/path/' + pathId + '/layer/' + layerId + '/bounds' , None, token)

    r['id'] = 0
    r['properties'] = {}
    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union

    return r


def getChanges(pathId, layerId, token = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    r = apiManager.get('/path/' + pathId + '/layer/' + layerId + '/changelog' , None, token)
    return r

def editFilter(pathId, layerId, propertyFilter, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    propertyFilter = sanitize.validObject('propertyFilter', propertyFilter, True)
    
    body = {'filter': propertyFilter}
    r = apiManager.post('/path/' + pathId + '/layer/' + layerId + '/filter' , body, token)
    return r


def getFeaturesByIds(pathId, layerId, featureIds, token = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)
    body = {'featureIds': featureIds}
    r = apiManager.get('/path/' + pathId + '/layer/' + layerId + '/featureByIds' , body, token)
        
    r = gpd.GeoDataFrame.from_features(r['result']['features'])    
    return r
    

def getFeaturesByBounds(pathId, layerId, bounds, propertyFilter = None, token = None, listAll = True, pageStart = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    bounds = sanitize.validBounds('bounds', bounds, True)
    propertyFilter = sanitize.validObject('propertyFilter', propertyFilter, True)
    listAll = sanitize.validObject('listAll', listAll, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False) 

    body = {'pageStart': pageStart, 'propertyFilter':propertyFilter, 'bounds':bounds}

    def f(body):
        return apiManager.get('/path/' + pathId + '/layer/' + layerId + '/featureByBounds' , body, token)
        
    r = recurse(f, body, listAll, 'features')

    r = gpd.GeoDataFrame.from_features(r['result']['features'])    
    return r


def listFeatures(pathId, layerId, token = None, listAll = True, pageStart = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    listAll = sanitize.validObject('listAll', listAll, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False) 

    body = {'pageStart': pageStart}

    def f(body):
        return apiManager.get('/path/' + pathId + '/layer/' + layerId + '/listFeatures' , body, token)

    r = recurse(f, body, listAll, 'features')

    
    r = gpd.GeoDataFrame.from_features(r['result']['features'])    
    return r




