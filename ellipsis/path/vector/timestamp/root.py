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



def getFeaturesByIds(pathId, timestampId, featureIds, token = None, showProgress = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)
    
    id_chunks = chunks(featureIds, 10)

    r = {'size': 0 , 'result': [], 'nextPageStart' : None}
    ids = id_chunks[0]
    i=0
    for ids in id_chunks:
        body = {'geometryIds': ids}
        r_new = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/featuresByIds' , body, token)
        
        r['result'] = r['result'] + r_new['result']['features']
        r['size'] = r['size'] + r_new['size']
        if len(id_chunks) >0 and showProgress:
            loadingBar(i*10 + len(ids),len(featureIds))
        i=i+1

        
    sh = gpd.GeoDataFrame.from_features(r['result'])    
    r['result'] = sh
    return r
    

def getFeaturesByExtent(pathId, timestampId, extent, propertyFilter = None, token = None, listAll = True, pageStart = None, epsg = 4326, coordinateBuffer = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    extent = sanitize.validBounds('extent', extent, True)
    propertyFilter = sanitize.validObject('propertyFilter', propertyFilter, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    pageStart = sanitize.validObject('pageStart', pageStart, False) 
    coordinateBuffer = sanitize.validFloat('coordinateBuffer', coordinateBuffer, False) 

    if str(type(coordinateBuffer)) == str(type(None)):
        info = getInfo(pathId, token)
        ts = [x for x in info['vector']['timestamps'] if x['id'] == timestampId]
        if len(ts) == 0:
            raise ValueError('Given timestampId does not exist')
        t = ts[0]
        zoom = t['zoom']
        coordinateBuffer = 0.5*360 / 2**zoom


    p = geometry.Polygon( [(extent['xMin'], extent['yMin']), (extent['xMin'], extent['yMax']),(extent['xMax'], extent['yMax']),(extent['xMax'], extent['yMin'])] )
    p = gpd.GeoDataFrame({'geometry':[p]})


    res = getActualExtent(extent['xMin'], extent['xMax'], extent['yMin'], extent['yMax'], 'EPSG:' + str(epsg))
    if res['status'] == '400':
        raise ValueError('Invalid epsg and extent combination')
        
    extent = res['message']


    extent['xMin'] = min(-180, extent['xMin'] - coordinateBuffer)
    extent['xMax'] = max(180, extent['xMax'] + coordinateBuffer)
    extent['yMin'] = min(-85, extent['yMin'] - coordinateBuffer)
    extent['yMax'] = max(85, extent['yMax'] + coordinateBuffer)

    try:
        p.crs = 'EPSG:' + str(epsg)
        p = p.to_crs('EPSG:4326')
    except:
        raise ValueError('Invalid crs given')
    extent = p.bounds
    extent = {'xMin': extent['minx'].values[0], 'xMax': extent['maxx'].values[0], 'yMin': extent['miny'].values[0], 'yMax': extent['maxy'].values[0] }        
    
    
    body = {'pageStart': pageStart, 'propertyFilter':propertyFilter, 'extent':extent}

    def f(body):
        return apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/featuresByExtent' , body, token)
        
    r = recurse(f, body, listAll, 'features')

    sh = gpd.GeoDataFrame.from_features(r['result']['features'])
    if sh.shape[0] ==0:
        r['result'] = sh
        return r
    bounds = sh.bounds
    px = (bounds['minx'] + bounds['maxx']) /2
    py = (bounds['miny'] + bounds['maxy']) /2
    sh = sh[ np.logical_and(np.logical_and( px >= extent['xMin'], px <= extent['xMax'] ), np.logical_and( py >= extent['yMin'], py <= extent['yMax'] )  )  ]
    sh.crs = 'EPSG:4326'
    sh = sh.to_crs('EPSG:' + str(epsg))
    r['result'] = sh
    
    return r


def listFeatures(pathId, timestampId, token = None, listAll = True, pageStart = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    pageStart = sanitize.validObject('pageStart', pageStart, False) 

    body = {'pageStart': pageStart}

    def f(body):
        return apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/listFeatures' , body, token)

    r = recurse(f, body, listAll, 'features')

    
    sh = gpd.GeoDataFrame.from_features(r['result']['features'])    
    sh.crs = {'init': 'epsg:4326'}
    r['result'] = sh

    return r




