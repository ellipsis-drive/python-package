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
import threading
import datetime
import multiprocessing
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from rasterio.features import rasterize
from geopy.distance import geodesic
import json
import cv2
import sys
from owslib.wfs import WebFeatureService
import fiona
from owslib.wms import WebMapService
import os
from requests_toolbelt import MultipartEncoder

import ellipsis.packages

__version__ = '1.1.11'
url = 'https://api.ellipsis-drive.com/v1'
#url = 'https://dev.api.ellipsis-earth.com/v2'
s = requests.Session()


def logIn(username, password):
        r =s.post(url + '/account/login/',
                         json = {'username':username, 'password':password} )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        token = r.json()
        token = token['token']
        token = 'Bearer ' + token
        return(token)



def myMaps(atlas = None,token = None):
    if token == None:
        r = s.get(url + '/account/mymaps')
    else:
        r = s.get(url + '/account/mymaps', 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = r.json()
    if not str(type(atlas)) == str(type(None)):
        r = [m for m in r if atlas in m['atlases']]
    
    return(r)


def myShapes(atlas = None,token = None):
    if token == None:
        r = s.get(url + '/account/myshapes')
    else:
        r = s.get(url + '/account/myshapes', 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = r.json()
    if not str(type(atlas)) == str(type(None)):
        r = [m for m in r if atlas in m['atlases']]
    
    return(r)


def getMapId(name, token = None):
    
    if token == None:
        r = s.get(url + '/account/mymaps')        
    else:
        r = s.get(url + '/account/mymaps', 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    mapId = [map['id'] for map in r.json() if map['name'] == name]
    if len(mapId)>0:
        mapId = mapId[0]
    else:
        raise ValueError('Map not found')

    return(mapId)

def getShapeId(name, token = None):
    
    if token == None:
        r = s.get(url + '/account/myshapes')        
    else:
        r = s.get(url + '/account/myshapes', 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    mapId = [map['id'] for map in r.json() if map['name'] == name]
    if len(mapId)>0:
        mapId = mapId[0]
    else:
        raise ValueError('Area not found')

    return(mapId)

    
def metadata(mapId, Type, token = None):
    if Type == 'captures':
        if token == None:
            r = s.get(url + '/account/mymaps')
        else:
            r = s.get(url + '/account/mymaps', headers = {"Authorization":token})
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        r = r.json()
        mapData = [mapData for mapData in r if mapData['id'] == mapId]
        if len(mapData)==0:
            raise ValueError('mapId not found')
        else:
            r = mapData[0]
            
        r = r['captures']
        for i in np.arange(len(r)):
            r[i]['startDate'] = datetime.datetime.strptime(r[i]['startDate'].split('T')[0],"%Y-%m-%d" )
            r[i]['endDate'] = datetime.datetime.strptime(r[i]['endDate'].split('T')[0],"%Y-%m-%d" )
        return(r)

    if Type == 'mapInfo':
        if token == None:
            r = s.get(url + '/account/mymaps')
        else:
            r = s.get(url + '/account/mymaps', headers = {"Authorization":token})
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        r = r.json()
        mapData = [mapData for mapData in r if mapData['id'] == mapId]
        if len(mapData)==0:
            raise ValueError('mapId not found')
        else:
            r = mapData[0]
    else:

        if token == None:
            r = s.post(url + '/metadata',
                             json = {"mapId":  mapId})
        else:
            r = s.post(url + '/metadata', headers = {"Authorization":token},
                             json = {"mapId":  mapId})
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r = r.json()
    
        if Type == 'classes':
            r = r['classes'][0]['classes']
        elif Type == 'measurements':
            r = r['measurements'][0]['measurements']
        elif Type == 'geometryLayers':
            r = r['polygonLayers']
        elif Type == 'bands':
            bands = r['bands']
            names = [band['name'] for band in bands]
            resolution = min([band['resolution'] for band in bands])
            measurements = r['measurements'][0]['measurements']
            N = len(bands)
            for m in measurements:
                if m['name'] not in names:
                    bands = bands + [{'id':m['id'],'name':m['name'], 'number':N, 'resolution':resolution}]
                    N = N +1
            r = bands
        elif Type == 'forms':
            r = r['forms']
        elif Type == 'mapLayers':
            r = r['mapLayers'][0]['layers']
        elif Type == 'timestamps':
            r = r['timestamps']
            for i in np.arange(len(r)):
                r[i]['dateFrom'] = datetime.datetime.strptime(r[i]['dateFrom'].split('T')[0],"%Y-%m-%d" )
                r[i]['dateTo'] = datetime.datetime.strptime(r[i]['dateTo'].split('T')[0],"%Y-%m-%d" )
        else:
            raise ValueError('Type must be either classes, measurements, geometryLayers, bands, forms, mapLayers, captures or timestamps')
        
    return(r)



def dataTimestamps(mapId, element, dataType, token = None, unit = 'km2'):
    
    className = 'all classes'
    if str(type(element)) == "<class 'str'>" or str(type(element)) == "<class 'numpy.int64'>":
        Type = 'polygon'
        element = element
    elif str(type(element)) ==  "<class 'dict'>":
        Type = 'tile'
        element['tileX'] = int(element['tileX'])
        element['tileY'] = int(element['tileY'])
        element['zoom'] = int(element['zoom'])
    else:
        Type = 'customPolygon'
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
            
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'element': element, 'className': className}
    body = json.dumps(body)
    body = json.loads(body)

    if token == None:
        r = s.post(url + '/data/timestamps',
                         json = body)
    else:
        r = s.post(url + '/data/timestamps', headers = {"Authorization":token},
                         json = body)
        
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = pd.read_csv(StringIO(r.text))
    
    if unit == 'ha':
        if dataType == 'class':
            columns = list( set(r.columns)  - set(['timestamp','date_from', 'date_to']) )
        else:
            columns = ['area']
        r[columns] = r[columns] * 100
    elif unit == 'm2':
        if dataType == 'class':
            columns = list( set(r.columns)  - set(['timestamp','date_from', 'date_to']) )
        else:
            columns = ['area']
        r[columns] = r[columns] * 1000000

    dates_start = []
    dates_end = []
    for i in np.arange(r.shape[0]):
        dates_end = dates_end + [datetime.datetime.strptime(r['date_from'].values[i],"%Y-%m-%d" )]
        dates_start = dates_start + [datetime.datetime.strptime(r['date_to'].values[i],"%Y-%m-%d" )]
    r['date_from'] = dates_start
    r['date_to'] = dates_end
    
    return(r)


def dataIds(mapId, elementIds, dataType, timestamp, token = None, wait = 0, unit = 'km2'):
    timestamp = int(timestamp)
    className = 'all classes'
    if len(elementIds) ==0:
            raise ValueError('elementIds has length 0')
    if str(type(elementIds[0])) == "<class 'str'>":
        Type = 'polygon'
    if str(type(elementIds[0])) ==  "<class 'dict'>":
        Type = 'tile'
        for i in np.arange(len(elementIds)):
            elementIds[i]['tileX'] = int(elementIds[i]['tileX'])
            elementIds[i]['tileY'] = int(elementIds[i]['tileY'])
            elementIds[i]['zoom'] = int(elementIds[i]['zoom'])
        
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'timestamp': timestamp, 'className':className}

    elementIds = list(elementIds)
    r_total = pd.DataFrame()
    chunks_ids = chunks(elementIds)
    
    for chunk_ids in chunks_ids:
        body['elementIds'] = chunk_ids
        if token == None:
            r = s.post(url + '/data/ids',
                             json = body)
        else:
            r = s.post(url + '/data/ids', headers = {"Authorization":token},
                             json = body)
            
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r = pd.read_csv(StringIO(r.text))
        r_total = r_total.append(r)
        loadingBar(r_total.shape[0], len(elementIds))


    if dataType == 'class':
        columns = list( set(r_total.columns)  - set(['id']) )
    else:
        columns = ['area']
        
    if unit == 'ha':
        r[columns] = r[columns] * 100
    elif unit == 'm2':
        r_total[columns] = r_total[columns] * 1000000
        
    return(r_total)


def dataTiles(mapId, timestamp, element, dataType, token = None, unit = 'km2'):
    timestamp = int(timestamp)
    className = 'all classes'
    if str(type(element)) == "<class 'str'>":
        Type = 'polygon'
    elif str(type(element)) ==  "<class 'dict'>":
        Type = 'tile'
        element['tileX'] = int(element['tileX'])
        element['tileY'] = int(element['tileY'])
        element['zoom'] = int(element['zoom'])
    else:
        Type = 'customPolygon'
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
    
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'timestamp':timestamp , 'element': element, 'className':className}
    body = json.dumps(body)
    body = json.loads(body)

    if token == None:
        r = s.post(url + '/data/tiles',
                         json = body)
    else:
        r = s.post(url + '/data/tiles', headers = {"Authorization":token},
                         json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    r = pd.read_csv(StringIO(r.text))

    if unit == 'ha':
        if dataType != 'class':
            columns = list( set(r.columns)  - set(['tileX', 'tileY', 'zoom']) )
        else:
            columns = ['area']
        r[columns] = r[columns] * 100
    elif unit == 'm2':
        if dataType != 'class':
            columns = list( set(r.columns)  - set(['tileX', 'tileY', 'zoom']) )
        else:
            columns = ['area']
        r[columns] = r[columns] * 1000000

    return(r)
    
def dataGeometry(mapId, geometry, dataType, timestamp=0, token = None):
    
    geometry =  gpd.GeoSeries([geometry]).__geo_interface__['features'][0]
    body = {"mapId": mapId, 'geometry':geometry['geometry'], 'timestamp':timestamp, 'type':dataType}

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


    

def getBounds(mapId, timestamp = 0, token = None ):
    body = {"mapId": mapId}

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
        
        
def geometryGet(mapId, layer, geometryIds = None, history = None, filters = None, limit = None, xMin = None, xMax = None, yMin=None, yMax=None, wait = 0, showLoadingBar = False, deleted = False, token = None):
    
    body = {"mapId":  mapId, 'layer':layer, 'deleted':deleted}
    
    if str(type(xMin)) != str(type(None)):
        body['bounds'] = {'xMin': float(xMin) , 'xMax':float(xMax), 'yMin':float(yMin), 'yMax':float(yMax)}
    if str(type(geometryIds)) != str(type(None)):
        body['geometryIds'] = geometryIds
    if str(type(filters)) != str(type(None)):
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
    if str(type(history)) != str(type(None)):
        if 'dateFrom' in history.keys():
                history[i]['dateFrom'] = history[i]['dateFrom'].strftime('%Y-%m-%d %H:%M:%S')
        if  'dateTo' in history.keys():
                history[i]['dateTo'] = history[i]['dateTo'].strftime('%Y-%m-%d %H:%M:%S') 
        body['history'] = history

    body = json.dumps(body)
    body = json.loads(body)

    if showLoadingBar:
        body['returnType'] = 'count'
        if token == None:
            r = s.post(url + '/geometry/get',
                             json = body)
        else:
            r = s.post(url + '/geometry/get', headers = {"Authorization":token},
                             json = body)
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r = r.json()
        totalCount = r['count']
        if totalCount == 0:
            sh = gpd.GeoDataFrame()
            sh.crs = {'init': 'epsg:4326'}
            return(sh)

    body['returnType'] = 'all'
    keepGoing = True

    sh = gpd.GeoDataFrame()
    while (keepGoing):

        if token == None:
            r = s.post(url + '/geometry/get',
                             json = body)
        else:
            r = s.post(url + '/geometry/get', headers = {"Authorization":token},
                             json = body)
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r = r.json()
        if len(r['result']['features']) ==0:
            keepGoing = False
        else:
            sh  = sh.append(gpd.GeoDataFrame.from_features(r['result']['features']))
            body['pageStart'] = r['nextPageStart']
            time.sleep(wait)
            
        if str(type(limit)) != str(type(None)) and sh.shape[0] > limit:
            sh = sh.iloc[0:limit]

        if showLoadingBar:
            loadingBar(sh.shape[0],totalCount)
            
    sh.crs = {'init': 'epsg:4326'}

    return(sh)


def getTiles(mapId, timestamp = 0, xMin = None, xMax = None, yMin=None, yMax=None, wait = 0, token = None, showLoadingBar = False):
    
    body = {"mapId":mapId, 'timestamp':int(timestamp)}
        
    if str(type(xMin)) != str(type(None)):
        body['bounds'] = {'Xmin': float(xMin) , 'xMax':float(xMax), 'yMin':float(yMin), 'yMax':float(yMax)}


    body = json.dumps(body)
    body = json.loads(body)


    if showLoadingBar:
        body['returnType'] = 'count'
        if token == None:
            r = s.post(url + '/geometry/tiles',
                             json = body)
        else:
            r = s.post(url + '/geometry/tiles', headers = {"Authorization":token},
                             json = body)
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r = r.json()
        totalCount = r['count']

        
    body['returnType'] = 'geometry'


    keepGoing = True

    sh = gpd.GeoDataFrame()
    while (keepGoing):

        if token == None:
            r = s.post(url + '/geometry/tiles',
                             json = body)
        else:
            r = s.post(url + '/geometry/tiles', headers = {"Authorization":token},
                             json = body)
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        
        r = r.json()
        if len(r['result']['features']) ==0:
            keepGoing = False
        else:
            sh  = sh.append(gpd.GeoDataFrame.from_features(r['result']['features']))
            body['pageStart'] = r['nextPageStart']
            time.sleep(wait)

        if showLoadingBar:
            loadingBar(sh.shape[0],totalCount)
   
    sh.crs = {'init': 'epsg:4326'}

    return(sh)
        

def geometryVersions(mapId, geometryId, token = None):
    body = {"mapId":  mapId, 'polygonId':geometryId}
    if token == None:
        r = s.post(url + '/geometry/iversions',
                         json = body)    
    else:
        r = s.post(url + '/geometry/versions', headers = {"Authorization":token},
                         json = body)    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    versions = r.json()

    sh = gpd.GeoDataFrame()
    for version in versions:
        body = {"mapId":  mapId, 'elementIds':[geometryId], 'type':'polygon', 'version':version['version']}
        if token == None:
            r = s.post(url + '/geometry/get',
                             json = body)    
        else:
            r = s.post(url + '/geometry/get', headers = {"Authorization":token},
                             json = body)    
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
        r  = gpd.GeoDataFrame.from_features(r.json()['features'])
        r['version'] = version['version']
        r['creationDate'] = version['editDate']
        r['creationUser'] = version['editUser']
        sh = sh.append(r)
    sh.crs = {'init': 'epsg:4326'}
    return(sh)

    


def geometryDelete(mapId, polygonId, token, revert= False):
    body = {"mapId":  mapId, 'rever':revert}

    body['polygonId'] = int(polygonId)
    r= s.post(url + '/geometry/delete', headers = {"Authorization":token},
                     json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def geometryAlter(mapId, geometryId, token, newProperties = {}, removeProperties = [], newGeometry = None, removeAllProperties = False):
    body = {"mapId":  mapId}

    polygonId = int(geometryId)
    body['polygonId'] = polygonId


    geometry = geometryGet(mapId = mapId, elementIds = [polygonId], token  = token)
    columns = set(geometry.columns) - set(['geometry', 'id', 'layer', 'user'])
    columns = list(columns - set(removeProperties))

    properties = {}
    if not removeAllProperties:
        for column in columns:
            properties[column] = geometry[column].values[0]
    
        for key in newProperties.keys():
            properties[key] =newProperties[key]

    
    keys = properties.keys()
    for key in keys:
        try:
            properties[key] = float(properties[key])
            if int(properties[key]) == float(properties[key]):
                properties[key] = int(properties[key])
            if math.isnan(properties[key]):
                properties[key] = 'NaN'
        except:
            properties[key] = str(properties[key])
    body['newProperties'] = properties            

    if str(type(newGeometry)) != str(type(None)):
        body['newGeometry'] = gpd.GeoSeries([newGeometry]).__geo_interface__['features'][0]
    
    r = s.post(url + '/geometry/alter', headers = {"Authorization":token},
                     json = {"mapId":  mapId, 'polygonId':polygonId, 'newProperties':properties})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def geometryMove(mapId, geometryIds, newLayer, token):
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

def geometryAdd(mapId, layer, features, token):

    if not str(type(features)) ==  "<class 'geopandas.geodataframe.GeoDataFrame'>":
        raise ValueError('features must be of type geopandas dataframe')

    features = features.to_crs({'init': 'epsg:4326'})

    property_names = list(set(features.columns) - set(['geometry']))

    features_json = []
    print('preparing geometries')

    for i in np.arange(features.shape[0]):

        properties = {}
        for property_name in property_names:
            try:
                properties[property_name] = float(features[property_name].values[i])
                if int(properties[property_name]) == float(properties[property_name]):
                    properties[property_name] = int(properties[property_name])
                if math.isnan(properties[property_name]):
                    properties[property_name] = 'NaN'
            except:
                properties[property_name] = str(features[property_name].values[i])


        feature = gpd.GeoSeries([features['geometry'].values[i]]).__geo_interface__['features'][0]
        feature['properties'] = properties
        
        features_json = features_json + [feature]
        
        loadingBar(i+1,features.shape[0])

    features_chunks = chunks(features_json)

    i = 0
    print('')
    print('uploading geometries')
    addedIds = []
    for features in features_chunks:
        body = {"mapId":  mapId, "layer":layer, "features":features}
        
        body = json.dumps(body)
        body = json.loads(body)
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
        addedIds = addedIds + r.json()['ids']
        loadingBar(i*3000 + len(features),len(features_chunks))
        i = i+1
        
    return(addedIds)

        
def messageIds( mapId, filters = None, limit = None, token = None):
    Type = 'polygon'
    body = {'mapId':mapId, 'type':Type}
    if limit != None:
        limit = int(limit)
        body['limit'] = limit
    if filters != None:
        body['filters'] = filters
    

    if token == None:
        r = s.post(url + '/message/ids',
                     json = body )        
    else:
        r = s.post(url + '/message/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    ids = r.json()
    return(ids)
    
def messageGet(mapId, messageIds, token = None):
    Type = 'polygon'

    body = {'mapId':mapId, 'type':Type, 'messageIds':messageIds}
    if token == None:
        r = s.post(url + '/message/get',
                     json = body )        
    else:
        r = s.post(url + '/message/get', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    return( r.json())

def messageAdd(mapId, elementId,token, replyTo = None, message = None, private= None, form = None, image=None, lon=None, lat=None, timestamp = 0): 
    
    Type = 'polygon'
    elementId = int(elementId)


    body = {'mapId':mapId, 'type':Type, 'elementId':elementId, 'timestamp':timestamp}
    if str(type(lon)) != "<class 'NoneType'>":
        lon = float(lon)
    if str(type(lat)) != "<class 'NoneType'>":
        lat = float(lat)
    if str(type(replyTo)) != "<class 'NoneType'>":
        body['replyTo'] = replyTo
    if str(type(message)) != "<class 'NoneType'>":
        body['message'] = message
    if str(type(private)) != "<class 'NoneType'>":
        body['private'] = private
    if str(type(form)) != "<class 'NoneType'>":
        body['form'] = form
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
    

def messageDelete(mapId, messageId, token):    
    Type = 'polygon'
    body = {'mapId':mapId, 'type':Type, 'messageId':messageId}
    r = s.post(url + '/message/delete', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    


def messageImage(mapId, geoMessageId, token = None):
    Type = 'polygon'

    body = {'mapId':mapId, 'type':Type, 'geoMessageId':geoMessageId}
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



def rasterRaw(mapId, timestamp, Type = 'imagery', tileId = None, xMin = None, xMax = None, yMin = None, yMax = None, geometry = None , wait = 0, token = None):

    if Type not in ['imagery','classification']:
        raise ValueError('Type must be either imagery or classification')

    dtype = 'int8'
    layer = 'labelRaw'
    if Type == 'imagery':
        dtype = 'float32'
        layer = 'raw'

    timestamp = int(timestamp)
    if str(type(tileId)) !=  "<class 'NoneType'>":
        tileId['tileX'] = int(tileId['tileX'])
        tileId['tileY'] = int(tileId['tileY'])
        tileId['zoom'] = int(tileId['zoom'])
        body = {'mapId':mapId, 'tileId':tileId , 'layer':layer, 'timestamp':timestamp}

        if token ==None:
            r = s.post(url + '/raster/get',
                         json = body )
        else:
            r = s.post(url + '/raster/get', headers = {"Authorization":token},
                         json = body )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
    
        r = r.json()
        crs = r['crs']
        bounds = r['bounds']
        r_total = np.array(r['data'], dtype = dtype)
        trans = rasterio.transform.from_bounds(bounds['x1'], bounds['y1'], bounds['x2'], bounds['y2'], r_total.shape[1], r_total.shape[0])
    else:
            num_bands = 1
            if Type == 'imagery':
                bands = metadata(mapId, 'bands')
                num_bands = len(bands)
                bandNames = [band['name'] for band in bands]
                transparent_band = bandNames.index('transparent')


            if str(type(geometry)) != str(type(None)):
              xMin,yMin,xMax,yMax = geometry.bounds  
            elif str(type(xMin)) == "<class 'NoneType'>" or str(type(xMax)) == "<class 'NoneType'>" or str(type(yMin)) == "<class 'NoneType'>" or str(type(yMax)) == "<class 'NoneType'>" :
                    raise ValueError('Either bounding box coordinates or tileId is required')

            xMin = float(xMin)
            xMax = float(xMax)
            yMin = float(yMin)
            yMax = float(yMax)

            timestamp = int(timestamp)
            if token == None:
               zoom = int(metadata(mapId, 'mapInfo')['zoom'])
            else:
               zoom = int(metadata(mapId, 'mapInfo', token = token)['zoom'])               

            
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
                    time.sleep(wait)
                    x_index = tileX - min_x_osm
                    y_index = tileY - min_y_osm
                    tileId = {'tileX':int(tileX), 'tileY':int(tileY),'zoom':int(zoom)}
                    body = {'mapId':mapId, 'tileId':tileId , 'layer':layer, 'timestamp':timestamp}
                    retries = 0
                    while retries <= 10:
                        try:

                            if token ==None:
                                r = s.post(url + '/raster/tile',
                                             json = body, timeout = 10 )        
                            else:
                                r = s.post(url + '/raster/tile', headers = {"Authorization":token},
                                             json = body, timeout = 10 )
                            retries = 11
                        except Exception as e:
                            if retries == 10:
                                raise ValueError(e)
                            retries = retries + 1
                            time.sleep(1)


                    if int(str(r).split('[')[1].split(']')[0]) != 200:
                        if r.json()['message'] == 'tile does not exist':
                            r = np.zeros((256,256,num_bands))
                        else:
                            raise ValueError(r.text)
                    else:
                        r = r.json()
                        r = np.array(r['data'])
                    r_total[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ] = r
                    loadingBar(x_index + y_index*len(x_tiles) + 1,len(x_tiles)*len(y_tiles))
                
                
            min_x_index = int(round((min_x_osm_precise - min_x_osm)*256))
            max_x_index = int(round((max_x_osm_precise- min_x_osm)*256))
            min_y_index = int(round((min_y_osm_precise - min_y_osm)*256))
            max_y_index = int(round((max_y_osm_precise- min_y_osm)*256))
            
            r_total = r_total[min_y_index:max_y_index,min_x_index:max_x_index,:]

            xMin,yMin =  transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMin, yMin)
            xMax,yMax = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMax, yMax)
 
            trans = rasterio.transform.from_bounds(xMin, yMin, xMax, yMax, r_total.shape[1], r_total.shape[0])
            crs = "EPSG:3857"
            bounds = {"xMin":xMin,"xMax":xMax,"yMin":yMin,"yMax":yMax} 

            if str(type(geometry)) != str(type(None)):
                shape = gpd.GeoDataFrame({'geometry':[geometry]})
                shape.crs = {'init': 'epsg:4326'}
                shape = shape.to_crs({'init': 'epsg:3857'})
                raster_shape = rasterize( shapes = [ (shape['geometry'].values[m], 1) for m in np.arange(shape.shape[0]) ] , fill = 0, transform = trans, out_shape = (r_total.shape[0], r_total.shape[1]), all_touched = True )
                if Type == 'imagery':
                    r_total[:,:,transparent_band] = np.minimum(r_total[:,:,transparent_band], raster_shape)
                else:
                    r_total = np.stack([r_total, raster_shape])


    return({'data':r_total, 'crs':crs, 'bounds':bounds, 'transform':trans})


def rasterVisual(mapId, timestampMin, timestampMax, layerName, xMin= None,xMax= None,yMin=None, yMax=None , tileId=None, downsampled = False, wait = 0, token = None):

    if timestampMin > timestampMax:
        raise ValueError('timestampMax must be greater or equal to timestampMin')
    if token != None:
        token_inurl = token.replace('Bearer ', '')
    if str(type(tileId)) == "<class 'dict'>":
        tileX = int(tileId['tileX'])
        tileY = int(tileId['tileY'])
        zoom = int(tileId['zoom'])
        location = 'https://api.ellipsis-earth.com/v2/tileService/' + mapId
        im = np.zeros((256,256,4), dtype = 'uint8')
        timestamps = list(np.arange(timestampMin, timestampMax +1))
        timestamps.reverse()
        for timestamp in timestamps:
           if token == None:
                r = s.get(location + '/'  + str(timestamp) + '/'  + layerName + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY))
           else:
                r = s.get( url = location + '/'  + str(timestamp) + '/'  + layerName + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY) + '?token=' + token_inurl)

           if int(str(r).split('[')[1].split(']')[0]) != 200:
                raise ValueError(r.text)
           else:
               im_new = np.array(Image.open(BytesIO(r.content)), dtype = 'uint8')

           im[im[:,:,3] == 0,:] = im_new[im[:,:,3] == 0,:]
           
           y1 = (2* math.atan( math.e**(math.pi - (tileY) * 2*math.pi / 2**zoom) ) - math.pi/2) * 360/ (2* math.pi)
           y2 = (2* math.atan( math.e**(math.pi - (tileY+1) * 2*math.pi / 2**zoom) ) - math.pi/2) * 360/ (2* math.pi)
           x1 = tileX * 360/2**zoom - 180 
           x2 = (tileX +1) * 360/2**zoom - 180
           x1,y1 =  transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), x1, y1)
           x2,y2 = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), x2, y2)
           trans = rasterio.transform.from_bounds(x1, y1, x2, y2, im.shape[1], im.shape[0])
           result = {'data':im, 'crs':'EPSG:3857', 'bounds':{'xMin':x1, 'xMax':x2,'yMin':y1, 'yMax':y2}, 'transform':trans}
           
    elif str(type(xMin)) == "<class 'NoneType'>" or str(type(xMax)) == "<class 'NoneType'>" or str(type(yMin)) == "<class 'NoneType'>" or str(type(yMax)) == "<class 'NoneType'>" :
            raise ValueError('Either bounding box coordinates or tileId is required')
    elif downsampled:
        xMin = float(xMin)
        xMax = float(xMax)
        yMin = float(yMin)
        yMax = float(yMax)

        first = True
        for timestamp in np.arange(timestampMin, timestampMax+1):        
            body = {'mapId':mapId, 'timestamp':int(timestamp), 'layer':layerName, 'bounds':{'xMin':float(xMin), 'xMax':float(xMax), 'yMin':float(yMin), 'yMax':float(yMax) } } 
            if token ==None:
                r = s.post(url + '/raster/bounds',
                             json = body )        
            else:
                r = s.post(url + '/raster/bounds', headers = {"Authorization":token},
                             json = body )
        
            if int(str(r).split('[')[1].split(']')[0]) != 200:
                raise ValueError(r.text)
            r = r.json()
            r = r['data']
            r = np.array(r)
            if first:
                im = r
                first = False
            else:
                im = np.maximum(im, r)

        x1,y1 =  transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMin, yMin)
        x2,y2 = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMax, yMax)
        trans = rasterio.transform.from_bounds(x1, y1, x2, y2, im.shape[1], im.shape[0])
        result = {'data':im, 'crs':'EPSG:3857', 'bounds':{'xMin':x1, 'xMax':x2,'yMin':y1, 'yMax':y2}, 'transform':trans}


    else:
            xMin = float(xMin)
            xMax = float(xMax)
            yMin = float(yMin)
            yMax = float(yMax)
            location = 'https://api.ellipsis-drive.com/v1/tileService/' + mapId

            if token == None:
               zoom = int(metadata(mapId, 'mapInfo')['zoom'])
            else:
               zoom = int(metadata(mapId, 'mapInfo', token = token)['zoom'])               
            
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


            r_total = np.zeros((256*(max_y_osm - min_y_osm + 1) ,256*(max_x_osm - min_x_osm + 1),4), dtype = 'uint8')
            timestamps = list(np.arange(timestampMin, timestampMax +1))
            timestamps.reverse()

            for tileY in y_tiles:
                for tileX in x_tiles:
                    time.sleep(wait)
                    x_index = tileX - min_x_osm
                    y_index = tileY - min_y_osm

                    im = np.zeros((256,256,4))
                    for timestamp in timestamps:
                       retries = 0
                       while retries <= 10:
                            try:
                               if token == None:
                                    r = s.get(location + '/'  + str(timestamp) + '/'  + layerName + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY))
                               else:
                                    r = s.get( url = location + '/'  + str(timestamp) + '/'  + layerName + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY) + '?token=' + token_inurl)
                               retries = 11
                            except Exception as e:
                                if retries == 10:
                                    raise ValueError(e)
                                retries = retries + 1
                                time.sleep(1)
                            

                       if int(str(r).split('[')[1].split(']')[0]) == 404:
                           im_new = np.zeros((256,256,4))
                       elif int(str(r).split('[')[1].split(']')[0]) != 200:
                            raise ValueError(r.text)
                       else:
                            im_new = np.array(Image.open(BytesIO(r.content)))
                       im[im[:,:,3] == 0,:] = im_new[im[:,:,3] == 0,:]
                    r_total[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256, : ] = im

                    loadingBar(x_index + y_index*len(x_tiles) + 1,len(x_tiles)*len(y_tiles))
                                        
                        
            min_x_index = int(round((min_x_osm_precise - min_x_osm)*256))
            max_x_index = int(round((max_x_osm_precise- min_x_osm)*256))
            min_y_index = int(round((min_y_osm_precise - min_y_osm)*256))
            max_y_index = int(round((max_y_osm_precise- min_y_osm)*256))
            
            im = r_total[min_y_index:max_y_index,min_x_index:max_x_index,:]

            x1,y1 =  transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMin, yMin)
            x2,y2 = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMax, yMax)
            trans = rasterio.transform.from_bounds(x1, y1, x2, y2, im.shape[1], im.shape[0])
            result = {'data':im, 'crs':'EPSG:3857', 'bounds':{'xMin':x1, 'xMax':x2,'yMin':y1, 'yMax':y2}, 'transform':trans}

    
    return(result)
    
def rasterSubmit(mapId, r,  timestamp, token, xMin = None, xMax = None, yMin = None, yMax= None, tileId = None, mask = None):
    if str(type(tileId)) == "<class 'dict'>":
            tileX = int(tileId['tileX'])
            tileY = int(tileId['tileY'])
            zoom = int(tileId['zoom'])
            
            body = {'mapId':mapId, 'tileId':{'tileX':tileX, 'tileY':tileY, 'zoom':zoom}, 'timestamp':timestamp, 'type':'label', 'newLabel': r[:,:].tolist(), 'store':False }
            
            body = json.dumps(body)
            body = json.loads(body)

            reply = s.post(url + '/raster/submit', headers = {"Authorization":token},
                         json = body )
            if int(str(reply).split('[')[1].split(']')[0]) != 200:
                raise ValueError(reply.text)
    elif str(type(xMin)) == "<class 'NoneType'>" or str(type(xMax)) == "<class 'NoneType'>" or str(type(yMin)) == "<class 'NoneType'>" or str(type(yMax)) == "<class 'NoneType'>" :
            raise ValueError('Either bounding box coordinates or tileId is required')
    else:
        xMin = float(xMin)
        xMax = float(xMax)
        yMin = float(yMin)
        yMax = float(yMax)
        
        zoom = int(metadata(mapId, 'mapInfo', token = token)['zoom'])               
        
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
        
                
        min_pixy =  round((min_y_osm_precise - min_y_osm)*256)
        max_pixy = round((max_y_osm_precise - min_y_osm)*256)
        min_pixx = round((min_x_osm_precise - min_x_osm)*256)
        max_pixx = round((max_x_osm_precise - min_x_osm)*256)
        
        max_pixx = min(max_pixx, max_x_osm * 256 - 1)
        max_pixy = min(max_pixy, max_y_osm * 256 - 1)

        r = [ cv2.resize(r[:,:,i], dsize=(max_pixx - min_pixx,max_pixy - min_pixy), interpolation=cv2.INTER_NEAREST) for i in np.arange(r.shape[-1])]        
        r = np.stack(r, axis = -1)

        r_new = np.zeros(( (max_y_osm - min_y_osm+1)*256, (max_x_osm - min_x_osm+1)*256 ))


        
        r_new[ min_pixy : max_pixy , min_pixx : max_pixx , :] = r
        
        r = r_new
        del r_new
        
        for tileX in x_tiles:
            for tileY in y_tiles:
                x_index = tileX - min_x_osm
                y_index = tileY - min_y_osm
                
                loadingBar(x_index * len(y_tiles) + y_index+1,len(x_tiles)* len(y_tiles))
                
                r_sub = r[y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256]
                
                body = {'mapId':mapId, 'tileId':{'tileX':int(tileX), 'tileY':int(tileY), 'zoom':int(zoom)}, 'timestamp':int(timestamp), 'type':'label', 'newLabel': r_sub[:,:].tolist(), 'store': False }

                body = json.dumps(body)
                body = json.loads(body)
                    
                if token ==None:
                    reply = s.post(url + '/raster/submit',
                                 json = body )        
                else:
                    reply = s.post(url + '/raster/submit', headers = {"Authorization":token},
                                 json = body )
                if int(str(reply).split('[')[1].split(']')[0]) != 200:
                    raise ValueError(reply.text)
                


def seriesAdd(mapId, geometryId, data, token, includeDatetime = True):
    if not 'datetime' in data.columns and includeDatetime:
        raise ValueError('Dataframe has no datetime column. In case you wish to upload data without a date and time use includeDatetime = False. In this case the server will add the current datetime as datetime')

    if 'datetime' in data.columns:
            data['date'] = data['datetime']
            del data['datetime']


            if str(data['date'].dtypes) == 'datetime64[ns]':
                data['date'] = data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
               raise  ValueError('datetime column must be of type datetime')

    for c in data.columns:
        if c != 'date':
            data[c] = data[c].astype(float)
        

    values = []
    for i in np.arange(data.shape[0]):
        for c in data.columns:
            if c != 'date':
                if 'date' in data.columns:
                    values = values + [{'property':c, 'value':data[c].values[i], 'date':data['date'].values[i]}]
                else:
                    values = values + [{'property':c, 'value':data[c].values[i]}]                    

    chunks_values = chunks(values)
    N = 0
    for values_sub in chunks_values:
        r = s.post(url + '/series/add', headers = {"Authorization":token},
                     json = {"mapId":  mapId, "values":values_sub, 'geometryId':geometryId})
        
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)

        loadingBar(N*3000 + len(values_sub), len(values))
        N = N+1


def seriesDelete(mapId, geometryId, token, user = None, dateFrom = None, dateTo = None, revert = False):
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
    
    r = s.post(url + '/series/delete', headers = {"Authorization":token},
                 json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def seriesGet(mapId, geometryId, dateFrom = None, dateTo = None, user=None, includeDeleted = False, token  = None):
    body = {'mapId':mapId, 'geometryId':geometryId, 'includeDeleted':includeDeleted}
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

    if token ==None:
        r = s.post(url + '/series/get',
                     json = body )        
    else:
        r = s.post(url + '/series/get', headers = {"Authorization":token},
                     json = body )

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    r = pd.read_csv(StringIO(r.text))
    r['date'] = pd.to_datetime(r['date'], format="%Y-%m-%d %H:%M:%S")
    return(r)

def seriesAggregated(mapId, geometryIds, aggregation = 'mean',  dateFrom = None, dateTo = None, user=None, token = None):
    body = {'mapId':mapId, 'geometryIds':geometryIds, 'aggregation' : aggregation}
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
    r = r.json()
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


def uploadRasterFile(mapId, captureId, file_path, file, token, epsg = None):
    body = {"mapId":  mapId, 'captureId':captureId, 'fileName':file}
    if str(type(epsg)) != str(type(None)):
        body['epsg'] = int(epsg)
    r = s.post(url + '/files/raster/initUpload', headers = {"Authorization":token},
                     json = body)
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    
    uploadId = r['id']
    
    if not os.path.exists(os.path.join(file_path , file)):
            raise ValueError(os.path.join(file_path , file) + ' not found')
    
    
    conn_file = open(os.path.join(file_path , file), 'rb')
    payload = MultipartEncoder({'upload': (file, conn_file, 'application/octet-stream')})
    
    r = s.post(url + '/files/raster/upload/' + uploadId, headers = {"Authorization":token, "Content-Type": payload.content_type}, data=payload)
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    conn_file.close()


def addGeometryLayer(mapId, layerName, token, color = "fcba03", private=False, restricted = False):
    r = s.post(url + '/settings/geometryLayers/add', headers = {"Authorization":token},
                 json = {"mapId":  mapId, "color":color, "private":private, "restricted":restricted, "layerName":layerName, "properties":[] })

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def deleteGeometryLayer(mapId, layerName, token):
    r = s.post(url + '/settings/geometryLayers/delete', headers = {"Authorization":token},
                 json = {"mapId":  mapId, "layerName":layerName })

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

        
def uploadGeometryFile(mapId, layerName, file_path, file, fileFormat, token, epsg=None):

    body = {"mapId":  mapId, 'layer':layerName, 'fileName':file, 'format':fileFormat}
    if str(type(epsg)) != str(type(None)):
        body['epsg'] = int(epsg)


    r = s.post(url + '/files/geometry/initUpload', headers = {"Authorization":token},
                     json = body)
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    
    uploadId = r['id']
    
    if not os.path.exists(os.path.join(file_path , file)):
            raise ValueError(os.path.join(file_path , file) + ' not found')
    
    
    conn_file = open(os.path.join(file_path , file), 'rb')
    payload = MultipartEncoder({'upload': (file, conn_file, 'application/octet-stream')})
    
    r = s.post(url + '/files/geometry/upload/' + uploadId, headers = {"Authorization":token, "Content-Type": payload.content_type}, data=payload)
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    conn_file.close()
        
    
############################new projects
def newShape(name, boundary, token, dryRun = True):
    boundary = gpd.GeoSeries([boundary]).__geo_interface__['features'][0]


    r = s.post(url + '/settings/projects/newShape', headers = {"Authorization":token},
                     json = {"name":  name, 'geoJson':boundary, 'dryRun':dryRun})
    
    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r)
    
def newMap(name,  token, shapeName = None, bands = [{'name':'red', 'number':1}, {'name':'green', 'number':2}, {'name':'blue', 'number':3}], visualizations= [{'name':'rgb', 'a':0,'b':0, 'c':1}], aggregationPixels = 256, model = None, fitToRaster = True, boundary = None, resolutionFromRaster = True, useMask=False, dataType = 'float32' , dryRun = True):
    if resolutionFromRaster:
        for i in np.arange(len(bands)):
            bands[i]['resolution'] = 0.008

    if fitToRaster:
        boundary = Polygon( [(-180,-90),(-180,90),(180,90),(180,-90),(-180,-90)])

    resolutions = []
    for i in np.arange(len(bands)):
        resolutions = resolutions + [bands[i]['resolution']]
    minResolution = min(resolutions)
    if not aggregationPixels in [16,32,64,128,256]:
        raise ValueError('aggregationPixels must be one of 16,32,64,128 or 256')
    aggregationZoomPossible = math.floor(math.log(40000000 / (minResolution * 1.4 * 256)) / math.log(2) + 1)
    aggregationZoom = aggregationZoomPossible + math.floor((256/aggregationPixels)) -1

    boundary = gpd.GeoSeries([boundary]).__geo_interface__['features'][0]
    measurements = {'name':[], 'perClass':False}
    body = {'name':name, 'dataSource':bands, 'useMask':useMask , 'captures': [], 'aggregationZoom':aggregationZoom, 'visualizations':visualizations, 'measurements':measurements, 'active':False, 'dataType':dataType, 'fitToRaster':fitToRaster, 'resolutionFromRaster':resolutionFromRaster, 'dryRun':dryRun }
    if str(type(model)) != str(type(None)):
        body['model'] = model
    if str(type(shapeName)) != str(type(None)):
        body['area'] = shapeName
    r = s.post(url + '/settings/projects/newMap', headers = {"Authorization":token},
                     json = body)

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r)





def newOrder(name, boundary, captures, token, shapeName,  visualizations = ['rgb'], measurements = ['ndvi'],  dataSource = 'sentinel2RGBIR', aggregationPixels = 256, model = None,  useMask=True, dryRun = True ):

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
    minResolution = minResolution[0]
    if not aggregationPixels in [16,32,64,128,256]:
        raise ValueError('aggregationPixels must be one of 16,32,64,128 or 256')
    aggregationZoom = minResolution + math.floor((256/aggregationPixels)) -1

    body = {'name':name, 'dataSource':{'name':dataSource}, 'useMask':useMask , 'captures': captures, 'aggregationZoom':aggregationZoom, 'visualizations':visuals, 'measurements':{'names':measurements, 'perClass':False}, 'active':True, 'dryRun':dryRun}
    print(body)

    if str(type(shapeName)) != str(type(None)):
        body['area'] = shapeName
    else:
        body['area'] = boundary
    if str(type(model)) != str(type(None)):
        body['model']=model
    r = s.post(url + '/settings/projects/newMap', headers = {"Authorization":token},
                     json = body)


    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = r.json()
    return(r)


def runModel(mapId, timestamp, token, dryRun=True):
    r = s.post(url + '/settings/model/run', headers = {"Authorization":token},
                     json = {'mapId':mapId, 'timestamp':timestamp,'type':'model', 'dryRun':dryRun })


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
    
    

def parallel(function, args, callsPerMinute, retries=0):
       
    
    q_result = multiprocessing.Queue()
    q_todo = multiprocessing.Queue()

    for i in np.arange(len(args)):
        q_todo.put({'args':args[i], 'key':i})


    def single_request(function):
        args_new = q_todo.get()
        while args_new != 'done_and_exit':
            retried = 0
            while retried <= retries:
                key = args_new['key']
                args_new = args_new['args']
                try:
                    r = function(*args_new)
                    retried = retries + 1
                except Exception as e:
                    if retried == retries:
                        raise ValueError(e)
                    retried = retried + 1
                    time.sleep(1)

            q_result.put({'result':r, 'key':key})
            args_new = q_todo.get()
            if args_new != 'done_and_exit':
                time.sleep(60)
                

    trs = []
    for n in np.arange(callsPerMinute):
        time.sleep(60/callsPerMinute)
        tr = threading.Thread(target = single_request, args = (function,) )
        trs = trs + [tr]
        tr.start()
        
    while q_result.qsize() != len(args):
        time.sleep(1)
        loadingBar(q_result.qsize(),len(args))


    for n in np.arange(callsPerMinute):
        q_todo.put('done_and_exit')
    
    for tr in trs:
        tr.join()
    
    print('joining results')
    
    result = [1 for j in np.arange(q_result.qsize())]
    for j in np.arange(q_result.qsize()):
        new = q_result.get()
        key = new['key']
        value = new['result']
        result[key] = value
        
    return(result)




def tilesCover(zoom, area = None, xMin= None, xMax = None,yMin = None, yMax = None ):

    def cover(area, zoom):
        x1, y1, x2, y2  = area.bounds
    
        #find the x osm tiles involved   
        x1_osm =  math.floor((x1 +180 ) * 2**zoom / 360 )
        x2_osm =  math.floor( (x2 +180 ) * 2**zoom / 360 +1)
        y2_osm = math.floor( 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + y1/360 * math.pi  ) ) ) + 1)
        y1_osm = math.floor( 2**zoom / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + y2/360 * math.pi  ) ) ))
        
        parts_x =  (x2_osm - x1_osm) + 1
        xosm_vec = [i for i in range(x1_osm, x2_osm + 1) ]
        parts_y = y2_osm - y1_osm + 1
        yosm_vec = [i for i in range(y1_osm, y2_osm + 1) ]
    
        #calculate the boundingbox coordinates of the tiles
        x1_vec = [ i * 360/2**zoom - 180  for i in np.arange( x1_osm, x2_osm +1 )  ]
        x2_vec = [i * 360/2**zoom - 180 for i in np.arange( x1_osm +1, x2_osm+2 )  ]
    
        y2_vec = [ (2* math.atan( math.e**(math.pi - (i) * 2*math.pi / 2**zoom) ) - math.pi/2) * 360/ (2* math.pi)     for i in np.arange(y1_osm, y2_osm+1) ]
        y1_vec = [ (2* math.atan( math.e**(math.pi - (i) * 2*math.pi / 2**zoom) ) - math.pi/2) * 360/ (2* math.pi)     for i in np.arange(y1_osm+1, y2_osm +2) ]
    
        #make a dataframe out of these boundingbox coordinates
        coords = pd.DataFrame()
        for n in np.arange( parts_y ):
           y1_sq = np.repeat(y1_vec[n], parts_x )
           y2_sq = np.repeat(y2_vec[n], parts_x )
           x1_sq = x1_vec
           x2_sq = x2_vec
           yosm_sq = np.repeat(yosm_vec[n], parts_x)
           xosm_sq = xosm_vec
           coords_temp = {'x1': x1_sq, 'x2': x2_sq, 'y1': y1_sq, 'y2':y2_sq, 'x_osm': xosm_sq, 'y_osm': yosm_sq }
           coords = coords.append(pd.DataFrame(coords_temp))
    
        #make a geopandas out of this dataframe    
        covering = []
        for i in np.arange(coords.shape[0]):
            covering.append(Polygon([ (coords['x1'].iloc[i] , coords['y1'].iloc[i]), (coords['x2'].iloc[i], coords['y1'].iloc[i]), (coords['x2'].iloc[i], coords['y2'].iloc[i]), (coords['x1'].iloc[i], coords['y2'].iloc[i])]))
        covering = MultiPolygon(covering)    
        
        coords = gpd.GeoDataFrame({'geometry': covering, 'tileX': coords['x_osm'].values, 'tileY':coords['y_osm'].values})
    
        #remove all tiles that do not intersect with the orgingal area    
        keep = [area.intersects(covering[j]) for j in np.arange(len(covering))]    
        coords = coords[pd.Series(keep, name = 'bools').values]
        
        
        return(coords)

    
    if str(type(area)) == str(type(None)):
        geometry = Polygon( [(xMin,yMin), (xMin, yMax), (xMax,yMax), (xMax,yMin)])
        area = gpd.GeoDataFrame({'geometry':[geometry]})

    
    total_covering = gpd.GeoDataFrame()
    if str(type(area)) == "<class 'shapely.geometry.polygon.Polygon'>" or str(type(area)) == "<class 'shapely.geometry.line.Line'>" or str(type(area)) == "<class 'shapely.geometry.point.Point'>":
        areas = [area]
    else:
        areas = area

    for area in areas:
        covering = cover( area, zoom )
        covering['zoom'] = zoom
        total_covering = total_covering.append(covering)

    total_covering['id'] = np.arange(total_covering.shape[0])
    total_covering = total_covering.drop_duplicates(['tileX', 'tileY'])
    
    total_covering.crs = {'init': 'epsg:4326'}

    return(total_covering)






def cover(w, area = None, xMin= None, xMax = None, yMin = None, yMax = None):
    def UTMcover(area,  w,v, hemisphere):
        
        if len(area) == 0:
            return(gpd.GeoDataFrame())
        
        x1, y1, x2, y2  = area.bounds
             
        #calculate the y1 and y2 of all squares
        if hemisphere == 'north':
            step_y =  v/geodesic((y1,x1), (y1 - 1,x1)).meters
            parts_y = math.floor((y2 - y1)/ step_y + 1)
            
            y1_vec = y1 + np.arange(0, parts_y )*step_y
            y2_vec = y1 + np.arange(1, parts_y +1 )*step_y
            
            if x1 < 179:
                steps_x = [   w/geodesic((y,x1), (y,x1+1)).meters for y in y1_vec  ]
            else:
                steps_x = [   w/geodesic((y,x1), (y,x1-1)).meters for y in y1_vec  ]            
            parts_x = [math.floor( (x2-x1) /step +1 ) for step in steps_x ]      
        if hemisphere == 'south':
            step_y =  v/geodesic((y1,x1), (y1 + 1,x1)).meters        
            parts_y = math.floor((y2 - y1)/ step_y + 1)
            
            y2_vec = y2 - np.arange(0, parts_y )*step_y
            y1_vec = y2 - np.arange(1, parts_y +1 )*step_y
            
            if x1<179:
                steps_x = [   w/geodesic((y,x1), (y,x1+1)).meters for y in y2_vec  ]
            else:
                steps_x = [   w/geodesic((y,x1), (y,x1-1)).meters for y in y2_vec  ]            
            parts_x = [math.floor( (x2-x1) /step +1 ) for step in steps_x ]      
            
    
        coords = pd.DataFrame()
        for n in np.arange(len(parts_x)):
            x1_sq = [ x1 + j*steps_x[n] for j in np.arange(0,parts_x[n]) ]
            x2_sq = [ x1 + j*steps_x[n] for j in np.arange(1, parts_x[n]+1) ]
            coords_temp = {'x1': x1_sq, 'x2': x2_sq, 'y1': y1_vec[n], 'y2':y2_vec[n]}
            coords = coords.append(pd.DataFrame(coords_temp))
        
        #make a geopandas of this covering dataframe
        cover = [Polygon([ (coords['x1'].iloc[j] , coords['y1'].iloc[j]) , (coords['x2'].iloc[j] , coords['y1'].iloc[j]), (coords['x2'].iloc[j] , coords['y2'].iloc[j]), (coords['x1'].iloc[j] , coords['y2'].iloc[j]) ]) for j in np.arange(coords.shape[0])]
        
        coords = gpd.GeoDataFrame({'geometry': cover, 'x1':coords['x1'], 'x2':coords['x2'], 'y1':coords['y1'], 'y2':coords['y2'] })
        
        #remove all tiles that do not intersect the area that needed covering    
        keep = [area.intersects(coords['geometry'].values[j]) for j in np.arange(coords.shape[0])]
        coords = coords[pd.Series(keep, name = 'bools').values]
        coords['id'] = np.arange(coords.shape[0])
        
        return(coords)

    total_covering = gpd.GeoDataFrame()

    if str(type(area)) == "<class 'shapely.geometry.polygon.Polygon'>" or str(type(area)) == "<class 'shapely.geometry.line.Line'>" or str(type(area)) == "<class 'shapely.geometry.point.Point'>":
        areas = [area]
    else:
        areas = area


    for area in areas:
    
        #convert to multipolygon in case of a polygon
        if str(type(area)) == "<class 'shapely.geometry.polygon.Polygon'>":
            area = MultiPolygon([area])
    
        #split the area in a western and eastern halve 
        south = Polygon([ (-180, -90), (180,-90), (180,0), (-180,0)])
        north = Polygon([ (-180, 90), (180,90), (180,0), (-180,0)])
        southern = MultiPolygon([poly.difference(north) for poly in area ])
        northern = MultiPolygon([poly.difference(south) for poly in area])
    
        #cover the area with tiles
        covering = gpd.GeoDataFrame()
        covering = covering.append(UTMcover(area = southern, w=w,v=w, hemisphere = 'south' ))
        covering = covering.append(UTMcover( area = northern, w =w,v=w, hemisphere ='north'))
               
        total_covering = total_covering.append(covering)        

    total_covering['id'] = np.arange(total_covering.shape[0])
    total_covering.crs = {'init': 'epsg:4326'}

    return(total_covering)
    
    
def loadingBar(count,total):
    percent = float(count)/float(total)*100
    sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent) + ' '*(100-int(percent)) + ']')

########################
    

def openGeometryLayers(layer, xMin, xMax, yMin, yMax):
    
    if layer == 'brp':
        url = 'https://geodata.nationaalgeoregister.nl/brpgewaspercelen/wfs'
        name =  'brpgewaspercelen:brpgewaspercelen'
        version = '1.1.0' 
        crs = {'init': 'epsg:28992'}
    elif layer == 'NAP':
        url = 'https://geodata.nationaalgeoregister.nl/napinfo/wfs'
        name =  'napinfo:nappeilmerken'
        version = '1.1.0' 
        crs = {'init': 'epsg:28992'}
    elif layer == 'kadasterBebouwing':
        url = 'https://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0'
        name =  'kadastralekaartv4:bebouwing'
        version = '1.1.0' 
        crs = {'init': 'epsg:28992'}
    elif layer == 'kadasterPercelen':
        url = 'https://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0'
        name =  'kadastralekaartv4:perceel'
        version = '1.1.0' 
        crs = {'init': 'epsg:28992'}
    elif layer == 'kadasterGrenzen':
        url = 'https://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0'
        name =  'kadastralekaartv4:kadastralegrens'
        version = '1.1.0' 
        crs = {'init': 'epsg:28992'}
    else:
        raise ValueError("layer must be 'brp', 'NAP', 'kadasterGrenzen', 'kadasterPercelen' or 'kadasterBebouwing'")

    wfs = WebFeatureService(url = url,  version=version)    
    #list(wfs.contents)
    bbox = gpd.GeoDataFrame( {'geometry': [Polygon([(xMin,yMin), (xMax, yMin), (xMax, yMax), (xMin, yMax)])]} )
    bbox.crs = {'init': 'epsg:4326'}
    bbox = bbox.to_crs(crs)
    xMin = bbox.bounds['minx'].values[0]
    xMax = bbox.bounds['maxx'].values[0]
    yMin = bbox.bounds['miny'].values[0]
    yMax = bbox.bounds['maxy'].values[0]
    bbox=(xMin,yMin,xMax,yMax)
    
    response = wfs.getfeature(typename=name, bbox=bbox)
    
    string = response.read()
    if str(type(string)) == "<class 'bytes'>":
        b = string
    else:
        b = bytes(string, 'UTF-8')
    
    try:    
        with fiona.BytesCollection(b) as f:
            crs = f.crs
            sh = gpd.GeoDataFrame.from_features(f, crs=crs)
    except:
        sh = gpd.GeoDataFrame()
        
    sh = sh.to_crs({'init': 'epsg:4326'})

    return(sh)    

def openMapLayers(layer, xMin, xMax, yMin, yMax, w,h):
    if layer == 'luchtfoto2019':
       layer =  '2019_ortho25'
       url = 'https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?'
    elif layer == 'luchtfoto2018':
       layer =  '2018_ortho25'
       url = 'https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?'
    elif layer == 'luchtfoto2017':
       layer =  '2019_ortho25'
       url = 'https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?'
    elif layer == 'luchtfoto2016':
       layer =  '2019_ortho25'
       url = 'https://geodata.nationaalgeoregister.nl/luchtfoto/rgb/wms?'
    elif layer == 'USTopo':
         url = 'https://basemap.nationalmap.gov:443/arcgis/services/USGSTopo/MapServer/WmsServer?'
         layer = '0'
    elif layer == 'USHydro':
        url = 'https://basemap.nationalmap.gov:443/arcgis/services/USGSHydroCached/MapServer/WmsServer?'
        layer = '0'
    elif layer == 'USHillshade':
        url = 'https://basemap.nationalmap.gov:443/arcgis/services/USGSShadedReliefOnly/MapServer/WmsServer?'
        layer = '0'
    else:
        raise ValueError("layer must be 'luchtfotos2016', 'luchtfotos2017', 'luchtfotos2018', 'luchtfotos2019', 'USHydro', 'USHillshade' or 'USTopo'")

    wms = WebMapService(url)
    bbox = gpd.GeoDataFrame( {'geometry': [Polygon([(xMin,yMin), (xMax, yMin), (xMax, yMax), (xMin, yMax)])]} )
    bbox=(xMin,yMin,xMax,yMax)

    img = wms.getmap(layers = [layer], srs = 'EPSG:4326', bbox = bbox , size = (w,h), format= 'image/jpeg')

    img = Image.open(BytesIO(img.read()))
    
    img = np.asarray(img)
