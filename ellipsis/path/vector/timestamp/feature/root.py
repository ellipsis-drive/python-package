from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util import chunks
from ellipsis.util import loadingBar
from ellipsis.util.root import stringToDate
from ellipsis.util.root import recurse

import numpy as np
import json
import geopandas as gpd


def manageLevels(levelOfDetail1, levelOfDetail2, levelOfDetail3, levelOfDetail4, levelOfDetail5, features):
    levelOfDetail1 = sanitize.validGeoSeries('levelOfDetail1', levelOfDetail1, False)
    levelOfDetail2 = sanitize.validGeoSeries('levelOfDetail2', levelOfDetail2, False)
    levelOfDetail3 = sanitize.validGeoSeries('levelOfDetail3', levelOfDetail3, False)
    levelOfDetail4 = sanitize.validGeoSeries('levelOfDetail4', levelOfDetail4, False)
    levelOfDetail5 = sanitize.validGeoSeries('levelOfDetail5', levelOfDetail5, False)

    if type(levelOfDetail1) != type(None) and len(levelOfDetail1) != features.shape[0]:
        raise ValueError('levelsOfDetail1 must have same length as number of rows in features')
    if type(levelOfDetail2) != type(None) and len(levelOfDetail2) != features.shape[0]:
        raise ValueError('levelsOfDetail2 must have same length as number of rows in features')
    if type(levelOfDetail3) != type(None) and len(levelOfDetail3) != features.shape[0]:
        raise ValueError('levelsOfDetail3 must have same length as number of rows in features')
    if type(levelOfDetail4) != type(None) and len(levelOfDetail4) != features.shape[0]:
        raise ValueError('levelsOfDetail4 must have same length as number of rows in features')
    if type(levelOfDetail5) != type(None) and len(levelOfDetail5) != features.shape[0]:
        raise ValueError('levelsOfDetail5 must have same length as number of rows in features')

    if type(levelOfDetail2) != type(None) and type(levelOfDetail1) == type(None):
        raise ValueError('If levelOfDetail2 is defined so should levelOfDetail1')
    if type(levelOfDetail3) != type(None) and type(levelOfDetail2) == type(None):
        raise ValueError('If levelOfDetail3 is defined so should levelOfDetail2')
    if type(levelOfDetail4) != type(None) and type(levelOfDetail3) == type(None):
        raise ValueError('If levelOfDetail4 is defined so should levelOfDetail3')
    if type(levelOfDetail5) != type(None) and type(levelOfDetail4) == type(None):
        raise ValueError('If levelOfDetail5 is defined so should levelOfDetail4')


    if type(levelOfDetail1) != type(None):
        levelOfDetail1 = levelOfDetail1.to_json()
        levelOfDetail1 = json.loads(levelOfDetail1)
        levelOfDetail1 = np.array( [ x['geometry'] for x in levelOfDetail1['features'] ])
    if type(levelOfDetail2) != type(None):
        levelOfDetail2 = levelOfDetail2.to_json()
        levelOfDetail2 = json.loads(levelOfDetail2)
        levelOfDetail2 = np.array( [ x['geometry'] for x in levelOfDetail2['features'] ])
    if type(levelOfDetail3) != type(None):
        levelOfDetail3 = levelOfDetail3.to_json()
        levelOfDetail3 = json.loads(levelOfDetail3)
        levelOfDetail3 = np.array( [ x['geometry'] for x in levelOfDetail3['features'] ])
    if type(levelOfDetail4) != type(None):
        levelOfDetail4 = levelOfDetail4.to_json()
        levelOfDetail4 = json.loads(levelOfDetail4)
        levelOfDetail4 = np.array( [ x['geometry'] for x in levelOfDetail4['features'] ])
    if type(levelOfDetail5) != type(None):
        levelOfDetail5 = levelOfDetail5.to_json()
        levelOfDetail5 = json.loads(levelOfDetail5)
        levelOfDetail5 = np.array( [ x['geometry'] for x in levelOfDetail5['features'] ])
        
    return levelOfDetail1, levelOfDetail2, levelOfDetail3, levelOfDetail4, levelOfDetail5

def zipLevels(levelOfDetail1, levelOfDetail2, levelOfDetail3, levelOfDetail4, levelOfDetail5, indices_sub):
    if type(levelOfDetail5) != type(None):         
        levels = list(zip(levelOfDetail1[indices_sub], levelOfDetail2[indices_sub], levelOfDetail3[indices_sub], levelOfDetail4[indices_sub], levelOfDetail5[indices_sub]))
    elif type(levelOfDetail4) != type(None):         
        levels = list(zip(levelOfDetail1[indices_sub], levelOfDetail2[indices_sub], levelOfDetail3[indices_sub], levelOfDetail4[indices_sub]))
    elif type(levelOfDetail3) != type(None):         
        levels = list(zip(levelOfDetail1[indices_sub], levelOfDetail2[indices_sub], levelOfDetail3[indices_sub]))
    elif type(levelOfDetail2) != type(None):         
        levels = list(zip(levelOfDetail1[indices_sub], levelOfDetail2[indices_sub]))                      
    elif type(levelOfDetail1) != type(None):         
        levels = list(zip(levelOfDetail1[indices_sub]))
    else:
        levels = None
    return levels
    
def add(pathId, timestampId, features, token, showProgress = True, levelOfDetail1 = None, levelOfDetail2 = None, levelOfDetail3 = None, levelOfDetail4 = None, levelOfDetail5 = None, cores = 1):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)
    cores = sanitize.validInt('cores', cores, True)
    features = sanitize.validGeopandas('features', features, True, cores = cores)

    levelOfDetail1, levelOfDetail2, levelOfDetail3, levelOfDetail4, levelOfDetail5 = manageLevels(levelOfDetail1, levelOfDetail2, levelOfDetail3, levelOfDetail4, levelOfDetail5, features)
    features_json = features.to_json(na='drop')
    features_json = json.loads(features_json)
    features_json = np.array(features_json['features'])
    
    #check if first time
    firstTime = apiManager.get('/path/' + pathId, None, token)
    if not 'vector' in firstTime.keys():
        raise ValueError('Can only add features if path is of type vector')
    firstTime = len(firstTime['vector']['properties']) ==0
    
    if firstTime:
        print('no properties known for this timestamp adding them automatically')
        columns = features.columns
        columns = [c for c in columns if c != 'geometry']
        for c in columns:
            if 'int' in str(features.dtypes[c]) or 'Int' in str(features.dtypes[c]):
                propertyType = 'integer'
            elif 'float' in str(features.dtypes[c]) or 'Float' in str(features.dtypes[c]):
                propertyType = 'float'
            elif 'bool' in str(features.dtypes[c]):
                propertyType = 'boolean'
            elif 'datetime' in str(features.dtypes[c]):
                propertyType = 'datetime'
            else:
                propertyType = 'string'


            ###date
            body = {'name': c , 'type': propertyType , 'required': False, 'private': False}
            apiManager.post('/path/' + pathId + '/vector/property', body, token)
    indices = chunks(np.arange(features.shape[0]))


    addedIds = []
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        features_sub = features_json[indices_sub]

        levels = zipLevels(levelOfDetail1, levelOfDetail2, levelOfDetail3, levelOfDetail4, levelOfDetail5, indices_sub)
                      
        if type(levels) != type(None):
            featuresBody = [{'feature': features_sub[i], 'levelsOfDetail': levels[i] } for i in np.arange(len(indices_sub))]
        else:
            featuresBody = [{'feature': features_sub[i] } for i in np.arange(len(indices_sub))]
        body = {"features":featuresBody}
        r = apiManager.post('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature', body, token)
        addedIds = addedIds + r
        if showProgress:
            loadingBar(i*3000 + len(indices_sub),features.shape[0])
        i = i+1
        
    return(addedIds)


    
def edit(pathId, timestampId, featureIds, token, features = None, showProgress = True, levelOfDetail1 = None, levelOfDetail2 = None, levelOfDetail3 = None, levelOfDetail4 = None, levelOfDetail5 = None, cores = 1):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, True)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)
    cores = sanitize.validInt('cores', cores, True)
    features = sanitize.validGeopandas('features', features, False, cores=cores)

    levelOfDetail1, levelOfDetail2, levelOfDetail3, levelOfDetail4, levelOfDetail5 = manageLevels(levelOfDetail1, levelOfDetail2, levelOfDetail3, levelOfDetail4, levelOfDetail5, features)


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

        levels = zipLevels(levelOfDetail1, levelOfDetail2, levelOfDetail3, levelOfDetail4, levelOfDetail5, indices_sub)

        if type(levels) == type(None):
                changes = [{'featureId':x[0] , 'newProperties':x[1]['properties'], 'newGeometry':x[1]['geometry']} for x in zip(featureIds_sub, features_sub['features'])]
        else:
                changes = [{'featureId':x[0], 'levelsOfDetail': levels , 'newProperties':x[1]['properties'], 'newGeometry':x[1]['geometry']} for x in zip(featureIds_sub, features_sub['features'])]
            
        body = {'changes':changes}
        r = apiManager.patch('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature', body, token)

        if len(indices) > 1 and showProgress:
            loadingBar(i*1000 + len(indices_sub),len(featureIds))

    return r


def trash(pathId, timestampId, featureIds, token, showProgress = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, True)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)

    indices = chunks(np.arange(len(featureIds)),1000)
    i=0
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        featureIds_sub = list(np.array(featureIds)[indices_sub])

        body = {'featureIds': featureIds_sub, 'trashed': True}
        r = apiManager.put('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/trashed', body, token)

        if len(indices) > 1 and showProgress:
            loadingBar(i*1000 + len(indices_sub),len(featureIds))

    return r


def recover(pathId, timestampId, featureIds, token, showProgress = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, True)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)

    indices = chunks(np.arange(len(featureIds)),1000)
    i=0
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        featureIds_sub = list(np.array(featureIds)[indices_sub])

        body = {'featureIds': featureIds_sub, 'trashed': False}
        r = apiManager.put('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/trashed', body, token)

        if len(indices) > 1 and showProgress:
            loadingBar(i*1000 + len(indices_sub),len(featureIds))

    return r



def versions(pathId, timestampId, featureId, token = None, pageStart = None, listAll = True):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    featureId = sanitize.validUuid('featureId', featureId, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    
    body = {'returnType':'all'}
    def f(body):
        return apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/' + featureId + '/version', body, token)

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


