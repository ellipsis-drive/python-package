from ellipsis import sanitize
from ellipsis.util.root import getActualExtent
from ellipsis import apiManager
from ellipsis.util import loadingBar
from ellipsis.util.root import reprojectRaster
from ellipsis.path.raster.timestamp.util import constructImage
from ellipsis.path.raster.timestamp.util import cutOfTilesPerZoom

from rasterio.io import MemoryFile
from skimage.transform import resize
import json
import numpy as np
from io import BytesIO
import rasterio
import math
import tifffile
from PIL import Image
import geopandas as gpd
import datetime
import pandas as pd
import time
import requests
from skimage.measure import find_contours
from shapely.geometry import Point, LineString

def getDownsampledRaster(pathId, timestampId, extent, width, height, epsg=3857, style = None, token = None):
    return getSampledRaster(pathId, timestampId, extent, width, height, epsg, style, token)

def getSampledRaster(pathId, timestampId, extent, width, height, epsg=4326, style = None, token = None):
    bounds = extent
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, True)
    style = sanitize.validObject('style', style, False)
    epsg = sanitize.validInt('epsg', epsg, True)
    body = {'pathId':pathId, 'timestampId':timestampId, 'extent':bounds, 'width':width, 'height':height, 'style':style, 'epsg':epsg}

    if str(type(style)) == str(type(None)):
        body['applyStyle'] = False

    r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/rasterByExtent', body, token, crash = True, parseJson = False)


    if type(style) == type(None):
        r = tifffile.imread(BytesIO(r.content))
    else:
        r = np.array(Image.open(BytesIO(r.content)))
    #tif also has bands in last channel
    r = np.transpose(r, [2,0,1])

    xMin = bounds['xMin']
    yMin = bounds['yMin']
    xMax = bounds['xMax']
    yMax = bounds['yMax']



    trans = rasterio.transform.from_bounds(xMin, yMin, xMax, yMax, r.shape[2], r.shape[1])

    return {'raster': r, 'transform':trans, 'extent': {'xMin' : xMin, 'yMin': yMin, 'xMax': xMax, 'yMax': yMax}, 'crs':"EPSG:" + str(epsg) }


def contour(pathId, timestampId, extent, interval = None, intervals = None, epsg = 4326, bandNumber = 1, token = None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, False)
    epsg = sanitize.validInt('epsg', epsg, True)
    extent = sanitize.validBounds('extent', extent, True)


    res = getActualExtent(extent['xMin'], extent['xMax'], extent['yMin'], extent['yMax'], 'EPSG:' + str(epsg))    
    if res['status'] == '400':
        raise ValueError('Invalid epsg and extent combination')
        
    bounds = res['message']

    xMinWeb = bounds['xMin']
    yMinWeb = bounds['yMin']
    xMaxWeb = bounds['xMax']
    yMaxWeb = bounds['yMax']

    extentWeb = {'xMin': xMinWeb, 'xMax':xMaxWeb, 'yMin':yMinWeb, 'yMax':yMaxWeb}
    size = 1000
    r = getSampledRaster(pathId = pathId, timestampId = timestampId, extent = extentWeb, width = size, height = size, epsg=3857, token = token)
    raster = r['raster']
    
    if bandNumber >= raster.shape[0]:
        raise ValueError('BandNumber too high. Raster only has ' + str(raster.shape[0]) + 'bands.')


    
    if type(intervals) == type(None):
        minVal = np.min(raster[bandNumber-1, raster[-1,:,:] == 1])
        maxVal = np.max(raster[bandNumber-1, raster[-1,:,:] == 1])
        
        
        cont = minVal + interval

        conts = []
        while cont < maxVal:
            conts = conts + [cont]
            cont = cont + interval
    else:
        conts = intervals

    
    Lx = (xMaxWeb - xMinWeb)/size
    Ly = (yMaxWeb - yMinWeb)/size

    sh_total = []
    for cont in conts:
        
        lines = find_contours(raster[bandNumber-1,:,:],  mask=raster[-1,:,:] == 1, level = cont)
         
        newLines = []
        line = lines[0]
        for line in lines:
            newLine = LineString([ Point( xMinWeb + x[0] * Lx  , yMinWeb +  x[1] * Ly )  for x in line])
            newLines = newLines + [newLine]
        
        sh = gpd.GeoDataFrame({'geometry': newLines, 'label': (np.repeat(cont, len(newLines)))} )        
        
        sh_total = sh_total + [sh]
    
    sh = pd.concat(sh_total)
    sh.crs = 'EPSG:3857'
    sh = sh.to_crs('EPSG:' + str(epsg))

    return sh


def getValuesAlongLine(pathId, timestampId, line, token = None, epsg = 4326):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, False)
    line = sanitize.validShapely('line', line, True)
    epsg = sanitize.validInt('epsg', epsg, True)

    if line.type != 'LineString':
        raise ValueError('line must be a shapely lineString')

    temp = gpd.GeoDataFrame({'geometry':[line]})
    temp.crs = 'EPSG:' + str(epsg)
    temp = temp.to_crs('EPSG:3857')
    line = temp['geometry'].values[0]
    line = list(line.coords)
        
    x_of_line = [p[0] for p in line]
    y_of_line = [p[1] for p in line]

    #the first action is to cacluate a bounding box for the raster we need to retrieve
    xMin = min(x_of_line)
    xMax = max(x_of_line)
    yMin = min(y_of_line)
    yMax = max(y_of_line)
    
    d = (xMax - xMin) * 0.1
    xMax = xMax + d
    xMin = xMin -d
    d = (yMax - yMin) * 0.1
    yMax = yMax + d
    yMin = yMin -d
    
    
    
    #now we retrieve the needed raster we use epsg = 4326 but we can use other coordinates as well
    extent = {'xMin': xMin, 'xMax':xMax, 'yMin':yMin, 'yMax':yMax}

    size = 1000
    r = getSampledRaster(pathId = pathId, timestampId = timestampId, extent = extent, width = size, height = size, epsg=3857, token = token)
    raster = r['raster']

    memfile =  MemoryFile()
    dataset = memfile.open( driver='GTiff', dtype='float32', height=size, width=size, count = raster.shape[0], crs= r['crs'], transform=r['transform'])
    dataset.write(raster)



    values = list(dataset.sample(line))

    memfile.close()
    return values

def getLocationInfo(pathId, timestampId, locations, epsg = 4326, token= None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, False)
    epsg = sanitize.validInt('epsg', epsg, True)
    body = {'locations':locations,'epsg':epsg}
    r = apiManager.post('/path/' + pathId + '/raster/timestamp/' + timestampId + '/location', body, token)
    return r

    
def getRaster(pathId, timestampId, extent, token = None, showProgress = True, epsg = 4326, reproject = False, threads = None, style = None):
    bounds = extent
    
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, True)
    showProgress = sanitize.validBool('showProgress', showProgress, True)
    reproject = sanitize.validBool('reproject', reproject, True)
    
    if type(threads)!= type(None):
        Warning('The parameter threads is deprecated')
    if type(style)!= type(None):
        Warning('The parameter style is deprecated')
        
    xMin = bounds['xMin']
    yMin = bounds['yMin']
    xMax = bounds['xMax']
    yMax = bounds['yMax']

    res = getActualExtent(xMin, xMax, yMin, yMax, 'EPSG:' + str(epsg))
    if res['status'] == '400':
        raise ValueError('Invalid epsg and extent combination')
        
    bounds = res['message']

    xMinWeb = bounds['xMin']
    yMinWeb = bounds['yMin']
    xMaxWeb = bounds['xMax']
    yMaxWeb = bounds['yMax']
    
    info = apiManager.get('/path/' + pathId, None, token)
    bands =  info['raster']['bands']
    as_jpg = info['raster']['asJpg']
    num_bands = len(bands)
    dtype = info['raster']['format']

    timestamps =  info['raster']['timestamps']
    all_timestamps = [item['id'] for item in timestamps]
    if not timestampId in all_timestamps:
        raise ValueError('given timestamp does not exist')
    
    t = next(item for item in timestamps if item["id"] == timestampId)

    if t['status'] != 'active':
        raise ValueError('timestamp is not active, please active timestamp before making queries to it')

    zoom = t['zoom']

    body = {"applyStyle":False}

    LEN = 2.003751e+07

    x_start = 2**zoom * (xMinWeb + LEN) / (2* LEN)
    x_end = 2**zoom * (xMaxWeb + LEN) / (2* LEN)
    y_end = 2**zoom * (LEN - yMinWeb) / (2* LEN)
    y_start = 2**zoom * (LEN - yMaxWeb) / (2* LEN)

    x1_osm = math.floor(x_start)
    x2_osm = math.floor(x_end)
    y1_osm = math.floor(y_start)
    y2_osm = math.floor(y_end)
    tarred = False
    
    #dit is voor testing beide moeten op false staan
    forceTar = False
    skipTar = False
    
    N=0
    w = 256
    if not skipTar and ((x2_osm - x1_osm) * (y2_osm - y1_osm) > 50 or forceTar):
        tarZoom = next(item for item in timestamps if item["id"] == timestampId)['tarZoom']
            
        if type(tarZoom) != type(None):
            N = zoom - tarZoom

            w = 256*2**N
            tarred = True
            zoom = tarZoom
            x_start = 2**zoom * (xMinWeb + LEN) / (2* LEN)
            x_end = 2**zoom * (xMaxWeb + LEN) / (2* LEN)
            y_end = 2**zoom * (LEN - yMinWeb) / (2* LEN)
            y_start = 2**zoom * (LEN - yMaxWeb) / (2* LEN)
        
            x1_osm = math.floor(x_start)
            x2_osm = math.floor(x_end)
            y1_osm = math.floor(y_start)
            y2_osm = math.floor(y_end)
            
    x_tiles = np.arange(x1_osm, x2_osm+1)
    y_tiles = np.arange(y1_osm, y2_osm +1)

    r_total = np.zeros((num_bands, w*(y2_osm - y1_osm + 1) ,w*(x2_osm - x1_osm + 1)), dtype = dtype)
    
    tiles = []            
    for tileY in y_tiles:
        for tileX in x_tiles:
            tiles = tiles + [(tileX, tileY)]
            
            
    def fetch(tileX, tileY):
        if tarred:

            cuts = cutOfTilesPerZoom[zoom]
            
            zones = [{'name': 'zone0', 'offset':0, 'start':cuts['start'][0] , 'end':cuts['end'][0]},  ]
            for i in [1,2,3]:
                zones = zones + [{'name':'zone' + str(i) + '_north','offset':i, 'start':cuts['start'][i] , 'end':cuts['start'][i-1] -1}, {'name':'zone' + str(i) + '_south','offset':i, 'start':cuts['end'][i-1]+1 , 'end':cuts['end'][i]}]

            for zone in zones:        
                if zone['start'] <= tileY  and tileY <= zone['end']:
                    offset = zone['offset']


            zoom_c = zoom - offset
            tileX_exact = tileX / 2**offset
            tileY_exact = tileY / 2**offset
            tileX_c = math.floor(tileX_exact)
            tileY_c = math.floor(tileY_exact)
            frac_x = int((tileX_exact - tileX_c)*w)
            frac_y = int(w*(tileY_exact - tileY_c))
            frac_w = int(w/2**offset)
            
            url = apiManager.baseUrl + '/path/' + pathId + '/raster/timestamp/' + timestampId + '/tarTile/' + str(zoom_c) + '/' + str(tileX_c) + '/' + str(tileY_c)
            if str(type(style)) == str(type(None)):
                url = url + '?applyStyle=false'
            if str(type(token)) == str(type(None)):
                r = requests.get(url)
            else:
                if not 'Bearer' in token:
                    r = requests.get(url, headers={"Authorization": 'Bearer ' + token})
                else:
                    r = requests.get(url, headers={"Authorization":  token})
            
        else:
            r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/tile/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY), body, token, False)
            
        if r.status_code == 403:
                raise ValueError('insufficient access')
        elif r.status_code == 204:
                r = np.zeros((num_bands,w,w))
        elif r.status_code != 200:
                raise ValueError(r.text)
        else:
            if tarred:
                stream = BytesIO(r.content).read()
                
                r = constructImage(N, stream, as_jpg, num_bands, dtype)
                
                
                r = r[: ,frac_y:  frac_y + frac_w, frac_x: + frac_x + frac_w]
                r = np.transpose(r, [1,2,0])
                r = resize(r, (w,w), order = 0, preserve_range=True, mode = 'edge')
                r = np.transpose(r, [2,0,1])
                
            else:
                r = tifffile.imread(BytesIO(r.content))
                
        r = r.astype(dtype)            
        return r

            
            

    def iterate(fetch, i, tileX, tileY):
        return fetch(tileX, tileY)
        attempts = 5
        if i > 0:
            time.sleep(0.5)
        if i < attempts:
            try:
                return fetch(tileX, tileY)
            except:
                iterate(fetch, i+1, tileX, tileY)
        else:
            return fetch(tileX, tileY)
    I = 0

    tile = tiles[0]    
    for tile in tiles:
        tileX = tile[0]
        tileY = tile[1]
        x_index = tileX - x1_osm
        y_index = tileY - y1_osm
        
        r = iterate(fetch, 0, tileX, tileY)

        r_total[:,y_index*w:(y_index+1)*w,x_index*w:(x_index+1)*w] = r
        I = I + 1
        if showProgress:
            loadingBar(I, len(tiles))
        



    min_x_index = int(math.floor((x_start - x1_osm)*w))
    max_x_index = max(int(math.floor((x_end- x1_osm)*w + 1 )), min_x_index + 1 )
    min_y_index = int(math.floor((y_start - y1_osm)*w))
    max_y_index = max(int(math.floor((y_end- y1_osm)*w +1)), min_y_index + 1)

    r_total = r_total[:,min_y_index:max_y_index,min_x_index:max_x_index]

    mercatorExtent =  {'xMin' : xMinWeb, 'yMin': yMinWeb, 'xMax': xMaxWeb, 'yMax': yMaxWeb}
    if (not reproject) or epsg == 3857:
        trans = rasterio.transform.from_bounds(xMinWeb, yMinWeb, xMaxWeb, yMaxWeb, r_total.shape[2], r_total.shape[1])
    
        return {'raster': r_total, 'transform':trans, 'extent':mercatorExtent, 'epsg':3857}
    else:
        return reprojectRaster(r = r_total, sourceExtent = mercatorExtent, targetExtent = extent, targetWidth=r_total.shape[2], targetHeight=r_total.shape[1], sourceEpsg = 3857, targetEpsg= epsg, interpolation = 'nearest')


def analyse(pathId, timestampIds, geometry, returnType= 'all', approximate=True, token = None, epsg = 4326):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    timestampIds = sanitize.validUuidArray('timestampIds', timestampIds, True)    
    approximate = sanitize.validBool(approximate, approximate, True)    
    geometry = sanitize.validShapely('geometry', geometry, True)
    returnType = sanitize.validString('returnType', returnType, True)

    temp = gpd.GeoDataFrame({'geometry':[geometry]})
    temp.crs = 'EPSG:' + str(epsg)
    temp = temp.to_crs('EPSG:4326')
    geometry = temp['geometry'].values[0]

    try:
        sh = gpd.GeoDataFrame({'geometry':[geometry]})
        geometry =sh.to_json(na='drop')
        geometry = json.loads(geometry)
        geometry = geometry['features'][0]['geometry']
    except:
        raise ValueError('geometry must be a shapely geometry')


    body = {'timestampIds':timestampIds, 'geometry':geometry, 'approximate':approximate, returnType:returnType}
    r = apiManager.get('/path/' + pathId + '/raster/timestamp/analyse', body, token)
    return r


def add(pathId, token, description= None, date ={'from': datetime.datetime.now(), 'to': datetime.datetime.now()}):
    

    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    date = sanitize.validDateRange('date', date, True)    
    description = sanitize.validString('description', description, False)    

    body = { 'date': date, 'description': description}    
    r = apiManager.post('/path/' + pathId + '/raster/timestamp'  , body, token)
    return r
    
def edit(pathId, timestampId, token, date=None, description= None):

    
    
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    description = sanitize.validString('description', description, False)    
    date = sanitize.validDateRange('date', date, False)    

    body = {'date':date, 'description': description}    
    r = apiManager.patch('/path/' + pathId + '/raster/timestamp/' + timestampId  , body, token)
    return r

def getBounds(pathId, timestampId, token = None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/bounds'  , None, token)
    r = {'id': 0, 'properties':{}, 'geometry':r}

    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union
    return r

def activate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/raster/timestamp/' + timestampId + '/activate'  , None, token)
    return r

def deactivate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/raster/timestamp/' + timestampId + '/deactivate'  , None, token)
    return r


def delete(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  

    r = apiManager.delete('/path/' + pathId + '/raster/timestamp/' + timestampId  , None, token)
    return r


def trash(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trashed' : True}
    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/trashed'  , body, token)
    return r

    
def recover(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trashed' : False}
    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/trashed'  , body, token)
    return r
