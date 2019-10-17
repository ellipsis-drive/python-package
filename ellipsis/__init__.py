#https://packaging.python.org/tutorials/packaging-projects/
#https://truveris.github.io/articles/configuring-pypirc/

import pandas as pd
import matplotlib.image as mpimg
from PIL import Image
import geopandas as gpd
import base64
import numpy as np
from io import BytesIO
from io import StringIO
import time
import requests
import rasterio
import math
import threading
import multiprocessing
from shapely.geometry import Polygon
from rasterio.features import rasterize
from geopy.distance import geodesic

__version__ = '0.1.5'
url = 'https://api.ellipsis-earth.com/v2'
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



def myMaps(token = None):
    if token == None:
        r = s.get(url + '/account/mymaps')
    else:
        r = s.get(url + '/account/mymaps', 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = r.json()
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

    
    
def metadata(mapId, Type, token = None):

    if token == None:
        r = s.post(url + '/metadata',
                         json = {"mapId":  mapId, 'type':Type})
    else:
        r = s.post(url + '/metadata', headers = {"Authorization":token},
                         json = {"mapId":  mapId, 'type':Type})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
            
    r = r.json()
    return(r)



def dataTimestamps(mapId, element, dataType, className = 'all classes', token = None):
    
    if str(type(element)) == "<class 'int'>":
        Type = 'polygon'
    if str(type(element)) ==  "<class 'dict'>":
        Type = 'tile'
    if str(type(element)) == "<class 'shapely.geometry.polygon.Polygon'>":
        Type = 'custom_polygon'
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
            
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'element': element, 'className': className}

    if token == None:
        r = s.post(url + '/data/timestamps',
                         json = body)
    else:
        r = s.post(url + '/data/timestamps', headers = {"Authorization":token},
                         json = body)
        
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = pd.read_csv(StringIO(r.text))
    return(r)


def dataIds(mapId, elementIds, dataType, timestampNumber, className = 'all classes', token = None):
    if len(elementIds) ==0:
            raise ValueError('elementIds has length 0')
    if str(type(elementIds[0])) == "<class 'int'>":
        Type = 'polygon'
    if str(type(elementIds[0])) ==  "<class 'dict'>":
        Type = 'tile'
        
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'timestampNumber': timestampNumber, 'elementIds': elementIds, 'className':className}
    if token == None:
        r = s.post(url + '/data/ids',
                         json = body)
    else:
        r = s.post(url + '/data/ids', headers = {"Authorization":token},
                         json = body)
        
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = pd.read_csv(StringIO(r.text))
    return(r)


def dataTiles(mapId, timestampNumber, element, dataType, className = 'all classes', token = None):

    if str(type(element)) == "<class 'int'>":
        Type = 'polygon'
    if str(type(element)) ==  "<class 'dict'>":
        Type = 'tile'
    if str(type(element)) == "<class 'shapely.geometry.polygon.Polygon'>":
        Type = 'custom_polygon'
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
    
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'timestampNumber':timestampNumber , 'element': element, 'className':className}

    if token == None:
        r = s.post(url + '/data/tiles',
                         json = body)
    else:
        r = s.post(url + '/data/tiles', headers = {"Authorization":token},
                         json = body)
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    r = pd.read_csv(StringIO(r.text))
    return(r)



def geometryIds(mapId, Type,limit = None, layer = None, xMin = None, xMax = None, yMin=None, yMax=None,  token = None):

    body = {"mapId":  mapId, 'type': Type}

    if xMin != None:
        body['xMin'] = xMin
    if xMax != None:
        body['xMax'] = xMax
    if yMin != None:
        body['yMin'] = yMin
    if yMax != None:
        body['yMax'] = yMax
    if layer != None:
        body['layer'] = layer
    if limit != None:
        body['limit'] = layer
            
    if token == None:
        r = s.post(url + '/geometry/ids',
                         json = body)    
    else:
        r = s.post(url + '/geometry/ids', headers = {"Authorization":token},
                         json = body)    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    ids = r.json()
    return(ids)



def geometryGet(mapId, elementIds, token = None):
    
    if len(elementIds) ==0:
            raise ValueError('elementIds has length 0')
    if str(type(elementIds[0])) == "<class 'int'>":
        Type = 'polygon'
    if str(type(elementIds[0])) ==  "<class 'dict'>":
        Type = 'tile'

    if token == None:
        r = s.post(url + '/geometry/get', headers = {"Authorization":token},
                         json = {"mapId":  mapId, 'type':Type, 'elementIds':elementIds})
    else:
        r = s.post(url + '/geometry/get',
                         json = {"mapId":  mapId, 'type':Type, 'elementIds':elementIds})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r  = gpd.GeoDataFrame.from_features(r.json()['features'])
    return(r)


def geometryDelete(mapId, polygonId, token):
    r= s.post(url + '/geometry/delete', headers = {"Authorization":token},
                     json = {"mapId":  mapId, 'polygonId':polygonId})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def geometryAlter(mapId, polygonId, properties, newLayerName, token):
    r = s.post(url + '/geometry/alter', headers = {"Authorization":token},
                     json = {"mapId":  mapId, 'polygonId':polygonId, 'newLayerName':newLayerName, 'properties':properties})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def geometryAdd(mapId, layer, feature, token, properties = None):
    feature = gpd.GeoSeries([feature]).__geo_interface__['features'][0]
    if properties != None:
        feature['properties'] = properties
    body = {"mapId":  mapId, 'layer': 'test',  'feature': feature}

    r = s.post(url + '/geometry/add', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
def geoMessageIds( mapId, Type, filters = None, limit = None, token = None):
    
    body = {'mapId':mapId, 'type':Type}
    if limit != None:
        body['limit'] = limit
    if filters != None:
        body['filters'] = filters
    

    if token == None:
        r = s.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = s.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    ids = r.json()
    return(ids)
    
def geoMessageGet(mapId, Type, messageIds, token = None):    

    body = {'mapId':mapId, 'type':Type, 'messageIds':messageIds}
    if token == None:
        r = s.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = s.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    return( r.json())

def geoMessageAdd(mapId, elementId,token, replyTo = None, message = None, private= None, form = None, image=None, lon=None, lat=None, timestamp = 0):    

    if str(type(elementId)) == "<class 'int'>":
        Type = 'polygon'
    if str(type(elementId)) ==  "<class 'dict'>":
        Type = 'tile'


    body = {'mapId':mapId, 'type':Type, 'elementId':elementId, 'timestamp':timestamp}
    if replyTo != None:
        body['replyTo'] = replyTo
    if message != None:
        body['message'] = message
    if private != None:
        body['private'] = private
    if form != None:
        body['form'] = form
    if image != None:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = str(base64.b64encode(buffered.getvalue()))
        img_str = 'data:image/jpeg;base64,' + img_str[2:-1]
        body['image'] = img_str
    if lon != None:
        body['x'] = lon
    if lat != None:
        body['y'] = lat
        
    r = s.post(url + '/geomessage/add', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    

def geoMessageDelete(mapId, Type, messageId, token):    
    body = {'mapId':mapId, 'type':Type, 'messageId':messageId}
    r = s.post(url + '/geomessage/delete', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    


def geoMessageImage(mapId, Type, geoMessageId, token = None):
    body = {'mapId':mapId, 'type':Type, 'geoMessageId':geoMessageId}
    if token ==None:
        r = s.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = s.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    im = Image.open(BytesIO(r.content))    
    return(im)



def rasterGet(mapId, element, channels, timestamp, token = None):


    if str(type(element)) ==  "<class 'dict'>":
        Type = 'tile'
    if str(type(element)) == "<class 'shapely.geometry.polygon.Polygon'>":
        Type = 'custom_polygon'
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
    
    body = {'mapId':mapId, 'type':Type, 'element':element, 'channels':channels, 'timestamp':timestamp}
    if token ==None:
        r = s.post(url + '/raster/get',
                     json = body )        
    else:
        r = s.post(url + '/raster/get', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    r = r.json()
    crs = r['projection']
    bounds = r['bounds']
    r = np.array(r['data'])
    transform = rasterio.transform.from_bounds(bounds['x1'], bounds['y1'], bounds['x2'], bounds['y2'], r.shape[1], r.shape[0])

    return({'data':r, 'crs':crs, 'bounds':bounds, 'transform':transform})


def visualBounds(mapId, timestampMin, timestampMax, layerName, xMin,xMax,yMin, yMax , token = None):

    
    body = {'mapId':mapId, 'timestampMin':timestampMin, 'timestampMax':timestampMax, 'layerName':layerName, 'xMin':xMin, 'xMax':xMax, 'yMin':yMin, 'yMax':yMax}
    if token ==None:
        r = s.post(url + '/visual/bounds',
                     json = body )        
    else:
        r = s.post(url + '/visual/bounds', headers = {"Authorization":token},
                     json = body )

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


    im = np.array(Image.open(BytesIO(r.content)))
    return(im)

def visualTile(mapId, tileId, zoom, timestampNumber, layer, token= None):
    tileX = tileId['tileX']
    tileY = tileId['tileY']
    zoom = tileId['zoom']
    location = 'https://api.ellipsis-earth.com/v2/tileService/' + mapId
    if token == None:
        r = s.get(location + '/'  + str(timestampNumber) + '/'  + layer + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY))
    else:
        r = s.get(headers = {"Authorization":token}, url = location + '/'  + str(timestampNumber) + '/'  + layer + '/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY))
        

    r = np.array( mpimg.imread(BytesIO(r.content)))
    return(r)

    
    
##################################################################################################################

def plotPolys(polys, xmin,xmax,ymin,ymax, alpha = None, im = None, colors = {0:(0,0,1)} , column= None):
    polys.crs = {'init': 'epsg:4326'}
    polys = polys.to_crs({'init': 'epsg:3785'})
    
    bbox = gpd.GeoDataFrame( {'geometry': [Polygon([(xmin,ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)])]} )
    bbox.crs = {'init': 'epsg:4326'}
    bbox = bbox.to_crs({'init': 'epsg:3785'})

    if str(type(im)) == "<class 'NoneType'>":
        im = np.zeros((1024,1024,4))
    if column == None:
        column = 'extra'
        polys[column] = 0
    
    transform = rasterio.transform.from_bounds(bbox.bounds['minx'], bbox.bounds['miny'], bbox.bounds['maxx'], bbox.bounds['maxy'], im.shape[1], im.shape[0])
    rasters = np.zeros(im.shape)
    for key in colors.keys():
        sub_polys = polys.loc[polys[column] == key]
        if sub_polys.shape[0] >0:
            raster = rasterize( shapes = [ (sub_polys['geometry'].values[m], 1) for m in np.arange(sub_polys.shape[0]) ] , fill = 0, transform = transform, out_shape = (im.shape[0], im.shape[1]), all_touched = True )
            raster = np.stack([raster * colors[key][0], raster*colors[key][1],raster*colors[key][2], raster ], axis = 2)
            rasters = np.add(rasters, raster)
     
    rasters = np.clip(rasters, 0,1)
    if alpha == None:
        image = rasters
        image[image[:,:,3] == 0, :] = im [image[:,:,3] == 0, :]
    else:
        image = im * (1 - alpha) + rasters*alpha 
    return(image)


def chunks(l, n = 3000):
    result = list()
    for i in range(0, len(l), n):
        result.append(l[i:i+n])
    return(result)



def cover(area,  w):
    
    if len(area) == 0:
        return(gpd.GeoDataFrame())
    
    x1 = area.bounds['minx'].min()
    x2 = area.bounds['maxx'].max()
    y1 = area.bounds['miny'].min()
    y2 = area.bounds['maxy'].max()
         
    #calculate the y1 and y2 of all squares
    step_y =  w/geodesic((y1,x1), (y1 + 1,x1)).meters
    
    parts_y = math.floor((y2 - y1)/ step_y + 1)
    
    y1_vec = y1 + np.arange(0, parts_y )*step_y
    y2_vec = y1 + np.arange(1, parts_y +1 )*step_y
    
    #make a dataframe of these bounding boxes
    steps_x = [    w/geodesic((y,x1), (y,x1+1)).meters  for y in y1_vec  ]
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
    coords = coords[keep]
    coords['id'] = np.arange(coords.shape[0])
        
    return(coords)




#global queues

def parallel(function, args, per_minute):
       
    
    q_result = multiprocessing.Queue()
    q_todo = multiprocessing.Queue()

    for i in np.arange(len(args)):
        q_todo.put({'args':args[i], 'key':i})


    def single_request(function, wait):
        time.sleep(wait)
        while q_todo.qsize() > 0:
            args_new = q_todo.get()
            key = args_new['key']
            args_new = args_new['args']
            r = function(*args_new)
            q_result.put({'result':r, 'key':key})
            if q_todo.qsize() > 0:
                time.sleep(60)

    trs = []
    for n in np.arange(per_minute):
        wait = 60/per_minute * n
        tr = threading.Thread(target = single_request, args = (function, wait) )
        trs = trs + [tr]
        tr.start()
        
    for tr in trs:
        tr.join()
    
    
    result = [1 for j in np.arange(q_result.qsize())]
    for j in np.arange(q_result.qsize()):
        new = q_result.get()
        key = new['key']
        value = new['result']
        result[key] = value
        
    return(result)



