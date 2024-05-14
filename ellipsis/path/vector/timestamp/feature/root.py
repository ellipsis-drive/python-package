from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util import chunks
from ellipsis.util import loadingBar
from ellipsis.util.root import stringToDate
from ellipsis.util.root import recurse

import numpy as np
import json
import geopandas as gpd



def add(pathId, timestampId, features, token, showProgress = True, cores = 1):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)
    cores = sanitize.validInt('cores', cores, True)
    features = sanitize.validGeopandas('features', features, True, cores = cores)

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


        featuresBody = [{'feature': features_sub[i] } for i in np.arange(len(indices_sub))]
        body = {"features":featuresBody}
        r = apiManager.post('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature', body, token)
        addedIds = addedIds + r
        if showProgress:
            loadingBar(i*3000 + len(indices_sub),features.shape[0])
        i = i+1

    return(addedIds)



def edit(pathId, timestampId, featureIds, token, features, showProgress = True, cores = 1):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, True)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)
    cores = sanitize.validInt('cores', cores, True)
    features = sanitize.validGeopandas('features', features, False, cores=cores)



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


        changes = [{'featureId':x[0] , 'newProperties':x[1]['properties'], 'newGeometry':x[1]['geometry']} for x in zip(featureIds_sub, features_sub['features'])]

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


