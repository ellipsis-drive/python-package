from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse
from ellipsis.util.root import stringToDate
from ellipsis.path.folder.root import listFolder

def search(pathTypes = ['raster', 'vector', 'file', 'folder'] ,root=None, text=None, active=None, userId=None, pageStart=None, hashtag=None, extent=None, resolution=None, date=None, listAll= False, token=None):

    token = sanitize.validString('token', token, False)
    pathTypes = sanitize.validStringArray('pathTypes', pathTypes, True)
    root = sanitize.validStringArray('root', root, False)
    text = sanitize.validString('text', text, False)
    userId = sanitize.validUuid('userId', userId, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    hashtag = sanitize.validString('hashtag', hashtag, False)



    listAll = sanitize.validBool('listAll', listAll, True)

    active = sanitize.validBool('active', active, False)

    extent = sanitize.validBounds('extent', extent, False)
    
    date = sanitize.validDateRange('date', date, False)


    resolution = sanitize.validResolution('resolution', resolution, False)

    body = {
        'type': pathTypes,
        'root': root,
        'text': text,
        'userId': userId,
        'active': active,
        'pageStart': pageStart,
        'hashtag': hashtag,
        'extent': extent,
        'resolution': resolution,
        'date':date
    }

    def f(body):
        return apiManager.get('/path', body, token)
    
    r = recurse(f, body, listAll)
    return r



def get(pathId, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    r = apiManager.get(f"/path/{pathId}", None, token)
    r = convertPath(r)
    return r

def setDomains(pathId, token, domains):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, True)
    domains = sanitize.validStringArray('domains', domains, False)
    body = {'domains': domains}
    r = apiManager.put(f"/path/{pathId}/domain", body, token)
    return r


####depricated
def listPath(pathId, pathType, pageStart=None, listAll = True, token=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, False)

    if type(pathType) != type('x') or (pathType != 'folder' and pathType !='layer' ) :
        raise ValueError("pathType must be one of 'layer' or 'folder'")
        
    isFolder = False
    if pathType == 'folder':
        isFolder = True        


    body  = {'pageStart': pageStart, 'isFolder':isFolder}
    
    def f(body):
        
        return apiManager.get(f'/path/{pathId}/list', body, token)

    r = recurse(f, body, listAll)
    return r


def editMetadata(pathId, token, description=None, attribution=None, licenseString =None, properties=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, True)
    attribution = sanitize.validString('attribution', attribution, False)
    description = sanitize.validString('description', description, False)
    properties = sanitize.validObject('properties', properties, False)
    licenseString = sanitize.validString('licenseString', licenseString, False)
    return apiManager.patch(f'/path/{pathId}/metadata', {
        'description': description,
        'attribution': attribution,
        'properties': properties,
        'license': licenseString
    }, token)

#####depricated
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
            folders = listFolder(pathId = pathId, includeTrashed=True, pathTypes=['folder'], token=token)['result']
            for f in folders:
                delete(f['id'], token, True)
            maps = listFolder(pathId=pathId, pathTypes=['raster','vector','file', 'pointCloud'], includeTrashed=True, token=token)['result']
            for m in maps:
                delete(m['id'], token, True)
        apiManager.delete(f'/path/{pathId}', None, token)            
    
    else:
        return apiManager.delete(f'/path/{pathId}', None, token)

def editPublicAccess(pathId, token, access = None, hidden=None, recursive = False):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)

    access = sanitize.validObject('access', access, False)
    hidden = sanitize.validBool('hidden', hidden, False)
    recursive = sanitize.validBool('recursive', recursive, True)

    if type(hidden) == type(None) and type(access) == type(None):
        raise ValueError('hidden and access cannot both be None')

    body = access
    body['hidden'] =  hidden



    if recursive:
        info = get(pathId, token)
        if info['type'] == 'folder':
            folders = listFolder(pathId=pathId, includeTrashed=False, pathTypes=['folder'], token=token)['result']
            for f in folders:
                editPublicAccess(pathId = f['id'], token = token, recursive = True, hidden = hidden, access = access)
            maps =  listFolder(pathId=pathId, pathTypes=['raster', 'vector', 'file', 'pointCloud'], includeTrashed=False, token=token)['result']
            for m in maps:
                editPublicAccess(pathId = m['id'], token = token, access=access, hidden = hidden, recursive = True)
        return apiManager.patch('/path/' + pathId + '/publicAccess', body, token)


    else:
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
        path['raster']['timestamps'] = [ {**x, 'date' : {'from':stringToDate(x['date']['from']), 'to' : stringToDate(x['date']['to']) }} for x in path['raster']['timestamps'] ]
    if path['type'] == 'vector':
        path['vector']['timestamps'] = [ {**x, 'date' : {'from':stringToDate(x['date']['from']), 'to' : stringToDate(x['date']['to']) }} for x in path['vector']['timestamps'] ]
        
    return(path)

