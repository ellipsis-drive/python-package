#https://packaging.python.org/tutorials/packaging-projects/

url = 'https://api.ellipsis-earth.com/v2'



import pandas as pd
from PIL import Image
import geopandas as gpd
import numpy as np
from io import BytesIO
from io import StringIO
import requests
import rasterio
import math
import threading
import multiprocessing
from shapely.geometry import Polygon
from shapely import geometry
from geopy.distance import geodesic



def logIn(username, password):
        r =requests.post(url + '/account/login/',
                         json = {'username':username, 'password':password} )
        if int(str(r).split('[')[1].split(']')[0]) != 200:
            raise ValueError(r.text)
            
        token = r.json()
        token = token['token']
        token = 'Bearer ' + token
        return(token)



def myMaps(token = None):
    if token == None:
        r = requests.get(url + '/account/mymaps')
    else:
        r = requests.get(url + '/account/mymaps', 
                     headers = {"Authorization":token} )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = r.json()
    return(r)

def getMapId(name, token = None):
    
    if token == None:
        r = requests.get(url + '/account/mymaps')        
    else:
        r = requests.get(url + '/account/mymaps', 
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
        r = requests.post(url + '/metadata',
                         json = {"mapId":  mapId, 'type':Type})
    else:
        r = requests.post(url + '/metadata', headers = {"Authorization":token},
                         json = {"mapId":  mapId, 'type':Type})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
            
    r = r.json()
    return(r)



def dataTimestamps(mapId, Type, element, dataType, className = None, token = None):
    if Type == 'custom_polygon':
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
    
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'element': element}
    if className != None:
        body['className'] = className

    if token == None:
        r = requests.post(url + '/data/timestamps',
                         json = body)
    else:
        r = requests.post(url + '/data/timestamps', headers = {"Authorization":token},
                         json = body)
        
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    r = pd.read_csv(StringIO(r.text))
    return(r)


def dataIds(mapId, Type, elementIds, dataType, timestampNumber, className = None, token = None):
        
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'timestampNumber': timestampNumber, 'elementIds': elementIds}
    if className != None:
        body['className'] = className
    if token == None:
        r = requests.post(url + '/data/ids',
                         json = body)
    else:
        r = requests.post(url + '/data/ids', headers = {"Authorization":token},
                         json = body)
        
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r = pd.read_csv(StringIO(r.text))
    return(r)


def dataTiles(mapId, Type, timestampNumber, element, dataType, className = None, token = None):
    if Type == 'custom_polygon':
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
    
    body = {'mapId':  mapId, 'dataType': dataType, 'type':Type, 'timestampNumber':timestampNumber , 'element': element}
    if className != None:
        body['className'] = className

    if token == None:
        r = requests.post(url + '/data/tiles',
                         json = body)
    else:
        r = requests.post(url + '/data/tiles', headers = {"Authorization":token},
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
        r = requests.post(url + '/geometry/ids',
                         json = body)    
    else:
        r = requests.post(url + '/geometry/ids', headers = {"Authorization":token},
                         json = body)    
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
        
    ids = r.json()
    return(ids)



def geometryGet(mapId, Type, elementIds, token = None):
    if token == None:
        r = requests.post(url + '/geometry/get', headers = {"Authorization":token},
                         json = {"mapId":  mapId, 'type':Type, 'elementIds':elementIds})
    else:
        r = requests.post(url + '/geometry/get',
                         json = {"mapId":  mapId, 'type':Type, 'elementIds':elementIds})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    r  = gpd.GeoDataFrame.from_features(r.json()['features'])
    return(r)


def geometryDelete(mapId, polygonId, token):
    r= requests.post(url + '/geometry/delete', headers = {"Authorization":token},
                     json = {"mapId":  mapId, 'polygonId':polygonId})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

def geometryAlter(mapId, polygonId, properties, newLayerName, token):
    r = requests.post(url + '/geometry/alter', headers = {"Authorization":token},
                     json = {"mapId":  mapId, 'polygonId':polygonId, 'newLayerName':newLayerName, 'properties':properties})
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


def geometryAdd(mapId, layer, geometry, token, properties = None):
    feature = gpd.GeoSeries([geometry]).__geo_interface__['features'][0]
    if properties != None:
        feature['properties'] = properties
    body = {"mapId":  mapId, 'layer': 'test',  'feature': feature}

    r = requests.post(url + '/geometry/add', headers = {"Authorization":token},
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
        r = requests.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = requests.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    ids = r.json()
    return(ids)
    
def geoMessageGet(mapId, Type, messageIds, token = None):    
    body = {'mapId':mapId, 'type':Type, 'messageIds':messageIds}
    if token == None:
        r = requests.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = requests.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    
    return( r.json())

def geoMessageAdd(mapId,Type, elementId,token, replyTo = None, message = None, private= None, form = None, image=None, x=None, y=None, timestamp = 0):    
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
        body['image'] = image
    if x != None:
        body['x'] = x
    if y != None:
        y['y'] = y
        
    r = requests.post(url + '/geomessage/ids', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    

def geoMessageDelete(mapId, Type, messageId, token):    
    body = {'mapId':mapId, 'type':Type, 'messageId':messageId}
    r = requests.post(url + '/geomessage/ids', headers = {"Authorization":token},
                 json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)
    


def geoMessageImage(mapId, Type, geoMessageId, token = None):
    body = {'mapId':mapId, 'type':Type, 'geoMessageId':geoMessageId}
    if token ==None:
        r = requests.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = requests.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    im = Image.open(BytesIO(r.content))    
    return(im)



def rasterGet(mapId, Type, element, channels, timestamp, token = None):
    if Type == 'custom_polygon':
        element = gpd.GeoSeries([element]).__geo_interface__['features'][0]
    
    body = {'mapId':mapId, 'type':Type, 'element':element, 'channels':channels, 'timestamp':timestamp}
    if token ==None:
        r = requests.post(url + '/geomessage/ids',
                     json = body )        
    else:
        r = requests.post(url + '/geomessage/ids', headers = {"Authorization":token},
                     json = body )
    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)

    im = Image.open(BytesIO(r.content))
    return(im)


def visualBounds(mapId, timestampMin, timestampMax, layerName, xMin,xMax,yMin, yMax , token = None):

    
    body = {'mapId':mapId, 'timestampMin':timestampMin, 'timestampMax':timestampMax, 'layerName':layerName, 'xMin':xMin, 'xMax':xMax, 'yMin':yMin, 'yMax':yMax}
    if token ==None:
        r = requests.post(url + '/visual/bounds',
                     json = body )        
    else:
        r = requests.post(url + '/visual/bounds', headers = {"Authorization":token},
                     json = body )

    if int(str(r).split('[')[1].split(']')[0]) != 200:
        raise ValueError(r.text)


    im = np.array(Image.open(BytesIO(r.content)))
    return(im)


##################################################################################################################



def plotPolys(polys, xmin,xmax,ymin,ymax, alpha = None, im = None, colors = [(0,0,1)] , column= None):
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
    
    transform = rasterio.transform.from_bounds(bbox.bounds['minx'], bbox.bounds['miny'], bbox.bounds['maxx'], bbox.bounds['maxy'], im.shape[0], im.shape[1])
    rasters = np.zeros(im.shape)
    for i in np.arange(len(colors)):
        sub_polys = polys.loc[polys[column] == i]
        raster = rasterio.features.rasterize( shapes = [ (sub_polys['geometry'].values[m], 1) for m in np.arange(sub_polys.shape[0]) ] , fill = 0, transform = transform, out_shape = (im.shape[0], im.shape[1]), all_touched = True )
        raster = np.stack([raster * colors[i][0], raster*colors[i][1],raster*colors[i][2], raster ], axis = 2)
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
    
    x1, y1, x2, y2  = area.bounds
         
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
    cover = [geometry.Polygon([ (coords['x1'].iloc[j] , coords['y1'].iloc[j]) , (coords['x2'].iloc[j] , coords['y1'].iloc[j]), (coords['x2'].iloc[j] , coords['y2'].iloc[j]), (coords['x1'].iloc[j] , coords['y2'].iloc[j]) ]) for j in np.arange(coords.shape[0])]
    
    coords = gpd.GeoDataFrame({'geometry': cover, 'x1':coords['x1'], 'x2':coords['x2'], 'y1':coords['y1'], 'y2':coords['y2'] })

    #remove all tiles that do not intersect the area that needed covering    
    keep = [area.intersects(coords['geometry'].values[j]) for j in np.arange(coords.shape[0])]
    coords = coords[pd.Series(keep, name = 'bools').values]
    coords['id'] = np.arange(coords.shape[0])
        
    return(coords)




#global queues
q_result = multiprocessing.Queue()
q_todo = multiprocessing.Queue()

def thread(request):
    s = requests.Session()
    while(q_todo.qsize()>0):
        args = q_todo.get()
        print(q_todo.qsize())
        key = list(args.keys())[0]
        args = args[key]
        args = (s,) + args
        r = request(*args)
        q_result.put({key:r})


def requestParallel(request, threads, argsDict):
    
    for key in argsDict.keys():
        q_todo.put({key:argsDict[key]})
    
    
    trs = list()
    for i in np.arange(threads):
        tr = threading.Thread(target = thread, args = (request,) )
        tr.start()
        trs.append(tr)
    
    for tr in trs:
        tr.join()
    
    result = dict()
    for j in np.arange(q_result.qsize()):
        new = q_result.get()
        key = list(new.keys())[0]
        value = new[key]
        result.update({key:value})
        
    return(result)



