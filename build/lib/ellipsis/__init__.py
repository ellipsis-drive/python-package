#python3 setup.py sdist bdist_wheel
#twine upload --repository pypi dist/*

import pandas as pd
from PIL import Image
import geopandas as gpd
from pyproj import Proj, transform
import base64
import numpy as np
from io import BytesIO
import time
import requests
import rasterio
from datetime import datetime
import math
import tifffile
from shapely.geometry import Polygon
from rasterio.features import rasterize
from geopy.distance import geodesic
import json
#import cv2
import sys
import os
from rasterio.io import MemoryFile
from requests_toolbelt import MultipartEncoder
import warnings
import threading

__version__ = '1.2.14'
url = 'https://api.ellipsis-drive.com/v1'

s = requests.Session()
warnings.filterwarnings("ignore")


def logIn(username, password):
        r =s.post(url + '/account/login/',
                         json = {'username':username, 'password':password} )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        token = r.json()
        token = token['token']
        token = 'Bearer ' + token
        return(token)

def metadata(projectId, includeDeleted=False, token = None):
    mapId = projectId
    if token == None:
        r = s.post(url + '/metadata',
                         json = {"mapId":  mapId})
    else:
        r = s.post(url + '/metadata', headers = {"Authorization":token},
                         json = {"mapId":  mapId, 'includeDeleted':includeDeleted})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r)


def getShapes(name= None, fuzzyMatch = False, favorite = None, access = ['subscribed', 'public', 'owned'], bounds=None, userId= None, hashtag = None, limit = 100, token = None):
    
    body = {'access': access}
    if str(type(name)) != str(type(None)):
        body['name'] = name
        
    body['nameFuzzy'] = True
    
    if str(type(favorite)) != str(type(None)):
        body['favorite'] = name
    
    if str(type(userId)) != str(type(None)):
        body['userId'] = userId
    if str(type(hashtag)) != str(type(None)):
        body['hashtag'] = hashtag
        
    if str(type(bounds)) != str(type(None)):
        bounds = {'xMin':float(bounds['xMin']), 'xMax':float(bounds['xMax']), 'yMin':float(bounds['yMin']), 'yMax':float(bounds['yMax'])}
        body['bounds'] = bounds
        
    keepGoing = True
    results = []
    while keepGoing:    
        if token == None:
            r = s.post(url + '/account/shapes', json = body )
        else:
            r = s.post(url + '/account/shapes', json = body, 
                         headers = {"Authorization":token} )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        result = r.json()
        body['pageStart'] = result['nextPageStart']
        result = result['result']
        if len(result) < 100:
            keepGoing = False
        results = results + result
        if len(result) >= limit:
            keepGoing = False
    end = min(limit, len(result))
    result = result[0:end]
    return(results)
    

def getMaps(name= None, fuzzyMatch = False, access = ['subscribed', 'public', 'owned'], bounds = None, userId= None, favorite = None, resolutionRange=None, dateRange=None, hashtag = None, limit = 100, token = None):

    body = {'access': access}
    if str(type(name)) != str(type(None)):
        body['name'] = name
    body['nameFuzzy'] = fuzzyMatch        
    if str(type(favorite)) != str(type(None)):
        body['favorite'] = favorite
    if str(type(userId)) != str(type(None)):
        body['userId'] = userId
    if str(type(dateRange)) != str(type(None)):
        body['dateFrom'] = dateRange['dateFrom'].strftime('%Y-%m-%d %H:%M:%S')
        body['dateTo'] = dateRange['dateTo'].strftime('%Y-%m-%d %H:%M:%S')
    if str(type(resolutionRange)) != str(type(None)):
        body['resolution'] = resolutionRange
    if str(type(hashtag)) != str(type(None)):
        body['hashtag'] = hashtag
    if str(type(bounds)) != str(type(None)):
        bounds = {'xMin':float(bounds['xMin']), 'xMax':float(bounds['xMax']), 'yMin':float(bounds['yMin']), 'yMax':float(bounds['yMax'])}
        body['bounds'] = bounds

    
    keepGoing = True
    results = []
    while keepGoing:    
        if token == None:
            r = s.post(url + '/account/maps', json = body )
        else:
            r = s.post(url + '/account/maps', json = body, 
                         headers = {"Authorization":token} )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        result = r.json()
        body['pageStart'] = result['nextPageStart']

        results = results + result['result']
        result = result['result']
        if len(result) < 100:
            keepGoing = False
        results = results + result
        if len(result) >= limit:
            keepGoing = False

    end = min(limit, len(result))
    result = result[0:end]
    return(results)
    
        

def getBounds(projectId, timestamp = None, token = None ):
    body = {"mapId": projectId}

    if str(type(timestamp)) != str(type(None)):
        body['timestamp'] = timestamp
    else:
        body['timestamp'] = 0
        
    if token == None:
        r = s.post(url + '/settings/projects/bounds',
                         json = body)
    else:
        r = s.post(url + '/settings/projects/bounds', headers = {"Authorization":token},
                         json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    r = r.json()
    r['id'] = 0
    r['properties'] = {}
    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union
    return(r)
        
def geometryIds(shapeId, layerId, geometryIds, wait = 0, token = None):
    body = {"mapId":  shapeId, 'layerId':layerId, 'returnType':'all'}
    ids_chunks = chunks( list(geometryIds))
    sh = gpd.GeoDataFrame()

    for chunk_ids in ids_chunks:
        body['geometryIds'] = list(chunk_ids)

        if token == None:
            r = s.post(url + '/geometry/bounds',
                             json = body, timeout=10)
        else:
            r = s.post(url + '/geometry/get', headers = {"Authorization":token},
                             json = body, timeout=10)
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)

        r = r.json()
        sh  = sh.append(gpd.GeoDataFrame.from_features(r['result']['features']))
        time.sleep(wait)

    return(sh)
    
def geometryGet(shapeId, layerId, filters = None, limit = None, wait = 0, token = None):
    body = {"mapId":  shapeId, 'layerId':layerId}
    if str(type(filters)) != str(type(None)):
        try:
            for i in np.arange(len(filters)):
                if 'float' in str(type(filters[i]['key'])):
                    filters[i]['value'] = float(filters[i]['value'])
                if 'bool' in str(type(filters[i]['key'])):
                    filters[i]['value'] = bool(filters[i]['value'])
                if 'int' in str(type(filters[i]['key'])):
                    filters[i]['value'] = int(filters[i]['value'])
                if filters[i]['key'] == 'creationDate':
                    filters[i]['value'] = filters[i]['value'].strftime('%Y-%m-%d %H:%M:%S') 
            body['propertyFilter'] = filters
        except:
            raise ValueError('filters must be an array with dictionaries. Each dictionary should have a property, key, operator and value')

    body = json.dumps(body)
    print(body)

    body = json.loads(body)

    body['returnType'] = 'all'
    keepGoing = True
    sh = gpd.GeoDataFrame()
    while (keepGoing):
        if str(type(limit)) != str(type(None)):
            limit = min(3000, limit - sh.shape[0])
            body['pageSize'] = limit
        if token == None:
            r = s.post(url + '/geometry/get',
                             json = body, timeout=10)
        else:
            r = s.post(url + '/geometry/get', headers = {"Authorization":token},
                             json = body, timeout=10)
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r = r.json()
        if len(r['result']['features']) < 3000 and not r['truncated']:
            keepGoing = False

        sh  = sh.append(gpd.GeoDataFrame.from_features(r['result']['features']))
        body['pageStart'] = r['nextPageStart']
        time.sleep(wait)
            
        if sh.shape[0]>0:
            loadingBar(sh.shape[0],sh.shape[0])
            
    sh.crs = {'init': 'epsg:4326'}

    return(sh)
    
        
def geometryBounds(shapeId, layerId, xMin = None, xMax = None, yMin=None, yMax=None, filters=None, wait = 0, limit = None, token = None):
    mapId = shapeId
    
    body = {"mapId":  mapId, 'layerId':layerId}
    if str(type(xMin)) == str(type(None)):
        xMin = -180
    if str(type(xMax)) == str(type(None)):
        xMax = 180
    if str(type(yMin)) == str(type(None)):
        yMin = -85
    if str(type(yMax)) == str(type(None)):
        yMax = 85
        
    body['bounds'] = {'xMin': float(xMin) , 'xMax':float(xMax), 'yMin':float(yMin), 'yMax':float(yMax)}

    if str(type(filters)) != str(type(None)):
        try:
            for i in np.arange(len(filters)):
                if 'float' in str(type(filters[i]['key'])):
                    filters[i]['value'] = float(filters[i]['value'])
                if 'bool' in str(type(filters[i]['key'])):
                    filters[i]['value'] = bool(filters[i]['value'])
                if 'int' in str(type(filters[i]['key'])):
                    filters[i]['value'] = int(filters[i]['value'])
                if filters[i]['key'] == 'creationDate':
                    filters[i]['value'] = filters[i]['value'].strftime('%Y-%m-%d %H:%M:%S') 
            body['propertyFilter'] = filters
        except:
            raise ValueError('filters must be an array with dictionaries. Each dictionary should have a property, key, operator and value')


    body = json.dumps(body)
    body = json.loads(body)

    body['returnType'] = 'all'
    keepGoing = True
    sh = gpd.GeoDataFrame()

    while (keepGoing):
        if str(type(limit)) != str(type(None)):
            limit = min(3000, limit - sh.shape[0])
            body['pageSize'] = limit
        if token == None:
            r = s.post(url + '/geometry/bounds',
                             json = body, timeout=10)
        else:
            r = s.post(url + '/geometry/bounds', headers = {"Authorization":token},
                             json = body, timeout=10)
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r = r.json()
        if len(r['result']['features']) < 3000 and not r['truncated']:
            keepGoing = False

        sh  = sh.append(gpd.GeoDataFrame.from_features(r['result']['features']))
        body['pageStart'] = r['nextPageStart']
        time.sleep(wait)
            
        if sh.shape[0]>0:
            loadingBar(sh.shape[0],sh.shape[0])
            
    sh.crs = {'init': 'epsg:4326'}

    return(sh)


        

def geometryVersions(shapeId, layerId, geometryId, token = None):
    mapId = shapeId
    body = {"mapId":  mapId, "layerId":layerId, 'geometryId':geometryId, 'returnType':'all'}
    if token == None:
        r = s.post(url + '/geometry/versions',
                         json = body)    
    else:
        r = s.post(url + '/geometry/versions', headers = {"Authorization":token},
                         json = body)    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    r  = r.json()['result']

    sh = gpd.GeoDataFrame()
    for v in r:
        sh_sub = gpd.GeoDataFrame({'geometry':[v['feature']]})
        sh_sub['editUser'] = v['editUser']
        sh_sub['editDate'] = v['editDate']
        sh = sh.append(sh_sub)

    sh.crs = {'init': 'epsg:4326'}
    return(sh)

    


def geometryDelete(shapeId, layerId, geometryIds, token, revert= False):

    body = {"mapId":  shapeId, "layerId":layerId , 'geometryIds': list(geometryIds), 'rever':revert}

    r= s.post(url + '/geometry/delete', headers = {"Authorization":token},
                     json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def geometryEdit(shapeId, layerId, geometryIds, features, token, zoomlevels = None):
    features = features.copy()
    if 'id' in features.columns:
        del features['id']
    if 'userId' in features.columns:
        del features['userId']
    if 'attribution' in features.columns:
        del features['attribution']

    if str(type(zoomlevels)) != str(type(None)):
        zoomlevels = [int(z) for z in zoomlevels]


    mapId = shapeId
    if not str(type(features)) ==  "<class 'geopandas.geodataframe.GeoDataFrame'>":
        raise ValueError('features must be of type geopandas dataframe')
        
    features = features.to_crs({'init': 'epsg:4326'})
    
    indices = chunks(np.arange(features.shape[0]),1000)
    i=0    
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        features_sub = features.iloc[indices_sub]
        geometryIds_sub = geometryIds[indices_sub]
        
        features_sub =features_sub.to_json(na='drop')
        features_sub = json.loads(features_sub)

        if str(type(zoomlevels)) != str(type(None)):
            changes = [{'geometryId':x[0] , 'newProperties':x[1]['properties'], 'newGeometry':x[1]['geometry'], 'newZoomlevels':zoomlevels} for x in zip(geometryIds_sub, features_sub['features'])]
        else:
            changes = [{'geometryId':x[0] , 'newProperties':x[1]['properties'], 'newGeometry':x[1]['geometry']} for x in zip(geometryIds_sub, features_sub['features'])]
            
            
        body = {"mapId":  mapId, "layerId":layerId, 'changes':changes}
        retried = 0
        while retried <= 20:
            try:
                r = s.post(url + '/geometry/edit', headers = {"Authorization":token},
                             json = body )
                retried = 21
            except Exception as e:
                if retried == 20:
                    raise ValueError(e)
                retried = retried +1
                time.sleep(1)

        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)


        loadingBar(i*1000 + len(indices_sub),features.shape[0])


def geometryChangelog(shapeId, layerId, limit = 100, userId = None, pageStart = None, actions = ['add', 'delete', 'recover', 'move'], token = None):
    changes = []
    keepGoing = True
    
    while keepGoing:
        pageSize = min(100, limit - len(changes))
        body = {'mapId':shapeId, 'layerId':layerId, 'pageSize':pageSize, 'actions':list(actions)}
        if str(type(userId)) != str(type(None)):
            body['userId'] = userId
        if str(type(pageStart)) != str(type(None)):
            body['pageStart'] = pageStart
    
        if token ==None:
            r = s.post(url + '/geometry/changeLog',
                         json = body )        
        else:
            r = s.post(url + '/geometry/changeLog', headers = {"Authorization":token},
                         json = body )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        r = r.json()
        pageStart = r['nextPageStart']
        r = r['result']
        changes = changes + r
        if len(changes) >= limit or str(type(pageStart)) == str(type(None)):
            break
    return({'changes':changes, 'pageStart':pageStart})
  
    
def geometryAdd(shapeId, layerId, features, token, zoomlevels=None):
    mapId = shapeId
    if not str(type(features)) ==  "<class 'geopandas.geodataframe.GeoDataFrame'>":
        raise ValueError('features must be of type geopandas dataframe')

    if str(type(features.crs)) == str(type(None)) and min(features.bounds['minx']) > -180  and max(features.bounds['maxx']) < 180 and min(features.bounds['miny']) > -90  and max(features.bounds['maxy']) < 90:
        print('assuming WGS84 coordinates')
    elif str(type(features.crs)) == str(type(None)):
        raise ValueError('Please provide CRS for the geopandas dataframe or translate to WGS84 coordinates')
    else:
        features = features.to_crs({'init': 'epsg:4326'})

    if str(type(None)) != str(type(zoomlevels)):
        zoomlevels = [int(z) for z in zoomlevels]
    
    firstTime = metadata(projectId = mapId, token = token)['geometryLayers']
    firstTime = [x for x in firstTime if x['id'] == layerId]
    if len(firstTime)==0:
        raise ValueError('layer does not exist')
    firstTime = len(firstTime[0]['properties']) ==0
    
    if firstTime:
        print('no properties known for this layer adding them automatically')
        columns = features.columns
        columns = [c for c in columns if c != 'geometry']
        for c in columns:
            if 'int' in str(features.dtypes[c]):
                propertyType = 'integer'
                features[c] = [ int(d) if not np.isnan(d) and d != None else  np.nan for d in features[c].values ]
            elif 'float' in str(features.dtypes[c]):
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
                
            addProperty(shapeId = mapId, layerId =layerId, propertyName = c, propertyType = propertyType, token = token)


    indices = chunks(np.arange(features.shape[0]))

    #add properties manually
    addedIds = []
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        features_sub = features.iloc[indices_sub]
        features_sub =features_sub.to_json(na='drop')
        features_sub = json.loads(features_sub)
        #float to int
        
        
        body = {"mapId":  mapId, "layerId":layerId, "features":features_sub['features']}

        if str(type(None)) != str(type(zoomlevels)):
            body['zoomLevels'] = zoomlevels

        retried = 0
        while retried <= 20:
            try:
                r = s.post(url + '/geometry/add', headers = {"Authorization":token},
                             json = body )
                retried = 21
            except Exception as e:
                if retried == 20:
                    raise ValueError(e)
                retried = retried +1
                time.sleep(1)

        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)

        addedIds = addedIds + r.json()

        loadingBar(i*3000 + len(indices_sub),features.shape[0])
        i = i+1
        
    return(addedIds)

        
    
def messageGet(shapeId, layerId, userId= None, messageIds =None, geometryIds=None, limit = None, deleted=False, token = None):

    body={'mapId':shapeId, 'layerId':layerId, 'deleted':deleted, 'returnType':'all'}

    if str(type(userId)) != str(type(None)):
        body['userId']=userId
    if str(type(geometryIds)) != str(type(None)):
        body['geometryIds']= list(geometryIds)
    
    keepGoing = True
    messages = []
    while(keepGoing):
        if str(type(limit)) == str(type(None)):
            body['pageSize'] = 100
        else:
            body['pageSize'] = min(100, limit - len(messages))

        if token == None:
            r = s.post(url + '/message/get',
                         json = body )        
        else:
            r = s.post(url + '/message/get', headers = {"Authorization":token},
                         json = body )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r =  r.json()

        body['pageStart']=r['nextPageStart']

        messages = messages +  r['result']
        if str(type(limit)) == str(type(None)):
            keepGoing = str(type(r['nextPageStart'])) != str(type(None))
        else:
            keepGoing = len(messages) < limit or str(type(r['nextPageStart'])) != str(type(None))
        loadingBar(len(messages), len(messages))
    
    return(messages)
    
def messageAdd(shapeId, layerId, geometryId, token, replyTo = None, message = None, private= None, image=None, lon=None, lat=None): 
    mapId = shapeId    
    body = {'mapId':mapId, 'layerId':layerId, 'geometryId':geometryId}
    if str(type(lon)) != "<class 'NoneType'>":
        lon = float(lon)
    if str(type(lat)) != "<class 'NoneType'>":
        lat = float(lat)
    if str(type(replyTo)) != "<class 'NoneType'>":
        body['replyTo'] = replyTo
    if str(type(message)) != "<class 'NoneType'>":
        body['text'] = message
    if str(type(private)) != "<class 'NoneType'>":
        body['private'] = private
    if str(type(image)) != "<class 'NoneType'>":
        image = Image.fromarray(image.astype('uint8'))
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = str(base64.b64encode(buffered.getvalue()))
        img_str = 'data:image/jpeg;base64,' + img_str[2:-1]
        body['image'] = img_str
    if str(type(lon)) != "<class 'NoneType'>":
        body['x'] = lon
    if str(type(lat)) != "<class 'NoneType'>":
        body['y'] = lat
        
    r = s.post(url + '/message/add', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    messageId = r.json()['id']


    return({'id':messageId})

def messageDelete(shapeId, layerId, messageId, token):    
    mapId = shapeId
    body = {'mapId':mapId, 'layerId':layerId, 'messageId':messageId}
    r = s.post(url + '/message/delete', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    


def messageImage(shapeId, layerId, messageId, token = None):
    mapId = shapeId
    body = {'mapId':mapId, 'layerId':layerId, 'messageId':messageId}
    if token ==None:
        r = s.post(url + '/message/image',
                     json = body )        
    else:
        r = s.post(url + '/message/image', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    try:
        im = Image.open(BytesIO(r.content))
    except:
           raise ValueError('No image or invalid image in geoMessage')
 
    return(im)



def rasterAggregated(mapId, timestamps, geometry, approximate = True, token = None):
    sh = gpd.GeoDataFrame({'geometry':[geometry]})
    geometry =sh.to_json(na='drop')
    geometry = json.loads(geometry)
    geometry = geometry['features'][0]['geometry']
    timestamps = list(timestamps)
    body = {'mapId':mapId, 'timestamps':timestamps, 'geometry':geometry, 'approximate':approximate}
    if token ==None:
        r = s.post(url +  '/raster/aggregated',
                     json = body )        
    else:
        r = s.post(url +  '/raster/aggregated', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    return(r.json())


def rasterRaw(mapId, timestamp, xMin= None,xMax= None,yMin=None, yMax=None, zoom = None, num_bands = None, bounds=None, downsample = False, width = None, height = None, threads = 1, token = None):
    dtype = 'float32'
    
    if str(type(bounds)) != str(type(None)):
      xMin,yMin,xMax,yMax = bounds.bounds  
    elif str(type(xMin)) == "<class 'NoneType'>" or str(type(xMax)) == "<class 'NoneType'>" or str(type(yMin)) == "<class 'NoneType'>" or str(type(yMax)) == "<class 'NoneType'>" :
            raise ValueError('Either xMin, xMax, yMin and yMax or bounds are required')

    xMin = float(xMin)
    xMax = float(xMax)
    yMin = float(yMin)
    yMax = float(yMax)

    xMinWeb,yMinWeb =  transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMin, yMin)
    xMaxWeb,yMaxWeb = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMax, yMax)

    timestamp = int(timestamp)

    token_inurl = ''
    if str(type(token)) != str(type(None)):
        token_inurl = '?token=' + token.replace('Bearer ', '')

    if downsample:
        if str(type(width)) == str(type(None)) or str(type(height)) == str(type(None)):
            raise ValueError('if downsample is true, width and height are required')


        bbox = {'xMin':xMin, 'xMax':xMax, 'yMin':yMin , 'yMax':yMax}
        body = {'mapId':mapId, 'timestamp' : timestamp, 'mapId':mapId, 'bounds':bbox, 'width':width, 'height':height}
        print(body)
        if str(type(token)) == str(type(None)):
            r = s.post(url + '/raster/raw',
                         json = body )        
        else:
            r = s.post(url + '/raster/raw', headers = {"Authorization":token},
                         json = body )


        if int(str(r).split('[')[1].split(']')[0]) != 200:
                raise ValueError(r.text)
        else:
                r_total = tifffile.imread(BytesIO(r.content))
                r_total = np.transpose(r_total, [2,0,1])

    else:
            if str(type(num_bands)) == str(type(None)):
                bands = metadata(mapId)['bands']
                num_bands = len(bands)


            if str(type(zoom)) == str(type(None)):
                timestamps = metadata(mapId, token = token)['timestamps']
                all_timestamps = [item["timestamp"] for item in timestamps]
                if not timestamp in all_timestamps:
                    raise ValueError('given timestamp does not exist')
                
                zoom = next(item for item in timestamps if item["timestamp"] == timestamp)['zoom']
          
            min_x_osm_precise =  (xMin +180 ) * 2**zoom / 360 
            max_x_osm_precise =   (xMax +180 ) * 2**zoom / 360
            max_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMin/360 * math.pi  ) ) ) 
            min_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMax/360 * math.pi  ) ) )
                        
            min_x_osm =  math.floor(min_x_osm_precise )
            max_x_osm =  math.floor( max_x_osm_precise)
            max_y_osm = math.floor( max_y_osm_precise)
            min_y_osm = math.floor( min_y_osm_precise)
            
            x_tiles = np.arange(min_x_osm, max_x_osm+1)
            y_tiles = np.arange(min_y_osm, max_y_osm +1)
            
            r_total = np.zeros((256*(max_y_osm - min_y_osm + 1) ,256*(max_x_osm - min_x_osm + 1),num_bands), dtype = dtype)
            
            tiles = []            
            for tileY in y_tiles:
                for tileX in x_tiles:
                    tiles = tiles + [(tileX, tileY)]

            def subTiles(tiles):
                    N = 0
                    for tile in tiles:
                        tileX = tile[0]
                        tileY = tile[1]
                        x_index = tileX - min_x_osm
                        y_index = tileY - min_y_osm
                        
                        url_req = url + '/tileService/' + mapId + '/' + str(timestamp) + '/data/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY) + token_inurl
                        r = s.get(url_req , timeout = 10 )
    
    
                        if int(str(r).split('[')[1].split(']')[0]) == 403:
                                raise ValueError('insufficient access')
                        if int(str(r).split('[')[1].split(']')[0]) != 200:
                                r = np.zeros((num_bands,256,256))
                        else:
                            r = tifffile.imread(BytesIO(r.content))
                        r = np.transpose(r, [1,2,0])
                        r_total[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ] = r
                        loadingBar(N, len(tiles))
                        N = N + 1
                    

            size = math.floor(len(tiles)/threads) + 1
            tiles_chunks = chunks(tiles, size)
            prs = []
            for tiles in tiles_chunks:
                pr = threading.Thread(target = subTiles, args =(tiles,), daemon=True)
                pr.start()
                prs = prs + [pr] 
            for pr in prs:
                pr.join()                           
                
            min_x_index = int(round((min_x_osm_precise - min_x_osm)*256))
            max_x_index = max(int(round((max_x_osm_precise- min_x_osm)*256)), min_x_index + 1 )
            min_y_index = int(round((min_y_osm_precise - min_y_osm)*256))
            max_y_index = max(int(round((max_y_osm_precise- min_y_osm)*256)), min_y_index + 1)
            
            r_total = r_total[min_y_index:max_y_index,min_x_index:max_x_index,:]
 

    if str(type(bounds)) != str(type(None)):
        trans = rasterio.transform.from_bounds(xMinWeb, yMinWeb, xMaxWeb, yMaxWeb, r_total.shape[1], r_total.shape[0])
        shape = gpd.GeoDataFrame({'geometry':[bounds]})
        shape.crs = {'init': 'epsg:4326'}
        shape = shape.to_crs({'init': 'epsg:3857'})
        raster_shape = rasterize( shapes = [ (shape['geometry'].values[m], 1) for m in np.arange(shape.shape[0]) ] , fill = 0, transform = trans, out_shape = (r_total.shape[0], r_total.shape[1]), all_touched = True )
        r_total[:,:,-1] = np.minimum(r_total[:,:,-1], raster_shape)


    return(r_total)



def rasterVisual(mapId, timestamp, layerId, xMin= None,xMax= None,yMin=None, yMax=None, bounds=None, downsample = False, width = None, height=None, threads = 1, token = None):

    dtype = 'uint8'

    if str(type(bounds)) != str(type(None)):
      xMin,yMin,xMax,yMax = bounds.bounds  
    elif str(type(xMin)) == "<class 'NoneType'>" or str(type(xMax)) == "<class 'NoneType'>" or str(type(yMin)) == "<class 'NoneType'>" or str(type(yMax)) == "<class 'NoneType'>" :
            raise ValueError('Either xMin, xMax, yMin and yMax or bounds are required')

    xMin = float(xMin)
    xMax = float(xMax)
    yMin = float(yMin)
    yMax = float(yMax)

    xMinWeb,yMinWeb =  transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMin, yMin)
    xMaxWeb,yMaxWeb = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMax, yMax)

    timestamp = int(timestamp)

    token_inurl = ''
    if token != None:
        token_inurl = '?token=' + token.replace('Bearer ', '')

    if downsample:
        if str(type(width)) == str(type(None)) or str(type(height)) == str(type(None)):
            raise ValueError('if downsample is true, width and height are required')

        bbox = {'xMin':xMin, 'xMax':xMax, 'yMin':yMin , 'yMax':yMax}
        body = {'mapId':mapId, 'timestamp' : timestamp,'layerId':layerId, 'mapId':mapId, 'bounds':bbox, 'width':width, 'height':height}

        if str(type(token)) == str(type(None)):
            r = s.post(url + '/raster/bounds',
                         json = body )        
        else:
            r = s.post(url + '/raster/bounds', headers = {"Authorization":token},
                         json = body )

        if int(str(r).split('[')[1].split(']')[0]) != 200:
                raise ValueError(r.text)
        else:
           r_total = np.array(Image.open(BytesIO(r.content)), dtype = 'uint8')
            

    else:

            timestamps = metadata(mapId, token = token)['timestamps']
            zoom = next(item for item in timestamps if item["timestamp"] == timestamp)['zoom']

            
            min_x_osm_precise =  (xMin +180 ) * 2**zoom / 360 
            max_x_osm_precise =   (xMax +180 ) * 2**zoom / 360
            max_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMin/360 * math.pi  ) ) ) 
            min_y_osm_precise = 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + yMax/360 * math.pi  ) ) )
        
            min_x_osm =  math.floor(min_x_osm_precise )
            max_x_osm =  math.floor( max_x_osm_precise)
            max_y_osm = math.floor( max_y_osm_precise)
            min_y_osm = math.floor( min_y_osm_precise)
        
            x_tiles = np.arange(min_x_osm, max_x_osm+1)
            y_tiles = np.arange(min_y_osm, max_y_osm +1)


            tiles = []            
            for tileY in y_tiles:
                for tileX in x_tiles:
                    tiles = tiles + [(tileX,tileY)]
                    
                    
            def subTiles(tiles):
                N=0
                for tile in tiles:
                    tileX = tile[0]
                    tileY = tile[1]
                    
                    x_index = tileX - min_x_osm
                    y_index = tileY - min_y_osm

                    r = s.get(url + '/tileService/' + mapId + '/' + str(timestamp) + '/' + layerId + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY) + token_inurl ,
                                 timeout = 10 )


                    if int(str(r).split('[')[1].split(']')[0]) != 200:
                            r = np.zeros((256,256,4))
                    else:
                        r = np.array(Image.open(BytesIO(r.content)), dtype = 'uint8')


                    r_total[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ] = r
                        
                    loadingBar(N, len(tiles))
                    N = N+1


            r_total = np.zeros((256*(max_y_osm - min_y_osm + 1) ,256*(max_x_osm - min_x_osm + 1),4), dtype = dtype)

            size = math.floor(len(tiles)/threads) + 1
            tiles_chunks = chunks(tiles, size)
            prs = []
            for tiles in tiles_chunks:
                pr = threading.Thread(target = subTiles, args =(tiles,), daemon=True)
                pr.start()
                prs = prs + [pr] 
            for pr in prs:
                pr.join()                     
                
            min_x_index = int(round((min_x_osm_precise - min_x_osm)*256))
            max_x_index = int(round((max_x_osm_precise- min_x_osm)*256))
            min_y_index = int(round((min_y_osm_precise - min_y_osm)*256))
            max_y_index = int(round((max_y_osm_precise- min_y_osm)*256))
            
            r_total = r_total[min_y_index:max_y_index,min_x_index:max_x_index,:]
 

    if str(type(bounds)) != str(type(None)):
        trans = rasterio.transform.from_bounds(xMinWeb, yMinWeb, xMaxWeb, yMaxWeb, r_total.shape[1], r_total.shape[0])
        shape = gpd.GeoDataFrame({'geometry':[bounds]})
        shape.crs = {'init': 'epsg:4326'}
        shape = shape.to_crs({'init': 'epsg:3857'})
        raster_shape = rasterize( shapes = [ (shape['geometry'].values[m], 1) for m in np.arange(shape.shape[0]) ] , fill = 0, transform = trans, out_shape = (r_total.shape[0], r_total.shape[1]), all_touched = True )
        r_total[:,:,-1] = np.minimum(r_total[:,:,-1], raster_shape)

    r_total = r_total.astype('uint8')
    r_total = Image.fromarray(r_total)

    return(r_total)    
    
    



def seriesAdd(shapeId, layerId, geometryId, data, token, includeDatetime = True):
    data = data.copy()
    mapId = shapeId
    
    if not 'datetime' in data.columns and includeDatetime:
        raise ValueError('Dataframe has no datetime column. In case you wish to upload data without a date and time use includeDatetime = False. In this case the server will add the current datetime as datetime')

    
    if 'datetime' in data.columns:
        includeDatetime = True
        if str(data['datetime'].dtypes) == 'datetime64[ns]':
            data['datetime'] = data['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            dates = list(data['datetime'])
            del data['datetime']

        else:
           raise  ValueError('datetime column must be of type datetime')

    for c in data.columns:
            data[c] = data[c].astype(float)
        
    values = []
    for i in np.arange(data.shape[0]):
        for c in data.columns:
                value = data[c].values[i]
                if not np.isnan(value):
                    if includeDatetime:
                        values = values + [{'property':c, 'value':data[c].values[i], 'date':dates[i]}]
                    else:
                        values = values + [{'property':c, 'value':data[c].values[i]}]                    


    chunks_values = chunks(values)
    N = 0
    for values_sub in chunks_values:
        body = {"mapId":  mapId, "values":values_sub, 'layerId':layerId, 'geometryId':geometryId}
        r = s.post(url + '/series/add', headers = {"Authorization":token},
                     json = body)
        
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)

        loadingBar(N*3000 + len(values_sub), len(values))
        N = N+1


def seriesDelete(shapeId, layerId, geometryId, seriesIds, token, revert = False):
    body = {'mapId':shapeId, 'layerId':layerId, 'geometryId':geometryId, 'seriesIds':list(seriesIds), 'revert':revert}
            
    r = s.post(url + '/series/delete', headers = {"Authorization":token},
                 json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def seriesChangelog(shapeId, layerId, geometryId, limit = 100, userId = None, pageStart = None, actions = ['add', 'delete', 'revert'], token = None):
    changes = []
    keepGoing = True
    
    while keepGoing:
        pageSize = min(100, limit - len(changes))
        body = {'mapId':shapeId, 'layerId':layerId, 'geometryId':geometryId, 'pageSize':pageSize, 'actions':list(actions)}
        if str(type(userId)) != str(type(None)):
            body['userId'] = userId
        if str(type(pageStart)) != str(type(None)):
            body['pageStart'] = pageStart
    
        if token ==None:
            r = s.post(url + '/series/changelog',
                         json = body )        
        else:
            r = s.post(url + '/series/changelog', headers = {"Authorization":token},
                         json = body )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        r = r.json()
        pageStart = r['nextPageStart']
        r = r['result']

        changes = changes + r
        if len(changes) >= limit or str(type(pageStart)) == str(type(None)):
            break
    return(changes)
    

def seriesInfo(shapeId, layerId, geometryId = None, token = None):
    mapId = shapeId
    body = {'mapId':mapId, 'layerId':layerId}
    if str(type(geometryId)) != str(type(None)):
        body['geometryId'] = geometryId
        
    if token ==None:
        r = s.post(url + '/series/info',
                     json = body )        
    else:
        r = s.post(url + '/series/info', headers = {"Authorization":token},
                     json = body )

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = r.json()

    r['dateMin'] = datetime.strptime(r['dateMin'], "%Y-%m-%d %H:%M:%S")
    r['dateMax'] = datetime.strptime(r['dateMax'], "%Y-%m-%d %H:%M:%S")

    return(r)

def seriesGet(shapeId, layerId, geometryId, propertyName = None, dateFrom = None, dateTo = None, pageStart = None, userId=None, limit = None, token  = None):

    mapId = shapeId
    body = {'mapId':mapId, 'geometryId':geometryId, 'returnType':'json', 'layerId':layerId}

    if str(type(pageStart)) != str(type(None)) and str(type(pageStart)) != str(type(None)):
        raise ValueError('cannot define pageStart together with dateTo')
    if str(type(dateFrom)) != str(type(None)):
        if str(type(dateFrom)) == "<class 'datetime.datetime'>":
            dateFrom = dateFrom.strftime('%Y-%m-%d %H:%M:%S')
            pageStart = {'dateFrom':dateFrom}
        

    if str(type(userId)) != str(type(None)):
        body['userId'] = userId
    if str(type(dateTo)) != str(type(None)):
        if str(type(dateTo)) == "<class 'datetime.datetime'>":
            dateTo = dateTo.strftime('%Y-%m-%d %H:%M:%S')
        body['dateTo'] = dateTo
    if str(type(propertyName)) != str(type(None)):
        body['property'] = propertyName


    keepGoing = True
    series = []
    while keepGoing:
        
        if(str(type(pageStart)) != str(type(None))):
            body['pageStart'] = pageStart
        if(str(type(limit)) != str(type(None))):
            body['limit'] = min(5000, limit - len(series))
        
        if token ==None:
            r = s.post(url + '/series/get',
                         json = body )        
        else:
            r = s.post(url + '/series/get', headers = {"Authorization":token},
                         json = body )
    
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        r = r.json()
        pageStart = r['nextPageStart']
        series = series + r['result']

        

        if str(type(limit)) != str(type(None)) and len(series >= limit):
            keepGoing = False

        if str(type(pageStart)) == str(type(None)):
            keepGoing = False

    series = [ { 'id':k['id'], 'property': k['property'], 'value': k['value'], 'date': datetime.strptime(k['date'], "%Y-%m-%dT%H:%M:%S.%fZ") } for k in series]
    series = pd.DataFrame(series)
    return(series)

    
################################################up and downloads
def addTimestamp(mapId, startDate, token, endDate = None, bounds=None):
    if str(type(endDate)) == str(type(None)):
        endDate = startDate

    if str(type(startDate)) != "<class 'datetime.datetime'>":
        raise ValueError('startDate must of of type python date')

    if str(type(endDate)) != "<class 'datetime.datetime'>":
        raise ValueError('endDate must of of type python date')

    startDate = startDate.strftime("%Y-%m-%dT%H:%M:%S.%f")
    endDate = endDate.strftime("%Y-%m-%dT%H:%M:%S.%f")

    toAdd = {'dateFrom':startDate, 'dateTo':endDate}

    if str(type(bounds)) != str(type(None)):
        boundary = gpd.GeoSeries([bounds]).__geo_interface__['features'][0]
        boundary = boundary['geometry']
        toAdd['bounds'] = boundary        

    body = {"mapId":  mapId, "toAdd":[toAdd]}    
        
    
    r = s.post(url + '/settings/projects/reschedule', headers = {"Authorization":token},
                 json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    r = r.json()[0]
    return({'id':r})

    
def activateTimestamp(mapId, timestampId, active, token):
    toActivate = []
    toDeactivate = []
    if active:
        toActivate = [timestampId]
    else:
        toDeactivate = [timestampId]
    
    body = {'mapId':mapId, 'toActivate': toActivate, 'toDeactivate': toDeactivate}
    r = s.post(url + '/settings/projects/reschedule', headers = {"Authorization":token},
                 json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def removeTimestamp(mapId, timestampNumber, token, revert = False, hard = False):

    r = s.post(url + '/settings/projects/deleteTimestamp', headers = {"Authorization":token},
                 json = {"mapId":  mapId, "timestamp":timestampNumber, 'revert':revert, 'hard':hard})

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def getGeometryUploads(shapeId, layerId, token):
    body = {'mapId':shapeId, 'layerId': layerId}
    r = s.post(url +  '/files/geometry/getUploads', headers = {"Authorization":token},
                 json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    return(r.json())
    

def uploadRasterFile(mapId, timestampId, file, token, fileFormat = 'tif', epsg = None):
    
    if not os.path.exists(file):
            raise ValueError( file + ' not found')
    
    splitsign = os.path.join('s' ,'s')[1]
    fileName = file.split(splitsign)[-1]
    
    if not os.path.exists(file):
            raise ValueError( file + ' not found')
    
    conn_file = open(file, 'rb')
    payload = MultipartEncoder(fields = {'upload': (fileName, conn_file, 'application/octet-stream'), 'timestampId': timestampId, 'mapId':mapId, 'format':fileFormat, 'fileName':fileName})
    
    if str(type(epsg)) != str(type(None)):
        payload['epsg'] = epsg
        
    r = s.post(url + '/files/raster/upload', headers = {"Authorization":token, "Content-Type": payload.content_type}, data=payload)
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    conn_file.close()


def addShapeLayer(shapeId, layerName, token, color = "#fcba033f"):
    mapId = shapeId
    r = s.post(url + '/settings/geometryLayers/add', headers = {"Authorization":token},
                 json = {"mapId":  mapId, "color":color, "layerName":layerName, "properties":[] })

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    return(r.json())

def removeShapeLayer(shapeId, layerId, token, revert = False):
    mapId = shapeId
    r = s.post(url + '/settings/geometryLayers/delete', headers = {"Authorization":token},
                 json = {"mapId":  mapId, "layerId":layerId, "revert": revert })

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

        
def uploadGeometryFile(shapeId, layerId, file, fileFormat, token, epsg=None):
    mapId = shapeId
    
    if not os.path.exists(file):
            raise ValueError( file + ' not found')
    
    splitsign = os.path.join('s' ,'s')[1]
    fileName = file.split(splitsign)[-1]

    conn_file = open(file, 'rb')
    payload = MultipartEncoder({'upload': (fileName, conn_file, 'application/octet-stream'), "mapId":  mapId, 'layerId':layerId, 'fileName':fileName, 'format':fileFormat } )

    if str(type(epsg)) != str(type(None)):
        payload['epsg'] = int(epsg)
    
    r = s.post(url + '/files/geometry/upload' , headers = {"Authorization":token, "Content-Type": payload.content_type}, data=payload)
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    conn_file.close()
    
def addProperty(shapeId, layerId, propertyName, propertyType, token, private=False, required=False):
    mapId = shapeId
    body = {"mapId":  mapId, 'layerId':layerId, 'propertyName': propertyName, 'type':propertyType, 'private':private, 'required':required }
    
    r = s.post(url + '/settings/geometryLayers/addProperty', headers = {"Authorization":token},
                     json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    return(r.json())


def deleteProperty(shapeId, layerId, propertyName, token, revert = False):
    mapId = shapeId
    body = {"mapId":  mapId, 'layerId':layerId, 'propertyName': propertyName, 'revert':revert }
    
    r = s.post(url + '/settings/geometryLayers/deleteProperty', headers = {"Authorization":token},
                     json = body)
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)



def ShapeLayerIndex(shapeId, layerId, token, filterProperties = [], idProperty = None):
        
    if type(filterProperties) != type([]):
        raise ValueError('filterProperties must be a list with property names')

    toAdd = [ {'property': p, 'id':False } for p in filterProperties]

    if str(type(idProperty)) != str(type(None)):
        if str(type(idProperty)) != str(type('hi')):
            raise ValueError('idProperty must be of type string')
        toAdd = toAdd + [{'property': idProperty, 'id':True }]


    
    layer = [layer for layer in metadata(shapeId, True, token)['geometryLayers'] if layer['id'] == layerId]
    if len(layer) == 0:
        raise ValueError('layerId not found in this shape')
        
    layer = layer[0]
    properties = layer['properties']    
    currentFilterProperties = [p for p in properties if 'filtering' in p.keys() ]

    names = [n['property'] for n in toAdd]
    toRemove = list( set(currentFilterProperties).difference(set(names)) )    
    
    body = {"mapId":shapeId,"layerId":layerId}
    
    
    if len(toAdd) >0:
        body['propertiesToAdd'] = toAdd
        
    if len(toRemove) > 0:
        body['propertiesToRemove'] = toRemove

    if len(toRemove) == 0 and len(toAdd) ==0:
        raise ValueError('The current properties are already the current filter properties')
    
    r = s.post(url + '/settings/geometryLayers/reIndex', headers = {"Authorization":token},
                     json = body)
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)



def shapeLayerAddStyle(shapeId, layerId, styleName, rules, token, isDefault=False):
    rules_new = []
    for rule in rules:
        value = rule['value']
        if 'float' in str(type(value)):
            value = float(value)
        elif 'int' in str(type(value)):
            value = int(value)
        elif 'str' in str(type(value)):
            value = str(value)
        elif 'bool' in str(type(value)):
            value = bool(value)
        else:
            raise ValueError('value must be a float, int or string')
        rules_new = rules_new + [ {'property': str(rule['property']) , 'value': value , 'operator': str(rule['operator']) , 'color': str(rule['color']) } ]

    body = {'mapId':shapeId, 'layerId': layerId, 'rules':rules_new, 'styleName':styleName, 'isDefault':isDefault }
    r = s.post(url + '/settings/geometryLayers/addStyle', headers = {"Authorization":token},
                     json = body)
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    r= r.json()
    return(r)

def shapeLayerRemoveStyle(shapeId, layerId, styleId, token):

    body = {'mapId':shapeId, 'layerId': layerId, 'styleId':styleId}
    r = s.post(url + '/settings/geometryLayers/removeStyle', headers = {"Authorization":token},
                     json = body)
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)



def mapVisualisationAdd(mapId, name, method , bands, parameters, token):
    parameter = json.loads(json.dumps(parameters))
    body = {'mapId': mapId, 'name':name, 'method':method, 'bands':list(bands), 'overwrite':False, 'parameters':parameter}
    r = s.post(url + '/settings/mapLayers/add', headers = {"Authorization":token},
                     json = body)
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    return(r.json())

def mapVisualisationRemove(mapId, layerId, token):
    body = {'mapId': mapId, 'layerId':layerId}
    r = s.post(url + '/settings/mapLayers/delete', headers = {"Authorization":token},
                     json = body)
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


############################new projects
def newShape(name, token):

    r = s.post(url + '/settings/projects/newShape', headers = {"Authorization":token},
                     json = {"name":  name})
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r)

def updateBounds(shapeId, token, boundary):
    boundary = gpd.GeoSeries([boundary]).__geo_interface__['features'][0]
    boundary = boundary['geometry']

    body = {"mapId":  shapeId, 'bounds':boundary}

    r = s.post(url + '/settings/projects/newBounds', headers = {"Authorization":token},
                     json = body)
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    
def newMap(name,  token):

    body = {'name':name}

    r = s.post(url + '/settings/projects/newMap', headers = {"Authorization":token},
                     json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r)


def newOrder(name, token,  dataSource = 'sentinel2RGBIR' ):

    body = {'name':name, 'dataSource':{'name':dataSource}}


    r = s.post(url + '/settings/projects/newMap', headers = {"Authorization":token},
                     json = body)


    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r)


def projectProperties(projectId, properties, token):
    mapId = projectId
    body = {'mapId':mapId, 'properties':properties}
    r = s.post(url + '/settings/organize/properties', headers = {"Authorization":token},
                     json = body)


    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    

def projectAddHashtag(projectId, hashtag, token):
    mapId = projectId
    body = {'mapId':mapId, 'hashtag':hashtag}
    
    r = s.post(url + '/settings/organize/addHashtag', headers = {"Authorization":token},
                     json = body)


    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def projectRemoveHashtag(projectId, hashtag, token):
    mapId = projectId
    body = {'mapId':mapId, 'hashtag':hashtag}
    r = s.post(url + '/settings/organize/removeHashtag', headers = {"Authorization":token},
                     json = body)


    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def projectDescription(projectId, description, token):
    r = s.post(url + '/settings/organize/description', headers = {"Authorization":token},
                     json = {'mapId':projectId, 'description':description })
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)





##################################################################################################################




def plotPolys(polys, xMin = None,xMax = None,yMin=None,yMax= None, alpha = None, image = None, colors = {0:(0,0,255)} , column= None):
    polys.crs = {'init': 'epsg:4326'}

    if str(type(xMin)) == str(type(None)):
        polys_union = polys.unary_union
        bbox = gpd.GeoDataFrame({'geometry':[polys_union]})
        xMin = bbox.bounds['minx'].values[0]
        yMin = bbox.bounds['miny'].values[0]
        xMax = bbox.bounds['maxx'].values[0]
        yMax = bbox.bounds['maxy'].values[0]
        
    bbox = gpd.GeoDataFrame( {'geometry': [Polygon([(xMin,yMin), (xMax, yMin), (xMax, yMax), (xMin, yMax)])]} )
    bbox.crs = {'init': 'epsg:4326'}
    bbox = bbox.to_crs({'init': 'epsg:3785'})
    polys = polys.to_crs({'init': 'epsg:3785'})

    if str(type(image)) == "<class 'NoneType'>":
        if (xMax-xMin) > (yMax - yMin):
            image = np.zeros((1024,1024* int((xMax-xMin)/(yMax-yMin)),4))
        else:
            image = np.zeros((1024* int((yMax-yMin)/(xMax-xMin)),1024,4))
            
    image = image/255
    if column == None:
        column = 'extra'
        polys[column] = 0
    
    transform = rasterio.transform.from_bounds(bbox.bounds['minx'], bbox.bounds['miny'], bbox.bounds['maxx'], bbox.bounds['maxy'], image.shape[1], image.shape[0])
    rasters = np.zeros(image.shape)
    for key in colors.keys():
        sub_polys = polys.loc[polys[column] == key]
        if sub_polys.shape[0] >0:
            raster = rasterize( shapes = [ (sub_polys['geometry'].values[m], 1) for m in np.arange(sub_polys.shape[0]) ] , fill = 0, transform = transform, out_shape = (image.shape[0], image.shape[1]), all_touched = True )
            raster = np.stack([raster * colors[key][0]/255, raster*colors[key][1]/255,raster*colors[key][2]/255, raster ], axis = 2)
            rasters = np.add(rasters, raster)
     
    rasters = np.clip(rasters, 0,1)

    image_out = rasters
    image_out[image_out[:,:,3] == 0, :] = image [image_out[:,:,3] == 0, :]
    if alpha != None:
        image_out = image * (1 - alpha) + image_out*alpha 

    image_out = image_out *255
    image_out = image_out.astype('uint8')
    return(image_out)


def chunks(l, n = 3000):
    result = list()
    for i in range(0, len(l), n):
        result.append(l[i:i+n])
    return(result)
    

 
def cover(bounds, w):
    if str(type(bounds)) == "<class 'shapely.geometry.polygon.Polygon'>" :
        bounds = [bounds]
    elif str(type(bounds)) =="<class 'shapely.geometry.multipolygon.MultiPolygon'>":
        bounds = bounds
    else:
        raise ValueError('bounds must be a shapely polygon or multipolygon')

    bound = bounds[0]
    coords_total = pd.DataFrame()
    for bound in bounds:
         x1, y1, x2, y2  = bound.bounds

         step_y =  w/geodesic((y1,x1), (y1 - 1,x1)).meters
         parts_y = math.floor((y2 - y1)/ step_y + 1)

         y1_vec = y1 + np.arange(0, parts_y )*step_y
         y2_vec = y1 + np.arange(1, parts_y +1 )*step_y
             
         steps_x = [   w/geodesic((y,x1), (y,x1+1)).meters for y in y1_vec  ]

         parts_x = [math.floor( (x2-x1) /step +1 ) for step in steps_x ]      
             
     
         coords = pd.DataFrame()
         for n in np.arange(len(parts_x)):
             x1_sq = [ x1 + j*steps_x[n] for j in np.arange(0,parts_x[n]) ]
             x2_sq = [ x1 + j*steps_x[n] for j in np.arange(1, parts_x[n]+1) ]
             coords_temp = {'x1': x1_sq, 'x2': x2_sq, 'y1': y1_vec[n], 'y2':y2_vec[n]}
             coords = coords.append(pd.DataFrame(coords_temp))
         coords_total = coords_total.append(coords)

    cover = [Polygon([ (coords_total['x1'].iloc[j] , coords_total['y1'].iloc[j]) , (coords_total['x2'].iloc[j] , coords_total['y1'].iloc[j]), (coords_total['x2'].iloc[j] , coords_total['y2'].iloc[j]), (coords_total['x1'].iloc[j] , coords_total['y2'].iloc[j]) ]) for j in np.arange(coords_total.shape[0])]
     


    coords = gpd.GeoDataFrame({'geometry': cover, 'x1':coords_total['x1'], 'x2':coords_total['x2'], 'y1':coords_total['y1'], 'y2':coords_total['y2'] })

    coords.crs = {'init': 'epsg:4326'}

    return(coords)
    

    
def loadingBar(count,total):
    if total == 0:
        return
    else:
        percent = float(count)/float(total)*100
        sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent) + ' '*(100-int(percent)) + ']')

########################
    
