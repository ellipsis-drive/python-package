#python3 setup.py sdist bdist_wheel
#twine upload --repository pypi dist/*

import pandas as pd
from PIL import Image
import geopandas as gpd
from pyproj import Proj, transform
import base64
import numpy as np
from io import BytesIO
from io import StringIO
import time
import requests
import rasterio
import math
import datetime
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
import xmltodict


__version__ = '1.1.31'
url = 'https://api.ellipsis-drive.com/v1'
#url = 'https://dev.api.ellipsis-earth.com/v2'
s = requests.Session()
warnings.filterwarnings("ignore")

CACHE = {'metadata':{}, 'wms':{}}

def logIn(username, password):
        r =s.post(url + '/account/login/',
                         json = {'username':username, 'password':password} )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        token = r.json()
        token = token['token']
        token = 'Bearer ' + token
        return(token)




def getMapId(name, token = None):

    body = {'name':name, 'nameFuzzy':False, 'access':['public','subscribed','owned']}    
    if token == None:
        r = s.post(url + '/account/maps', json = body )
    else:
        r = s.post(url + '/account/maps', json = body, 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    results = r.json()['result']
    if( len(results) == 0):
        raise ValueError('Map not found')
    
    
    return(results[0]['id'])

def getShapeId(name, token = None):

    body = {'name':name, 'nameFuzzy':False, 'access':['public','subscribed','owned']}    
    if token == None:
        r = s.post(url + '/account/shapes', json = body )
    else:
        r = s.post(url + '/account/shapes', json = body, 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    results = r.json()['result']
    if( len(results) == 0):
        raise ValueError('Map not found')
    
    
    return(results[0]['id'])

    
def metadata(projectId, token = None):
    mapId = projectId
    if token == None:
        r = s.post(url + '/metadata',
                         json = {"mapId":  mapId})
    else:
        r = s.post(url + '/metadata', headers = {"Authorization":token},
                         json = {"mapId":  mapId})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    CACHE['metadata'][projectId] = r
    return(r)


def getShapes(namePart= None, access = ['subscribed', 'public', 'owned'], atlas = None, bounds=None, username= None, token = None):
    
    body = {'access': access}
    if str(type(namePart)) != str(type(None)):
        body['name'] = namePart        
        body['nameFuzzy'] = True        
    if str(type(atlas)) != str(type(None)):
        body['atlas'] = atlas
    if str(type(atlas)) != str(type(None)):
        body['atlas'] = atlas
    if str(type(username)) == str(type(None)):
        body['username'] = username
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
        results = results + result
        if len(result) < 100:
            keepGoing = False
            
    return(results)
    

def getMaps(namePart= None, access = ['subscribed', 'public', 'owned'], atlas = None, bounds = None, username= None, bandType=None, resolutionRange=None, dateRange=None, token = None):

    body = {'access': access}
    if str(type(namePart)) != str(type(None)):
        body['name'] = namePart        
        body['nameFuzzy'] = True        
    if str(type(atlas)) != str(type(None)):
        body['atlas'] = atlas
    if str(type(atlas)) != str(type(None)):
        body['atlas'] = atlas
    if str(type(username)) != str(type(None)):
        body['username'] = username
    if str(type(dateRange)) != str(type(None)):
        body['dateFrom'] = dateRange['dateFrom'].strftime('%Y-%m-%d %H:%M:%S')
        body['dateTo'] = dateRange['dateTo'].strftime('%Y-%m-%d %H:%M:%S')
    if str(type(bandType)) != str(type(None)):
        body['bandType'] = bandType
    if str(type(resolutionRange)) != str(type(None)):
        body['resolution'] = resolutionRange
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
        if len(result) < 100:
            keepGoing = False
            
    return(results)
    
    
def rasterAggregate(mapId, geometry, aggregation = 'mean', timestamp=0, token = None):
    
    geometry =  gpd.GeoSeries([geometry]).__geo_interface__['features'][0]
    body = {"mapId": mapId, 'geometry':geometry['geometry'], 'timestamp':timestamp, 'aggregation':aggregation}

    if token == None:
        r = s.post(url + '/data/geometry',
                         json = body)
    else:
        r = s.post(url + '/data/geometry', headers = {"Authorization":token},
                         json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    r = r.json()
    r_dict = {}
    for c in r.keys():
        r_dict[c] = [r[c]]
        
    r  = pd.DataFrame(r_dict)

    return(r)


    

def getBounds(mapId, timestamp = None, token = None ):
    body = {"mapId": mapId}

    if str(type(timestamp)) != str(type(None)):
        body['timestamp'] = timestamp

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
    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union
    return(r)
        
        
def geometryGet(shapeId, layer, geometryIds = None, historyFilter = None, filters = None, xMin = None, xMax = None, yMin=None, yMax=None, wait = 0, deleted = False, limit = None, token = None):
    mapId = shapeId
    
    body = {"mapId":  mapId, 'layer':layer, 'deleted':deleted}
    if str(type(xMin)) != str(type(None)):
        body['bounds'] = {'xMin': float(xMin) , 'xMax':float(xMax), 'yMin':float(yMin), 'yMax':float(yMax)}
    if str(type(geometryIds)) != str(type(None)):
        body['geometryIds'] = geometryIds
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
            body['metadataFilters'] = filters
        except:
            raise ValueError('filters must be an array with dictionaries. Each dictionary should have a property, key, operator and value')
    if str(type(historyFilter)) != str(type(None)):
        if 'dateFrom' in historyFilter.keys():
                historyFilter['dateFrom'] = historyFilter['dateFrom'].strftime('%Y-%m-%d %H:%M:%S')
        if  'dateTo' in historyFilter.keys():
                historyFilter['dateTo'] = historyFilter['dateTo'].strftime('%Y-%m-%d %H:%M:%S') 
        body['history'] = historyFilter

    body = json.dumps(body)
    body = json.loads(body)


    body['returnType'] = 'all'
    keepGoing = True
    sh = gpd.GeoDataFrame()

    while (keepGoing):
        if str(type(limit)) != str(type(None)):
            limit = min(5000, limit - sh.shape[0])
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
        if len(r['result']['features']) < 5000:
            keepGoing = False

        sh  = sh.append(gpd.GeoDataFrame.from_features(r['result']['features']))
        body['pageStart'] = r['nextPageStart']
        time.sleep(wait)
            

        loadingBar(sh.shape[0],sh.shape[0])
            
    sh.crs = {'init': 'epsg:4326'}

    return(sh)


        

def geometryVersions(shapeId, geometryId, token = None):
    mapId = shapeId
    body = {"mapId":  mapId, 'geometryId':geometryId}
    if token == None:
        r = s.post(url + '/geometry/versions',
                         json = body)    
    else:
        r = s.post(url + '/geometry/versions', headers = {"Authorization":token},
                         json = body)    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    versions = r.json()

    sh = gpd.GeoDataFrame()
    for version in versions:
        body = {"mapId":  mapId, 'geometryIds':[geometryId], 'type':'polygon', 'version':version['version']}
        if token == None:
            r = s.post(url + '/geometry/get',
                             json = body)    
        else:
            r = s.post(url + '/geometry/get', headers = {"Authorization":token},
                             json = body)    
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        r  = gpd.GeoDataFrame.from_features(r.json()['result']['features'])
        r['version'] = version['version']
        r['creationDate'] = version['editDate']
        r['creationUser'] = version['editUser']
        sh = sh.append(r)
    sh.crs = {'init': 'epsg:4326'}
    return(sh)

    


def geometryDelete(shapeId, geometryIds, token, revert= False):

    body = {"mapId":  shapeId, 'geometryIds': list(geometryIds), 'rever':revert}

    r= s.post(url + '/geometry/delete', headers = {"Authorization":token},
                     json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def geometryEdit(shapeId, geometryIds, features, token):
    features = features.copy()
    del features['id']
    del features['user']
    del features['creationDate']
    del features['layer']


    mapId = shapeId
    if not str(type(features)) ==  "<class 'geopandas.geodataframe.GeoDataFrame'>":
        raise ValueError('features must be of type geopandas dataframe')
        
    features = features.to_crs({'init': 'epsg:4326'})
    
    indices = chunks(np.arange(features.shape[0]))

    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        features_sub = features.iloc[indices_sub]
        geometryIds_sub = geometryIds[indices_sub]

        features_sub =features_sub.to_json(na='drop')
        features_sub = json.loads(features_sub)

        changes = [{'geometryId':x[0] , 'newProperties':x[1]['properties'], 'newGeometry':x[1]['geometry']} for x in zip(geometryIds_sub, features_sub['features'])]
        
        body = {"mapId":  mapId, 'changes':changes}
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


        loadingBar(i*3000 + len(indices_sub),features.shape[0])
        i = i+1


def geometryMove(shapeId, geometryIds, newLayer, token):
    mapId = shapeId
    geometryIds = list(geometryIds)
    chunks_ids = chunks(geometryIds)
    N=0
    for chunk_ids in chunks_ids:
        r = s.post(url + '/geometry/move', headers = {"Authorization":token},
                         json = {"mapId":  mapId, 'geometryIds':chunk_ids, 'newLayer':newLayer})
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        loadingBar(N*3000 + len(chunk_ids), len(geometryIds))
        N=N+1


    
    
def geometryAdd(shapeId, layer, features, token):
    mapId = shapeId
    if not str(type(features)) ==  "<class 'geopandas.geodataframe.GeoDataFrame'>":
        raise ValueError('features must be of type geopandas dataframe')

    if str(type(features.crs)) == str(type(None)) and min(features.bounds['minx']) > -180  and max(features.bounds['maxx']) < 180 and min(features.bounds['miny']) > -90  and max(features.bounds['maxy']) < 90:
        print('assuming WGS84 coordinates')
    elif str(type(features.crs)) == str(type(None)):
        raise ValueError('Please provide CRS for the geopandas dataframe or translate to WGS84 coordinates')
    else:
        features = features.to_crs({'init': 'epsg:4326'})
    
    firstTime = metadata(projectId = mapId, token = token)['geometryLayers']
    firstTime = [x for x in firstTime if x['name'] == layer]
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
            elif 'float' in str(features.dtypes[c]):
                propertyType = 'float'
            elif 'bool' in str(features.dtypes[c]):
                propertyType = 'boolean'
            else:
                propertyType = 'string'
                
            addProperty(shapeId = mapId, layer =layer, propertyName = c, propertyType = propertyType, token = token)


    indices = chunks(np.arange(features.shape[0]))

    #add properties manually
    addedIds = []
    for i in np.arange(len(indices)):
        indices_sub = indices[i]
        features_sub = features.iloc[indices_sub]
        features_sub =features_sub.to_json(na='drop')
        features_sub = json.loads(features_sub)
        #float to int
        
        
        body = {"mapId":  mapId, "layer":layer, "features":features_sub['features']}
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

        
    
def messageGet(shapeId, users= None, userGroups=None, messageIds =None, geometryIds=None, showLoadingBar=False, includeDeleted=False, token = None):
    mapId = shapeId
    messages = []
    Continue = True
    body={'mapId':mapId, 'includeDeleted':includeDeleted}

    if str(type(users)) != str(type(None)):
        body['users']=users
    if str(type(userGroups)) != str(type(None)):
        body['userGroups']=userGroups
    if str(type(messageIds)) != str(type(None)):
        body['messageIds']=messageIds
    if str(type(geometryIds)) != str(type(None)):
        body['geometryIds']=geometryIds
    
    if showLoadingBar:
        body['returnType']='count'
        if token == None:
            r = s.post(url + '/message/get',
                         json = body )        
        else:
            r = s.post(url + '/message/get', headers = {"Authorization":token},
                         json = body )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r =  r.json()
        count = r['count']        
    
    body['returnType']='all'

    while(Continue):
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
        Continue = len(r['result']) ==100
        messages = messages +  r['result']
        if showLoadingBar:
            loadingBar(len(messages), count)
    
    return(messages)
def messageAdd(shapeId, geometryId, token, attachFile=None, replyTo = None, message = None, private= None, image=None, lon=None, lat=None): 
    mapId = shapeId    
    body = {'mapId':mapId, 'geometryId':geometryId}
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

    if str(type(attachFile)) != str(type(None)):
            fileName = attachFile.split('/')[-1].split('/')[-1]

            files = {'upload': open(attachFile,'rb')}
            body = {'mapId':mapId, 'messageId':messageId, 'fileName':fileName}

            r = s.post(url + '/message/attach', headers = {"Authorization":token},
                         data = body, files =files )
            if int(str(r).split('[')[1].split(']')[0]) != 200:
                raise ValueError(r.text)


    return(messageId)

def messageDelete(shapeId, messageId, token):    
    mapId = shapeId
    body = {'mapId':mapId, 'messageId':messageId}
    r = s.post(url + '/message/delete', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    


def messageImage(shapeId, messageId, token = None):
    mapId = shapeId
    body = {'mapId':mapId, 'messageId':messageId}
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

def messageAttachement(shapeId, messageId, fileName, token = None):
    mapId = shapeId    
    body = {'mapId':mapId, 'messageId':messageId}
    if token ==None:
        r = s.post(url + '/message/downloadAttachment',
                     json = body )        
    else:
        r = s.post(url + '/message/downloadAttachment', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    open(fileName, 'wb').write(r.content)


def rasterRaw(mapId, timestamp, xMin= None,xMax= None,yMin=None, yMax=None, bounds=None, downsample = False, width = None, height = None, token = None):
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
    if token != None:
        token_inurl = '?token=' + token.replace('Bearer ', '')

    if downsample:
        if str(type(width)) == str(type(None)) or str(type(height)) == str(type(None)):
            raise ValueError('if downsample is true, width and height are required')

        if mapId in CACHE['metadata'].keys():
            timestamps = CACHE['metadata'][mapId]['timestamps']
        else:
            timestamps = metadata(mapId, token)['timestamps']

        if mapId in CACHE['wms'].keys():
            layers = CACHE['wms'][mapId]
        else:
            r = s.get(url + '/wms/raw/' + mapId + '?SERVICE=WMS&REQUEST=GetCapabilities' + token_inurl)                
            d = xmltodict.parse(r.text)
            layers = {}
            for layer in d['Capabilities']['Capability']['Layer']:
                layers[layer['Title']] = layer['Name']
                
            CACHE['wms'][mapId] = layers

        timestampDate = next(item['dateTo'] for item in timestamps if item["timestamp"] == timestamp)
        timestampDate = str(timestampDate).split('T')[0]
        layerId = layers[timestampDate + '_' + str(timestamp)]
        w = int(width)
        h = int(height)
        r = s.get(url + '/wms/raw/' + mapId + '?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=' + str(yMinWeb) + ',' + str(xMinWeb) + ',' + str(yMaxWeb) + ',' + str(xMaxWeb) + '&CRS=EPSG:3857&WIDTH=' + str(w) + '&HEIGHT=' + str(h) + '&LAYERS=' + layerId + '&STYLES=&FORMAT=image/tiff&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi:96&TRANSPARENT=TRUE' + token_inurl)

        if int(str(r).split('[')[1].split(']')[0]) != 200:
                raise ValueError(r.text)
        else:
                 with MemoryFile(r.content) as memfile:
                     with memfile.open() as dataset:
                         r_total = dataset.read()
        r_total = np.transpose(r, (1,2,0) )


    else:
            if mapId in CACHE['metadata'].keys():
                bands = CACHE[mapId]['bands']
            else:
                bands = metadata(mapId)['bands']
            num_bands = len(bands)


            if token == None:
               zoom = int(metadata(mapId)['zoom'])
            else:
               zoom = int(metadata(mapId, token = token)['zoom'])

            
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
            
            for tileY in y_tiles:
                for tileX in x_tiles:
                    x_index = tileX - min_x_osm
                    y_index = tileY - min_y_osm

                    r = s.get(url + '/tileService/' + mapId + '/' + str(timestamp) + '/data/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY) + token_inurl ,
                                 timeout = 10 )


                    if int(str(r).split('[')[1].split(']')[0]) != 200:
                        if r.json()['message'] == 'tile does not exist':
                            r = np.zeros((256,256,num_bands))
                        else:
                            raise ValueError(r.text)
                    else:
                             with MemoryFile(r.content) as memfile:
                                 with memfile.open() as dataset:
                                     r = dataset.read()
                    r = np.transpose(r, (1,2,0) )

                    bands = list(np.arange(num_bands-1))
                    bands.append(r.shape[2]-1)
                    r_total[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ] = r[:,:, bands]
                        

                    loadingBar(x_index + y_index*len(x_tiles) + 1,len(x_tiles)*len(y_tiles))
                
                
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


    return(r_total)



def rasterVisual(mapId, timestamp, layerName, xMin= None,xMax= None,yMin=None, yMax=None, bounds=None, downsample = False, width = None, height=None, token = None):

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

        if mapId in CACHE['metadata'].keys():
            timestamps = CACHE['metadata'][mapId]['timestamps']
        else:
            timestamps = metadata(mapId, token)['timestamps']

        if mapId in CACHE['wms'].keys():
            layers = CACHE['wms'][mapId]
        else:
            r = s.get(url + '/wms/' + mapId + '?SERVICE=WMS&REQUEST=GetCapabilities' + token_inurl)                
            d = xmltodict.parse(r.text)
            layers = {}
            for layer in d['Capabilities']['Capability']['Layer']:
                layers[layer['Title']] = layer['Name']
                
            CACHE['wms'][mapId] = layers

        timestampDate = next(item['dateTo'] for item in timestamps if item["timestamp"] == timestamp)
        timestampDate = str(timestampDate).split('T')[0]
        layerId = layers[timestampDate + '_' + str(timestamp) + '_' + layerName]
        w = int(width)
        h = int(height)
        r = s.get(url + '/wms/raw/' + mapId + '?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=' + str(yMinWeb) + ',' + str(xMinWeb) + ',' + str(yMaxWeb) + ',' + str(xMaxWeb) + '&CRS=EPSG:3857&WIDTH=' + str(w) + '&HEIGHT=' + str(h) + '&LAYERS=' + layerId + '&STYLES=&FORMAT=image/tiff&DPI=96&MAP_RESOLUTION=96&FORMAT_OPTIONS=dpi:96&TRANSPARENT=TRUE' + token_inurl)

        if int(str(r).split('[')[1].split(']')[0]) != 200:
                raise ValueError(r.text)
        else:
           r_total = np.array(Image.open(BytesIO(r.content)), dtype = 'uint8')
            

    else:

        if mapId in CACHE['metadata'].keys():
            zoom = CACHE[mapId]['zoom']
        else:
            zoom = metadata(mapId, token = token)['zoom']

            
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

            r_total = np.zeros((256*(max_y_osm - min_y_osm + 1) ,256*(max_x_osm - min_x_osm + 1),4), dtype = dtype)
            
            for tileY in y_tiles:
                for tileX in x_tiles:
                    x_index = tileX - min_x_osm
                    y_index = tileY - min_y_osm

                    r = s.get(url + '/tileService/' + mapId + '/' + str(timestamp) + '/data/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY) + token_inurl ,
                                 timeout = 10 )


                    if int(str(r).split('[')[1].split(']')[0]) != 200:
                        if r.json()['message'] == 'tile does not exist':
                            r = np.zeros((256,256,4))
                        else:
                            raise ValueError(r.text)
                    else:
                        r = np.array(Image.open(BytesIO(r.content)), dtype = 'uint8')


                    r_total[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ] = r
                        

                    loadingBar(x_index + y_index*len(x_tiles) + 1,len(x_tiles)*len(y_tiles))
                
                
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
    
    



def seriesAdd(shapeId, geometryId, data, token, includeDatetime = True):
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
        body = {"mapId":  mapId, "values":values_sub, 'geometryId':geometryId}
        r = s.post(url + '/series/add', headers = {"Authorization":token},
                     json = body)
        
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)

        loadingBar(N*3000 + len(values_sub), len(values))
        N = N+1


def seriesDelete(shapeId, geometryId, token, user = None, dateFrom = None, dateTo = None, revert = False, history=None):
    mapId = shapeId
    body = {'mapId':mapId, 'geometryId':geometryId, 'revert':revert}
    if str(type(user)) != str(type(None)):
        body['user'] = user
    if str(type(dateTo)) != str(type(None)):
        if str(type(dateTo)) == "<class 'datetime.datetime'>":
            dateTo = dateTo.strftime('%Y-%m-%d %H:%M:%S')
        body['dateTo'] = dateTo
    if str(type(dateFrom)) != str(type(None)):
        if str(type(dateFrom)) == "<class 'datetime.datetime'>":
            dateFrom = dateFrom.strftime('%Y-%m-%d %H:%M:%S')
        body['dateFrom'] = dateFrom

    if str(type(history)) != str(type(None)):
            if 'dateFrom' in history.keys():
                history['dateFrom'] = history['dateFrom'].strftime('%Y-%m-%d %H:%M:%S')
            if 'dateTo' in history.keys():
                history['dateTo'] = history['dateTo'].strftime('%Y-%m-%d %H:%M:%S')
            body['history'] = history
            
    r = s.post(url + '/series/delete', headers = {"Authorization":token},
                 json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def seriesInfo(shapeId, geometryId = None, token = None):
    mapId = shapeId
    body = {'mapId':mapId}
    if str(type(geometryId)) != str(type(None)):
        body['geometryId'] = geometryId
        
    if token ==None:
        r = s.post(url + '/series/info',
                     json = body )        
    else:
        r = s.post(url + '/series/info', headers = {"Authorization":token},
                     json = body )
        
    r = r.json()
    return(r)

def seriesGet(shapeId, geometryId, propertyString = None, dateFrom = None, dateTo = None, user=None, historyFilter = None, deleted = False, token  = None):
    mapId = shapeId
    body = {'mapId':mapId, 'geometryId':geometryId, 'deleted':deleted}
    if str(type(user)) != str(type(None)):
        body['user'] = user
    if str(type(dateTo)) != str(type(None)):
        if str(type(dateTo)) == "<class 'datetime.datetime'>":
            dateTo = dateTo.strftime('%Y-%m-%d %H:%M:%S')
        body['dateTo'] = dateTo
    if str(type(dateFrom)) != str(type(None)):
        if str(type(dateFrom)) == "<class 'datetime.datetime'>":
            dateFrom = dateFrom.strftime('%Y-%m-%d %H:%M:%S')
        body['dateFrom'] = dateFrom
    if str(type(propertyString)) != str(type(None)):
        body['property'] = propertyString

    if str(type(historyFilter)) != str(type(None)):
        if 'dateFrom' in historyFilter.keys():
                historyFilter['dateFrom'] = historyFilter['dateFrom'].strftime('%Y-%m-%d %H:%M:%S')
        if  'dateTo' in historyFilter.keys():
                historyFilter['dateTo'] = historyFilter['dateTo'].strftime('%Y-%m-%d %H:%M:%S') 
        body['history'] = historyFilter


    if token ==None:
        r = s.post(url + '/series/get',
                     json = body )        
    else:
        r = s.post(url + '/series/get', headers = {"Authorization":token},
                     json = body )

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    r = pd.read_csv(StringIO(r.text))
    if r.shape[0]>0:
        r['date'] = pd.to_datetime(r['date'], format="%Y-%m-%d %H:%M:%S")
    return(r)

def seriesAggregated(shapeId, geometryIds, aggregation = 'mean',  dateFrom = None, dateTo = None, user=None, token = None):
    mapId = shapeId
    body = {'mapId':mapId, 'geometryIds': list(geometryIds), 'aggregation' : aggregation}
    if str(type(user)) == str(type(None)):
        body['user'] = user
    if str(type(dateTo)) != str(type(None)):
        if str(type(dateTo)) == "<class 'datetime.datetime'>":
            dateTo = dateTo.strftime('%Y-%m-%d %H:%M:%S')
        body['dateTo'] = dateTo
    if str(type(dateFrom)) != str(type(None)):
        if str(type(dateFrom)) == "<class 'datetime.datetime'>":
            dateFrom = dateFrom.strftime('%Y-%m-%d %H:%M:%S')
        body['dateFrom'] = dateFrom

    if token ==None:
        r = s.post(url + '/series/aggregated',
                     json = body )        
    else:
        r = s.post(url + '/series/aggregated', headers = {"Authorization":token},
                     json = body )

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    r = pd.read_csv(StringIO(r.text))
    return(r)




    
################################################up and downloads
def addCapture(mapId, startDate, endDate, token):
    startDate = startDate.strftime('%Y-%m-%d')
    endDate = endDate.strftime('%Y-%m-%d')
    r = s.post(url + '/settings/projects/reschedule', headers = {"Authorization":token},
                 json = {"mapId":  mapId, "toAdd":[{'startDate':startDate, 'endDate':endDate}]})

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    r = r.json()[0]
    return(r)

    
def activateMap(mapId, active, token):

    r = s.post(url + '/settings/projects/reschedule', headers = {"Authorization":token},
                 json = {"mapId":  mapId, 'active':active})

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def removeCapture(mapId, captureId, token):

    r = s.post(url + '/settings/projects/reschedule', headers = {"Authorization":token},
                 json = {"mapId":  mapId, "toRemove":[captureId]})

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def uploadRasterFile(mapId, timestampId, file, token, fileFormat = 'tif', epsg = None):
    
    if not os.path.exists(file):
            raise ValueError( file + ' not found')
    
    splitsign = os.path.join('s' ,'s')[1]
    fileName = file.split(splitsign)[-1]

    conn_file = open(file, 'rb')
    
    if not os.path.exists(file):
            raise ValueError( file + ' not found')
    
    conn_file = open(file, 'rb')
    payload = MultipartEncoder({'upload': (fileName, conn_file, 'application/octet-stream'), 'captureId': timestampId, 'format':fileFormat, 'fileName':fileName})
    
    if str(type(epsg)) != str(type(None)):
        payload['epsg'] = epsg
        
    r = s.post(url + '/files/raster/upload', headers = {"Authorization":token, "Content-Type": payload.content_type}, data=payload)
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    conn_file.close()


def addShapeLayer(shapeId, layerName, token, color = "fcba033f"):
    mapId = shapeId
    r = s.post(url + '/settings/geometryLayers/add', headers = {"Authorization":token},
                 json = {"mapId":  mapId, "color":color, "layerName":layerName, "properties":[] })

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def deleteShapeLayer(shapeId, layerName, token):
    mapId = shapeId
    r = s.post(url + '/settings/geometryLayers/delete', headers = {"Authorization":token},
                 json = {"mapId":  mapId, "layerName":layerName })

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

        
def uploadGeometryFile(shapeId, layerName, file, fileFormat, token, epsg=None):
    mapId = shapeId
    
    if not os.path.exists(file):
            raise ValueError( file + ' not found')
    
    splitsign = os.path.join('s' ,'s')[1]
    fileName = file.split(splitsign)[-1]

    conn_file = open(file, 'rb')
    payload = MultipartEncoder({'upload': (fileName, conn_file, 'application/octet-stream'), "mapId":  mapId, 'layer':layerName, 'fileName':fileName, 'format':fileFormat } )

    if str(type(epsg)) != str(type(None)):
        payload['epsg'] = int(epsg)
    
    r = s.post(url + '/files/geometry/upload' , headers = {"Authorization":token, "Content-Type": payload.content_type}, data=payload)
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    else:
        print('upload completed')

    conn_file.close()
        
def addProperty(shapeId, layer, propertyName, propertyType, token, private=False, required=False):
    mapId = shapeId
    body = {"mapId":  mapId, 'layerName':layer, 'propertyName': propertyName, 'type':propertyType, 'private':private, 'required':required }

    r = s.post(url + '/settings/geometryLayers/addProperty', headers = {"Authorization":token},
                     json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def shapeLayerAddStyle(shapeId, layerId, styleName, rules, isDefault, token):
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
    print(json.dumps(body))
    r = s.post(url + '/settings/geometryLayers/addStyle', headers = {"Authorization":token},
                     json = body)
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    r= r.json()
    return(r)

def shapeLayerDeleteStyle(shapeId, layerId, styleId, token):

    body = {'mapId':shapeId, 'layerId': layerId, 'styleId':styleId}
    print(json.dumps(body))
    r = s.post(url + '/settings/geometryLayers/deleteStyle', headers = {"Authorization":token},
                     json = body)
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    
############################new projects
def newShape(name, token, dryRun = True):

    r = s.post(url + '/settings/projects/newShape', headers = {"Authorization":token},
                     json = {"name":  name, 'dryRun':dryRun})
    
    
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
    

def getBands(token=None):
    body = {}
    if str(type(token)) == str(type(None)):
        r = s.post(url + '/settings/projects/bands',
                         json = body)    
    else:
        r = s.post(url + '/settings/projects/bands', headers = {"Authorization":token},
                         json = body)    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)



    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r['id'])
    
    
def addBand(name, token):
    body = {'name':name}
    r = s.post(url + '/settings/projects/newBand' , headers = {"Authorization":token},
                     json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r['id'])

    
    
def newMap(name,  token, bands = [{'name':'red', 'number':1}, {'name':'green', 'number':2}, {'name':'blue', 'number':3}], visualizations= [{'name':'rgb', 'a':0,'b':255, 'c':1}], resolutionFromRaster = True, useMask=False, dataType = 'float32' , dryRun = True):
    if resolutionFromRaster:
        for i in np.arange(len(bands)):
            bands[i]['resolution'] = 0.008
            

    resolutions = []
    for i in np.arange(len(bands)):
        resolutions = resolutions + [bands[i]['resolution']]



    body = {'name':name, 'dataSource':bands, 'useMask':useMask , 'captures': [], 'visualizations':visualizations, 'active':False, 'dataType':dataType, 'resolutionFromRaster':resolutionFromRaster, 'dryRun':dryRun }

    r = s.post(url + '/settings/projects/newMap', headers = {"Authorization":token},
                     json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r['id'])


def newOrder(name, boundary, captures, token,  visualizations = ['rgb'],  dataSource = 'sentinel2RGBIR', model = None,  useMask=True, dryRun = True ):
    measurements = []
    boundary = gpd.GeoSeries([boundary]).__geo_interface__['features'][0]

    newCaptures = []
    for capture in captures:
        newCaptures = newCaptures + [{'startDate':capture['startDate'].strftime('%Y-%m-%d'),'endDate':capture['endDate'].strftime('%Y-%m-%d') }] 
    captures = newCaptures

    visuals = []
    for nameVisual in visualizations:
        visuals = visuals + [{'name':nameVisual}]

    r = s.get(url + '/settings/projects/options')
    r = r.json()
    minResolution = [ source['defaultZoom'] for source in r['dataSources'] if source['name'] == dataSource]
    if len(minResolution) == 0:
        ValueError('dataSource must be one of sentinel2, droneRGB, sentinel2RGBIR, sentinel1, spot, pleiades, spotTasking or pleiadesTasking')


    body = {'name':name, 'dataSource':{'name':dataSource}, 'useMask':useMask , 'captures': captures, 'visualizations':visuals, 'measurements':{'names':measurements, 'perClass':False}, 'active':True, 'dryRun':dryRun}

    body['bounds'] = boundary

    if str(type(model)) != str(type(None)):
        body['model']=model
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
    

def projectDescription(projectId, description, token):
    r = s.post(url + '/settings/organize/description', headers = {"Authorization":token},
                     json = {'mapId':projectId, 'description':description })
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    
###calculations

def runModel(mapId, timestamp, token, dryRun=True):
    body = {'mapId':mapId, 'timestamp':timestamp,'type':'model', 'dryRun':dryRun }
    print(body)
    r = s.post(url + '/settings/models/run', headers = {"Authorization":token},
                     json = body)


    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    if dryRun:
        r = r.json()
        return(r)
    
def aggregate(mapId, timestamp, token, dryRun = True):
    r = s.post(url + '/settings/model/run', headers = {"Authorization":token},
                     json = {'mapId':mapId, 'timestamp':timestamp,'type':'aggregation', 'dryRun':dryRun })


    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    if dryRun:
        r = r.json()
        return(r)


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
    percent = float(count)/float(total)*100
    sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent) + ' '*(100-int(percent)) + ']')

########################
    
