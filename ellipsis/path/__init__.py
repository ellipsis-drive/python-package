
from ellipsis import apiManager
from ellipsis import sanitize

def searchRaster(root = None, name = None, fuzzySearchOnName = False, userId = None, disabled = False, canView = None, pageStart = None, hashtag = None, bounds = None, bands = None, resolution = None, dateFrom = None, dateTo = None, hasTimestamp = None, timestampSize = None, token = None):


    root = sanitize.validRootArray('root', root, False)    
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
    
    if timestampSize != None and timestampSize < 0:
        raise ValueError("timestampSize must be at least 0")

    if dateFrom != None and dateTo != None and dateFrom > dateTo:
        raise ValueError("dateFrom must be smaller than date To")

    
    if type(resolution) != type(None):
        try:
            resolution = list(resolution)
            resolution = [float(resolution[0]), float(resolution[1])]
        except:
            raise ValueError('resolution must ba a list with two floats, the second float must be greater than the first small')
        if resolution[0] > resolution[1]:
            raise ValueError('resolution must ba a list with two floats, the second float must be greater than the first small')
    


    if type(root) != type(None) and token == None and (len(root) > 1  or root[0] != 'public'):
        raise ValueError("When no token is given the root can only be ['public'']")

    body = {'root': root, 'name':name, 'fuzzySearchOnName':fuzzySearchOnName, 'userId':userId, 'disabled':disabled, 'canView':canView, 'pagestart':pageStart, 'hashtag':hashtag, 'bounds':bounds, 'bands':bands, 'resolution':resolution, 'dateFrom':dateFrom, 'dateTo':dateTo, 'hasTimestamp': hasTimestamp, 'timestampSize':timestampSize}
    r = apiManager.get('/path', body, token)

    return(r)

##retrieving all pages depricated
def searchVector(root = ['myDrive', 'sharedWithMe', 'favorites'], name = None, fuzzySearchOnName = False, userId = None, disabled = False, canView = None, pageSize = None, pageStart = None, hashtag = None, bounds = None, hasVectorLayers = None, layerName = None, fuzzySearchOnLayerName = None, featureSize = None, seriesSize = None, messageSize = None, token = None, firstPageOnly = True):



    return(None)

    
##retrieving all pages depricated
def searchFolder(root = ['myDrive', 'sharedWithMe', 'favorites'], name = None, fuzzySearchOnName = False, userId = None, disabled = False, canView = None, pageSize = None, pageStart = None, hashtag = None, bounds = None, token = None, firstPageOnly = True):
    return(None)


