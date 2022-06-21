from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse
from ellipsis.util.root import stringToDate

def searchRaster(root=None, name=None, fuzzySearchOnName=False, userId=None, disabled=False, canView=None, pageStart=None, hashtag=None, bounds=None, bands=None, resolution=None, dateFrom=None, dateTo=None, hasTimestamp=None, timestampSize=None, listAll= False, token=None):
    token = sanitize.validString('token', token, False)
    root = sanitize.validStringArray('root', root, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    name = sanitize.validString('name', name, False)
    fuzzySearchOnName = sanitize.validBool(
        'fuzzySearchOnName', fuzzySearchOnName, True)
    userId = sanitize.validUuid('userId', userId, False)
    disabled = sanitize.validBool('disabled', disabled, True)
    canView = sanitize.validBool('canView', canView, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    hashtag = sanitize.validString('hashtag', hashtag, False)
    bounds = sanitize.validBounds('bounds', bounds, False)
    bands = sanitize.validStringArray('bands', bands, False)
    dateFrom = sanitize.validDate('dateFrom', dateFrom, False)
    dateTo = sanitize.validDate('dateTo', dateTo, False)
    hasTimestamp = sanitize.validBool('hasTimestamp', hasTimestamp, False)
    timestampSize = sanitize.validFloat('timestampSize', timestampSize, False)
    resolution = sanitize.validFloatArray('resolution', resolution, False)

    body = {
        'type': ['raster'],
        'root': root,
        'name': name,
        'fuzzySearchOnName': fuzzySearchOnName,
        'userId': userId,
        'disabled': disabled,
        'canView': canView,
        'pagestart': pageStart,
        'hashtag': hashtag,
        'bounds': bounds,
        'bands': bands,
        'resolution': resolution,
        'dateFrom': dateFrom,
        'dateTo': dateTo,
        'hasTimestamp': hasTimestamp, 'timestampSize': timestampSize
    }
    
    def f(body):
        return apiManager.get('/path', body, token)
    
    r = recurse(f, body, listAll)
    return r


def searchVector(root=None, name=None, fuzzySearchOnName=False, userId=None, disabled=False, canView=None, pageStart=None, hashtag=None, bounds=None, hasVectorLayers=None, layerName=None, fuzzySearchOnLayerName=None, listAll=False, token=None):
    token = sanitize.validString('token', token, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    root = sanitize.validStringArray('root', root, False)
    name = sanitize.validString('name', name, False)
    fuzzySearchOnName = sanitize.validBool(
        'fuzzySearchOnName', fuzzySearchOnName, True)
    userId = sanitize.validUuid('userId', userId, False)
    disabled = sanitize.validBool('disabled', disabled, True)
    canView = sanitize.validBool('canView', canView, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    hashtag = sanitize.validString('hashtag', hashtag, False)
    bounds = sanitize.validBounds('bounds', bounds, False)
    hasVectorLayers = sanitize.validBool(
        'hasVectorLayers', hasVectorLayers, False)
    layerName = sanitize.validString('layerName', layerName, False)
    fuzzySearchOnLayerName = sanitize.validBool(
        'fuzzySearchOnLayerName', fuzzySearchOnLayerName, False)

    if root != None and token == None and (len(root) > 1 or root[0] != 'public'):
        raise ValueError(
            "When no token is given the root can only be ['public'']")

    body = {
        'type': ['vector'],
        'root': root,
        'name': name,
        'fuzzySearchOnName': fuzzySearchOnName,
        'userId': userId,
        'disabled': disabled,
        'canView': canView,
        'pagestart': pageStart,
        'hashtag': hashtag,
        'bounds': bounds,
        'hasVectorLayers': hasVectorLayers,
        'layerName': layerName,
        'fuzzySearchOnLayerName': fuzzySearchOnLayerName
    }

    def f(body):
        return apiManager.get('/path', body, token)

    r = recurse(f, body, listAll)
    
    return r

# retrieving all pages depricated
def searchFolder(root=None, name=None, fuzzySearchOnName=False, userId=None, pageStart=None, listAll = False, token=None):
    token = sanitize.validString('token', token, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    root = sanitize.validStringArray('root', root, False)
    name = sanitize.validString('name', name, False)
    fuzzySearchOnName = sanitize.validBool(
        'fuzzySearchOnName', fuzzySearchOnName, True)
    userId = sanitize.validUuid('userId', userId, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)

    if root != None and token == None and (len(root) > 1 or root[0] != 'public'):
        raise ValueError(
            "When no token is given the root can only be ['public'']")

    body = {
        'type': ['folder'],
        'root': root,
        'name': name,
        'fuzzySearchOnName': fuzzySearchOnName,
        'userId': userId,
        'pagestart': pageStart
    }
    
    def f(body):
        return (apiManager.get('/path', body, token))

    r = recurse(f, body, listAll)
    return r


def get(pathId, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    r = apiManager.get(f"/path/{pathId}", None, token)
    r = convertPath(r)
    return r

def listMaps(pathId, pageStart=None, listAll = True, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, False)

    body  = {'pageStart': pageStart, 'isFolder':False}
    
    def f(body):
        
        return apiManager.get(f'/path/{pathId}/list', body, token)

    r = recurse(f, body, listAll)
    return r

def listFolders(pathId, pageStart=None, listAll = True, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, False)

    body  = {'pageStart': pageStart, 'isFolder':True}
    
    def f(body):
        
        return apiManager.get(f'/path/{pathId}/list', body, token)

    r = recurse(f, body, listAll)
    return r

def editMetadata(pathId, token, description=None, attribution=None, properties=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, True)
    attribution = sanitize.validString('attribution', attribution, False)
    description = sanitize.validString('description', description, False)
    properties = sanitize.validObject('properties', properties, False)

    return apiManager.patch(f'/path/{pathId}/metadata', {
        'description': description,
        'attribution': attribution,
        'properties': properties
    }, token)


def add( pathType, name, token, parentId = None, publicAccess =None, metadata=None):
    pathType = sanitize.validString('pathType', pathType, True)
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    parentId = sanitize.validUuid('parentId', parentId, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)

    body = {'name': name, 'parentId':parentId, 'type': pathType, 'publicAccess':publicAccess, 'metadata':metadata }

    return apiManager.post('/path', body, token)

def rename(pathId, name, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    name = sanitize.validString('name', name, False)

    return apiManager.put(f'/path/{pathId}/name', {
        'name': name
    }, token)


def move(pathIds, parentId, token):
    token = sanitize.validString('token', token, False)
    pathIds = sanitize.validUuidArray('pathIds', pathIds, True)
    parentId = sanitize.validUuid('parentId', parentId, False)

    return apiManager.put('/path/parentId', {
        'pathIds': pathIds,
        'parentId': parentId,
    }, token)


def trash(pathId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)

    return apiManager.put(f'/path/{pathId}/trashed', {
        'trashed': True
    }, token)


def recover(pathId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)

    return apiManager.put(f'/path/{pathId}/trashed', {
        'trashed': False
    }, token)


def delete(pathId, token, recursive = False):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    recursive = sanitize.validBool('recursive', recursive, True)
    
    if recursive:
        info = get(pathId, token)
        if info['type'] == 'folder':
            folders = listFolders(pathId, token=token)['result']
            for f in folders:
                delete(f['id'], token, True)
            maps = listMaps(pathId, token=token)['result']
            for m in maps:
                delete(m['id'], token, True)
        apiManager.delete(f'/path/{pathId}', None, token)            
    
    else:
        return apiManager.delete(f'/path/{pathId}', None, token)

def editPublicAccess(pathId, token, accessLevel=None, hidden=None, processingUnits=None, geoFence=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    geoFence = sanitize.validObject('geoFence', geoFence, False)
    accessLevel = sanitize.validInt('accessLevel', accessLevel, False)
    processingUnits = sanitize.validInt('processingUnits', processingUnits, False)
    hidden = sanitize.validBool('hidden', hidden, False)
    body = {'accessLevel':accessLevel, 'processingUnits':processingUnits, 'geoFence':geoFence, 'hidden': hidden}    
    
    return apiManager.patch('/path/' + pathId + '/publicAccess', body, token)
    
def favorite(pathId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    body = {'favorite':True}
    return apiManager.put(f'/path/{pathId}/favorite', body, token)
    
    
def unfavorite(pathId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    body = {'favorite':False}
    return apiManager.put(f'/path/{pathId}/favorite', body, token)
    
##helper function
    
def convertPath(path):
    if path['type'] == 'raster':
        path['raster']['timestamps'] = [ {**x, 'dateFrom' : stringToDate(x['dateFrom']), 'dateTo' : stringToDate(x['dateTo']) } for x in path['raster']['timestamps'] ]
    return(path)

