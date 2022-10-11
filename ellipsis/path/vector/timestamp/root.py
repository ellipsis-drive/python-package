from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse
import geopandas as gpd

from ellipsis.util import chunks
from ellipsis.util import loadingBar
from ellipsis.util.root import stringToDate

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
    

def getFeaturesByExtent(pathId, timestampId, extent, propertyFilter = None, token = None, listAll = True, pageStart = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    extent = sanitize.validBounds('extent', extent, True)
    propertyFilter = sanitize.validObject('propertyFilter', propertyFilter, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False) 
    
    body = {'pageStart': pageStart, 'propertyFilter':propertyFilter, 'extent':extent}

    def f(body):
        return apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/featuresByExtent' , body, token)
        
    r = recurse(f, body, listAll, 'features')

    sh = gpd.GeoDataFrame.from_features(r['result']['features'])
    r['result'] = sh
    return r


def listFeatures(pathId, timestampId, token = None, listAll = True, pageStart = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False) 

    body = {'pageStart': pageStart}

    def f(body):
        return apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/listFeatures' , body, token)

    r = recurse(f, body, listAll, 'features')

    
    sh = gpd.GeoDataFrame.from_features(r['result']['features'])    
    r['result'] = sh

    return r




