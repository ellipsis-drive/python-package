from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util import chunks
from ellipsis.util import loadingBar
from ellipsis.util.root import stringToDate
from ellipsis.util.root import recurse

import numpy as np
import json
import geopandas as gpd


def add(pathId, layerId, features, token, zoomlevels = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    features = sanitize.validGeopandas('features', features, True)
    zoomlevels = sanitize.validIntArray('zoomlevels', zoomlevels, False)
        
    
    #check if first time
    firstTime = apiManager.get('/path/' + pathId, None, token)
    firstTime = [x for x in firstTime['vector']['layers'] if x['id'] == layerId]
    if len(firstTime)==0:
        raise ValueError('layer does not exist')
    firstTime = len(firstTime[0]['properties']) ==0
    
    if firstTime:
        print('no properties known for this layer adding them automatically')
        columns = features.columns
        columns = [c for c in columns if c != 'geometry']
        for c in columns:
            if 'int' in str(features.dtypes[c]) or 'Int' in str(features.dtypes[c]):
                propertyType = 'integer'
                features[c] = [ int(d) if not np.isnan(d) and d != None else  np.nan for d in features[c].values ]
            elif 'float' in str(features.dtypes[c]) or 'Float' in str(features.dtypes[c]):
                propertyType = 'float'
                features[c] = [ float(d) if not np.isnan(d) and d != None else  np.nan for d in features[c].values ]
            elif 'bool' in str(features.dtypes[c]):
                propertyType = 'boolean'
                features[c] = [ bool(d) if not np.isnan(d) and d != None else  np.nan for d in features[c].values ]
            elif 'datetime' in str(features.dtypes[c]):
                propertyType = 'datetime'
                features[c] = [ d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for d in features[c].values ]
            else:
                propertyType = 'string'
                features[c] = [ str(d) if d != None else  np.nan for d in features[c].values ]


            ###date
            body = {'name': c , 'type': propertyType , 'required': False, 'private': False}
            apiManager.post('/path/' + pathId + '/vector/layer/' + layerId + '/property', body, token)                
    indices = chunks(np.arange(features.shape[0]))


    addedIds = []
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        features_sub = features.iloc[indices_sub]
        features_sub =features_sub.to_json(na='drop')
        features_sub = json.loads(features_sub)
        
        body = {"features":features_sub['features'], 'zoomlevels':zoomlevels}

        r = apiManager.post('/path/' + pathId + '/vector/layer/' + layerId + '/feature', body, token)

        addedIds = addedIds + r

        loadingBar(i*3000 + len(indices_sub),features.shape[0])
        i = i+1
        
    return(addedIds)


    
def edit(pathId, layerId, featureIds, token, zoomlevels = None, features = None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    features = sanitize.validGeopandas('features', features, False)
    zoomlevels = sanitize.validIntArray('zoomlevels', zoomlevels, False)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)


    if type(features) != type(None) and features.shape[0] != len(featureIds):
        raise ValueError('featureIds must be of same length as the features geopandas dataframe')
        

    indices = chunks(np.arange(len(featureIds)),1000)
    i=0
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        featureIds_sub = list( np.array(featureIds)[indices_sub])

        if type(features) != type(None):
            features_sub = features.iloc[indices_sub]        
            features_sub =features_sub.to_json(na='drop')
            features_sub = json.loads(features_sub)

        if str(type(zoomlevels)) != str(type(None)) and str(type(features)) != str(type(None)):
            changes = [{'featureId':x[0] , 'newProperties':x[1]['properties'], 'newGeometry':x[1]['geometry'], 'newZoomlevels':zoomlevels} for x in zip(featureIds_sub, features_sub['features'])]
        elif str(type(zoomlevels)) != str(type(None)) and str(type(features)) == str(type(None)):
            changes = [{'featureId':geometryId, 'newZoomlevels':zoomlevels} for geometryId in featureIds]
        else:
            changes = [{'featureId':x[0] , 'newProperties':x[1]['properties'], 'newGeometry':x[1]['geometry']} for x in zip(featureIds_sub, features_sub['features'])]
            
        body = {'changes':changes}
        r = apiManager.patch('/path/' + pathId + '/vector/layer/' + layerId + '/feature', body, token)

        if len(indices) > 1:
            loadingBar(i*1000 + len(indices_sub),len(featureIds))

    return r


def delete(pathId, layerId, featureIds, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)

    indices = chunks(np.arange(len(featureIds)),1000)
    i=0
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        featureIds_sub = list(np.array(featureIds)[indices_sub])

        body = {'featureIds': featureIds_sub, 'deleted': True}
        r = apiManager.put('/path/' + pathId + '/vector/layer/' + layerId + '/feature/deleted', body, token)

        if len(indices) > 1:
            loadingBar(i*1000 + len(indices_sub),len(featureIds))

    return r


def recover(pathId, layerId, featureIds, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, True)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)

    indices = chunks(np.arange(len(featureIds)),1000)
    i=0
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        featureIds_sub = list(np.array(featureIds)[indices_sub])

        body = {'featureIds': featureIds_sub, 'deleted': False}
        r = apiManager.put('/path/' + pathId + '/vector/layer/' + layerId + '/feature/deleted', body, token)

        if len(indices) > 1:
            loadingBar(i*1000 + len(indices_sub),len(featureIds))

    return r



def versions(pathId, layerId, featureId, token = None, pageStart = None, listAll = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    token = sanitize.validString('token', token, False)
    featureId = sanitize.validUuid('featureId', featureId, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    
    body = {'returnType':'all'}
    def f(body):
        return apiManager.get('/path/' + pathId + '/vector/layer/' + layerId + '/feature/' + featureId + '/version', body, token)

    r = recurse(f, body, listAll)

    features = [ x['feature'] for x in r['result']]
    dates = [stringToDate(x['date']) for x in r['result'] ]
    usernames = [x['user']['username'] for x in r['result'] ]
    userIds = [x['user']['id'] for x in r['result'] ]

    sh = gpd.GeoDataFrame.from_features(features)     
    sh['username'] = usernames
    sh['userId'] = userIds
    sh['dates'] = dates
    
    sh.crs = {'init': 'epsg:4326'}
    r['result'] = sh
    return(r)


