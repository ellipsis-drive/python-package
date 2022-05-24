from ellipsis import apiManager
from ellipsis import sanitize


def searchRaster(root=None, name=None, fuzzySearchOnName=False, userId=None, disabled=False, canView=None, pageStart=None, hashtag=None, bounds=None, bands=None, resolution=None, dateFrom=None, dateTo=None, hasTimestamp=None, timestampSize=None, token=None):
    token = sanitize.validString('token', token, False)
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
    bands = sanitize.validStringArray('bands', bands, False)
    dateFrom = sanitize.validDate('dateFrom', dateFrom, False)
    dateTo = sanitize.validDate('dateTo', dateFrom, False)
    hasTimestamp = sanitize.validBool('hasTimestamp', hasTimestamp, False)
    timestampSize = sanitize.validFloat('timestampSize', timestampSize, False)
    resolution = sanitize.validFloatArray('resolution', resolution, False)

    return apiManager.get('/path', {
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
    }, token)


def searchVector(root=None, name=None, fuzzySearchOnName=False, userId=None, disabled=False, canView=None, pageStart=None, hashtag=None, bounds=None, hasVectorLayers=None, layerName=None, fuzzySearchOnLayerName=None, token=None):
    token = sanitize.validString('token', token, False)
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

    return apiManager.get('/path', {
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
    }, token)


# retrieving all pages depricated
def searchFolder(root=None, name=None, fuzzySearchOnName=False, userId=None, pageStart=None, token=None):
    token = sanitize.validString('token', token, False)
    root = sanitize.validStringArray('root', root, False)
    name = sanitize.validString('name', name, False)
    fuzzySearchOnName = sanitize.validBool(
        'fuzzySearchOnName', fuzzySearchOnName, True)
    userId = sanitize.validUuid('userId', userId, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)

    if root != None and token == None and (len(root) > 1 or root[0] != 'public'):
        raise ValueError(
            "When no token is given the root can only be ['public'']")

    return (apiManager.get('/path', {
        'type': ['folder'],
        'root': root,
        'name': name,
        'fuzzySearchOnName': fuzzySearchOnName,
        'userId': userId,
        'pagestart': pageStart
    }, token))


def get(pathId=None, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    return apiManager.get(f"/path/{pathId}", None, token)


# This is supposed to be private
def list(pathId=None, token=None, isFolder=False, pageSize=None, pageStart=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    pageSize = sanitize.validInt('pageSize', pageSize, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)

    return apiManager.get(f'/path/{pathId}/list', {
        'pageStart': pageStart,
        'pageSize': pageSize,
    }, token)


def listFolders(pathId=None, token=None, pageSize=None, pageStart=None):
    return list(pathId, token, True, pageSize, pageStart)


def listFiles(pathId=None, token=None, pageSize=None, pageStart=None):
    return list(pathId, token, False, pageSize, pageStart)


def editMetaData(pathId=None, token=None, description=None, attribution=None, properties=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    attribution = sanitize.validString('attribution', attribution, False)
    properties = sanitize.validDict('properties', properties, False)

    return apiManager.patch(f'/path/{pathId}/metadata', {
        'description': description,
        'attribution': attribution,
        'properties': properties
    }, token)


def rename(pathId=None, token=None, name=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    name = sanitize.validString('name', name, False)

    return apiManager.put(f'/path/{pathId}/name', {
        'name': name
    }, token)


def movePaths(token=None, pathIds=None, parentId=None):
    token = sanitize.validString('token', token, False)
    pathIds = sanitize.validUuidArray('pathIds', pathIds, True)
    parentId = sanitize.validUuid('parentId', parentId, False)

    return apiManager.put('/path/parentId', {
        'pathIds': pathIds,
        'parentId': parentId,
    }, token)


def setTrashed(pathId=None, token=None, trashed=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    trashed = sanitize.validBool('trashed', trashed, True)

    return apiManager.put(f'/path/{pathId}/trashed', {
        'trashed': trashed
    }, token)


def delete(pathId=None, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    return apiManager.delete(f'/path/{pathId}', None, token)

# NOT IMPLEMENTED: edit access, favorite, request access
