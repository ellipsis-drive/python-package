from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse
import geopandas as gpd
from shapely import geometry
import numpy as np

from ellipsis.util import chunks
from ellipsis.util import loadingBar
from ellipsis.util.root import stringToDate
from ellipsis.util.root import getActualExtent
from ellipsis.path import get as getInfo

import datetime

def add(pathId,  token, properties = None, description = None, date ={'from': datetime.datetime.now(), 'to': datetime.datetime.now()}):

    pathId = sanitize.validUuid('pathId', pathId, True) 
    token = sanitize.validString('token', token, True)
    date = sanitize.validDateRange('date', date, True)    
    properties = sanitize.validObject('properties', properties, False)
    description = sanitize.validString('description', description, False)

    body = {'properties':properties, 'date': date, 'description':description}
    r = apiManager.post('/path/' + pathId + '/vector/timestamp', body, token)
    return r

def getLocationInfo(pathId, timestampId, locations, epsg = 4326, token= None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, False)
    epsg = sanitize.validInt('epsg', epsg, True)
    body = {'locations':locations,'epsg':epsg}
    r = apiManager.post('/path/' + pathId + '/vector/timestamp/' + timestampId + '/location', body, token)
    return r

def edit(pathId, timestampId, token, description=None, date=None):

    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, True)
    description = sanitize.validString('description', description, False)
    date = sanitize.validDateRange('date', date, False)    

    body = {'date':date,'description':description}
    r = apiManager.patch('/path/' + pathId + '/vector/timestamp/' + timestampId, body, token)
    return r
    

def trash(pathId, timestampId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, True)
    body = {'trashed':True}
    r = apiManager.put('/path/' + pathId + '/vector/timestamp/' + timestampId + '/trashed', body, token)
    return r


def recover(pathId, timestampId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, True)
    body = {'trashed':False}
    r = apiManager.put('/path/' + pathId + '/vector/timestamp/' + timestampId + '/trashed', body, token)
    return r

def delete(pathId, timestampId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, True)
    r = apiManager.delete('/path/' + pathId + '/vector/timestamp/' + timestampId , None, token)
    return r
    

def activate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/vector/timestamp/' + timestampId + '/activate'  , None, token)
    return r

def deactivate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/vector/timestamp/' + timestampId + '/deactivate'  , None, token)
    return r
    
def getBounds(pathId, timestampId, token = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    r = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/bounds' , None, token)

    r = {'id': 0, 'properties':{}, 'geometry':r}
    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union

    return r


def getChanges(pathId, timestampId, token = None, pageStart = None, listAll = False, actions = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    pageStart = sanitize.validObject('pageStart', pageStart, False) 
    actions = sanitize.validObject('actions', actions, False)
    body = {'pageStart':pageStart}    
    def f(body):
        r = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/changelog' , body, token)
        return r
    r = recurse(f, body, listAll)
    r['result'] = [ {**x, 'date':stringToDate(x['date'])} for x in r['result'] ]
    return r



def getFeaturesByIds(pathId, timestampId, featureIds, token = None, showProgress = True, levelOfDetail = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)
    levelOfDetail = sanitize.validInt('levelOfDetail', levelOfDetail, False)
    
    id_chunks = chunks(featureIds, 10)

    r = {'size': 0 , 'result': [], 'nextPageStart' : None}
    ids = id_chunks[0]
    i=0
    for ids in id_chunks:
        body = {'geometryIds': ids, levelOfDetail:levelOfDetail}
        r_new = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/featuresByIds' , body, token)
        
        r['result'] = r['result'] + r_new['result']['features']
        r['size'] = r['size'] + r_new['size']
        if len(id_chunks) >0 and showProgress:
            loadingBar(i*10 + len(ids),len(featureIds))
        i=i+1

    try:
        sh = gpd.GeoDataFrame.from_features(r['result']['features'])
    except:
        for i in range(len(r['result']['features'])):
            if 'crs' in r['result']['features'][i]['properties'].keys():
                del r['result']['features'][i]['properties']['crs']
        sh = gpd.GeoDataFrame.from_features(r['result']['features'])
        

    r['result'] = sh
    return r
    

def getFeaturesByExtent(pathId, timestampId, extent, propertyFilter = None, token = None, listAll = True, pageStart = None, epsg = 4326, coordinateBuffer = None, levelOfDetail = None, onlyIfCenterPointInExtent = False):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    extent = sanitize.validBounds('extent', extent, True)
    levelOfDetail = sanitize.validInt('levelOfDetail', levelOfDetail, False)
    propertyFilter = sanitize.validObject('propertyFilter', propertyFilter, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    epsg = sanitize.validInt('epsg', epsg, True)
    pageStart = sanitize.validObject('pageStart', pageStart, False) 
    coordinateBuffer = sanitize.validFloat('coordinateBuffer', coordinateBuffer, False) 
    if str(type(coordinateBuffer)) == str(type(None)):
        if onlyIfCenterPointInExtent:
            coordinateBuffer = 0
        else:
            info = getInfo(pathId, token)
            ts = [x for x in info['vector']['timestamps'] if x['id'] == timestampId]
            if len(ts) == 0:
                raise ValueError('Given timestampId does not exist')
            t = ts[0]
            zoom = t['zoom']
            coordinateBuffer = 0.5*360 / 2**zoom






    res = getActualExtent(extent['xMin'], extent['xMax'], extent['yMin'], extent['yMax'], 'EPSG:' + str(epsg), 4326)
    if res['status'] == '400':
        raise ValueError('Invalid epsg and extent combination')

    extent_new = res['message']

    extent_new['xMin'] = max(-180, extent['xMin'] - coordinateBuffer)
    extent_new['xMax'] = min(180, extent['xMax'] + coordinateBuffer)
    extent_new['yMin'] = max(-85, extent['yMin'] - coordinateBuffer)
    extent_new['yMax'] = min(85, extent['yMax'] + coordinateBuffer)


    body = {'pageStart': pageStart, 'propertyFilter':propertyFilter, 'extent':extent_new, 'levelOfDetail':levelOfDetail}

    def f(body):
        return apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/featuresByExtent' , body, token)

    r = recurse(f, body, listAll, 'features')

    try:
        sh = gpd.GeoDataFrame.from_features(r['result']['features'])
    except:
        for i in range(len(r['result']['features'])):
            if 'crs' in r['result']['features'][i]['properties'].keys():
                del r['result']['features'][i]['properties']['crs']
        sh = gpd.GeoDataFrame.from_features(r['result']['features'])

        
    if sh.shape[0] ==0:
        r['result'] = sh
        return r

    if onlyIfCenterPointInExtent:
        bounds = sh.bounds
        centerX = (bounds['maxx'].values + bounds['minx'].values )/2
        centerY = (bounds['maxy'].values + bounds['miny'].values )/2
        sh = sh[ np.logical_and(np.logical_and( centerX >= extent['xMin'], centerX <= extent['xMax'] ), np.logical_and( centerY >= extent['yMin'], centerY <= extent['yMax'] )  )  ]

    else:
        bounds = sh.bounds

        sh = sh[ np.logical_and(np.logical_and( bounds['maxx'] >= extent['xMin'], bounds['minx'] <= extent['xMax'] ), np.logical_and( bounds['maxy'] >= extent['yMin'], bounds['miny'] <= extent['yMax'] )  )  ]
    sh.crs = 'EPSG:4326'
    sh = sh.to_crs('EPSG:' + str(epsg))
    r['result'] = sh
    
    return r


def listFeatures(pathId, timestampId, token = None, listAll = True, pageStart = None, levelOfDetail = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    pageStart = sanitize.validObject('pageStart', pageStart, False) 
    levelOfDetail = sanitize.validInt('levelOfDetail', levelOfDetail, False)

    body = {'pageStart': pageStart, 'levelOfDetail':levelOfDetail, 'pageSize':10000}


    def f(body):
        if type(body['pageStart']) == type(None):
            try:
                return  apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/compressedListFeatures' , body, token)
            except:
                return apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/listFeatures' , body, token)                
        else:
            return apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/listFeatures' , body, token)

    r = recurse(f, body, listAll, 'features')



    try:
        sh = gpd.GeoDataFrame.from_features(r['result']['features'])
    except:
        for i in range(len(r['result']['features'])):
            if 'crs' in r['result']['features'][i]['properties'].keys():
                del r['result']['features'][i]['properties']['crs']
        sh = gpd.GeoDataFrame.from_features(r['result']['features'])
    

    sh.crs = {'init': 'epsg:4326'}
    r['result'] = sh

    return r




