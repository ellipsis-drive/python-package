
from ellipsis import apiManager
from ellipsis import sanitize

def searchRaster(root = ['myDrive', 'sharedWithMe', 'favorites'], name = None, fuzzySearchOnName = False, userId = None, disabled = False, canView = None, pageStart = None, hashtag = None, bounds = None, bands = None, resolution = None, dateFrom = None, dateTo = None, hasTimestamp = None, timestampSize = None, token = None):


    root = sanitize.validRootArray('root', root, True)    
    name = sanitize.validString('name', name, False)    
    fuzzySearchOnName = sanitize.validBool('fuzzySearchOnName', fuzzySearchOnName, True)
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
    
    if timestampSize < 0:
        raise ValueError("timestampSize must be at least 0")

    if if dateFrom != None and dateTo != None and dateFrom > dateTo:
        raise ValueError("dateFrom must be smaller than date To")

    
    if type(resolution) != type(None)
        try:
            resolution = list(resolution)
            resolution = [float(resolution[0]), float(resolution[1])]
        except:
            raise ValueError('resolution must ba a list with two floats, the second float must be greater than the first small')
        if resolution[0] > resolution[1]:
            raise ValueError('resolution must ba a list with two floats, the second float must be greater than the first small')
    


    body = {'root': root, 'name':name, 'fuzzySearchOnName':fuzzySearchOnName, 'userId':userId, 'disabled':disabled, 'canView':canView, 'pagestart':pageStart, 'hashtag':hashtag, 'bounds':bounds, 'bands':bands, 'resolution':resolution, 'dateFrom':dateFrom, 'dateTo':dateTo, 'hasTimestamp': hasTimestamp, 'timestampSize':timestampSize}
    r = apiManager.get('/path', body, token)

    return(r)

def searchVector(root = ['myDrive', 'sharedWithMe', 'favorites'], name = None, fuzzySearchOnName = False, userId = None, disabled = False, canView = None, pageSize = None, pageStart = None, hashtag = None, bounds = None, hasVectorLayers = None, layerName = None, fuzzySearchOnLayerName = None, featureSize = None, seriesSize = None, messageSize = None, token = None, firstPageOnly = True)):
    body = {'root': root, 'type': ['vector']}

    dictAdd(body, "hasVectorLayers", hasVectorLayers)
    dictAdd(body, "layerName", layerName)
    dictAdd(body, "fuzzySearchOnLayerName", fuzzySearchOnLayerName)
    dictAdd(body, "featureSize", featureSize)
    dictAdd(body, "seriesSize", seriesSize)
    dictAdd(body, "messageSize", messageSize)
    
    dictAdd(body, "root", root)
    dictAdd(body, "name", name)
    dictAdd(body, "fuzzySearchOnName", fuzzySearchOnName)
    dictAdd(body, "userId", userId)
    dictAdd(body, "disabled", disabled)
    dictAdd(body, "canView", canView)
    dictAdd(body, "pageSize", pageSize)
    dictAdd(body, "pageStart", pageStart)
    dictAdd(body, "hashtag", hashtag)
    dictAdd(body, "bounds", bounds)

    keepGoing = True
    results = []
    while keepGoing:
        if token == None:
            r = s.get(f"{URL}/path?{urllib.parse.urlencode(body)}")
        else:
            r = s.get(f"{URL}/path?{urllib.parse.urlencode(body)}", headers = {"Authorization":token} )
        
        if r.status_code != 200:
            raise ValueError(r.text)
            
        result = r.json()
        body['pageStart'] = result['nextPageStart']

        results = results + result['result']
        result = result['result']

        if firstPageOnly:
            keepGoing = False
        if len(result) < pageSize:
            keepGoing = False
        results = results + result


    return(results)

    

def searchFolder(root = ['myDrive', 'sharedWithMe', 'favorites'], name = None, fuzzySearchOnName = False, userId = None, disabled = False, canView = None, pageSize = None, pageStart = None, hashtag = None, bounds = None, token = None, firstPageOnly = True):
    body = {'root': root, 'type': ['folder']}
    
    dictAdd(body, "root", root)
    dictAdd(body, "name", name)
    dictAdd(body, "fuzzySearchOnName", fuzzySearchOnName)
    dictAdd(body, "userId", userId)
    dictAdd(body, "disabled", disabled)
    dictAdd(body, "canView", canView)
    dictAdd(body, "pageSize", pageSize)
    dictAdd(body, "pageStart", pageStart)
    dictAdd(body, "hashtag", hashtag)
    dictAdd(body, "bounds", bounds)

    if bounds is not None:
        bounds = {'xMin':float(bounds['xMin']), 'xMax':float(bounds['xMax']), 'yMin':float(bounds['yMin']), 'yMax':float(bounds['yMax'])}
        body['bounds'] = bounds

    keepGoing = True
    results = []
    while keepGoing:
        if token == None:
            r = s.get(f"{URL}/path?{urllib.parse.urlencode(body)}")
        else:
            r = s.get(f"{URL}/path?{urllib.parse.urlencode(body)}", headers = {"Authorization":token} )
        
        if r.status_code != 200:
            raise ValueError(r.text)
            
        result = r.json()
        body['pageStart'] = result['nextPageStart']

        results = results + result['result']
        result = result['result']

        if firstPageOnly:
            keepGoing = False
        if len(result) < 20:
            keepGoing = False
        results = results + result


    return(results)

"""
def searchPaths(name = None, fuzzySearchOnName = False, root = ['myDrive', 'sharedWithMe', 'favorites'], firstPageOnly = True, bounds = None, userId= None, resolution=None,  dateFrom=None, dateTo= None, hashtag = None, token = None):
    body = {'root': root, 'pageSize':20}

    if name is not None:
        body['name'] = name

    body['fuzzySearchOnName'] = fuzzySearchOnName        

    if userId is not None:
        body['userId'] = userId

    if dateFrom is not None:
        body['dateFrom'] = dateFrom.strftime('%Y-%m-%d %H:%M:%S')

    if dateTo is not None:
        body['dateTo'] = dateTo.strftime('%Y-%m-%d %H:%M:%S')

    if resolution is not None:
        body['resolution'] = resolution

    if hashtag is not None:
        body['hashtag'] = hashtag

    if bounds is not None:
        bounds = {'xMin':float(bounds['xMin']), 'xMax':float(bounds['xMax']), 'yMin':float(bounds['yMin']), 'yMax':float(bounds['yMax'])}
        body['bounds'] = bounds

    keepGoing = True
    results = []
    while keepGoing:
        if token == None:
            r = s.get(url + '/path?' + urllib.parse.urlencode(body) )
        else:
            r = s.get(url + '/path?' + urllib.parse.urlencode(body), headers = {"Authorization":token} )
        
        if r.status_code != 200:
            raise ValueError(r.text)
            
        result = r.json()
        body['pageStart'] = result['nextPageStart']

        results = results + result['result']
        result = result['result']

        if firstPageOnly:
            keepGoing = False
        if len(result) < 20:
            keepGoing = False
        results = results + result


    return(results)
"""