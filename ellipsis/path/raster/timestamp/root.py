from ellipsis import sanitize
from ellipsis import apiManager
from ellipsis.util import loadingBar
from ellipsis.util import chunks
from ellipsis.util.root import transformPoint

import json
import numpy as np
from io import BytesIO
import rasterio
import math
import tifffile
import threading
from PIL import Image
import geopandas as gpd
import datetime

def getDownsampledRaster(pathId, timestampId, extent, width, height, layer = None, token = None):
    bounds = extent
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, True)
    layer = sanitize.validObject('layer', layer, False)

    body = {'pathId':pathId, 'timestampId':timestampId, 'bounds':bounds, 'width':width, 'height':height}
    r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/rasterByBounds', body, token, crash = False)
    if r.status_code != 200:
        raise ValueError(r.message)


    if type(layer) == type(None):
        r = tifffile.imread(BytesIO(r.content))
    else:
        r = np.array(Image.open(BytesIO(r.content)))
        r = np.transpose(r, [2,0,1])

    xMin = bounds['xMin']
    yMin = bounds['yMin']
    xMax = bounds['xMax']
    yMax = bounds['yMax']

    xMinWeb, yMinWeb = transformPoint( (xMin, yMin), 'EPSG:4326', 'EPSG:3857')
    xMaxWeb, yMaxWeb = transformPoint( (xMax, yMax), 'EPSG:4326', 'EPSG:3857')


    trans = rasterio.transform.from_bounds(xMinWeb, yMinWeb, xMaxWeb, yMaxWeb, r.shape[2], r.shape[1])

    return {'raster': r, 'transform':trans, 'extent': {'xMin' : xMinWeb, 'yMin': yMinWeb, 'xMax': xMaxWeb, 'yMax': yMaxWeb}, 'crs':"EPSG:3857"}




def getRaster(pathId, timestampId, extent, layer = None, threads = 1, token = None, showProgress = True):
    bounds = extent
    threads = sanitize.validInt('threads', threads, True)
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, True)
    layer = sanitize.validObject('layer', layer, False)
    showProgress = sanitize.validBool('showProgress', showProgress, True)

        
    xMin = bounds['xMin']
    yMin = bounds['yMin']
    xMax = bounds['xMax']
    yMax = bounds['yMax']
    xMinWeb,yMinWeb =  transformPoint((xMin, yMin), 'EPSG:4326', 'EPSG:3857')
    xMaxWeb,yMaxWeb = transformPoint((xMax, yMax), 'EPSG:4326', 'EPSG:3857')

    info = apiManager.get('/path/' + pathId, None, token)
    bands =  info['raster']['bands']
    if type(layer) == type(None):
        num_bands = len(bands)
        dtype = info['raster']['format']
    else:
        num_bands = 4
        dtype = 'uint8'

    timestamps =  info['raster']['timestamps']
    all_timestamps = [item['id'] for item in timestamps]
    if not timestampId in all_timestamps:
        raise ValueError('given timestamp does not exist')
    
    zoom = next(item for item in timestamps if item["id"] == timestampId)['zoom']

    body = {'layer':layer}

    LEN = 2.003751e+07

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
    
    r_total = np.zeros((num_bands, 256*(y2_osm - y1_osm + 1) ,256*(x2_osm - x1_osm + 1)), dtype = dtype)
    
    tiles = []            
    for tileY in y_tiles:
        for tileX in x_tiles:
            tiles = tiles + [(tileX, tileY)]
    def subTiles(tiles):
            N = 0
            for tile in tiles:
                tileX = tile[0]
                tileY = tile[1]
                x_index = tileX - x1_osm
                y_index = tileY - y1_osm
                
                r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/tile/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY), body, token, False)

                if r.status_code == 403:
                        raise ValueError('insufficient access')
                if r.status_code != 200:
                        r = np.zeros((num_bands,256,256))
                else:
                    if type(layer) == type(None):
                        r = tifffile.imread(BytesIO(r.content))
                    else:
                        r = np.array(Image.open(BytesIO(r.content)))
                        r = np.transpose(r, [2,0,1])

                r = r.astype(dtype)
                r_total[:,y_index*256:(y_index+1)*256,x_index*256:(x_index+1)*256] = r
                if showProgress:
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
        
    min_x_index = int(math.floor((x_start - x1_osm)*256))
    max_x_index = max(int(math.floor((x_end- x1_osm)*256 + 1 )), min_x_index + 1 )
    min_y_index = int(math.floor((y_start - y1_osm)*256))
    max_y_index = max(int(math.floor((y_end- y1_osm)*256 +1)), min_y_index + 1)

    r_total = r_total[:,min_y_index:max_y_index,min_x_index:max_x_index]
 
    trans = rasterio.transform.from_bounds(xMinWeb, yMinWeb, xMaxWeb, yMaxWeb, r_total.shape[2], r_total.shape[1])

    return {'raster': r_total, 'transform':trans, 'extent': {'xMin' : xMinWeb, 'yMin': yMinWeb, 'xMax': xMaxWeb, 'yMax': yMaxWeb}, 'crs':"EPSG:3857"}


def getAggregatedData(pathId, timestampIds, geometry, approximate=True, token = None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    timestampIds = sanitize.validUuidArray('timestampIds', timestampIds, True)    
    approximate = sanitize.validBool(approximate, approximate, True)    
    geometry = sanitize.validShapely('geometry', geometry, True)
    try:
        sh = gpd.GeoDataFrame({'geometry':[geometry]})
        geometry =sh.to_json(na='drop')
        geometry = json.loads(geometry)
        geometry = geometry['features'][0]['geometry']
    except:
        raise ValueError('geometry must be a shapely geometry')


    body = {'timestampIds':timestampIds, 'geometry':geometry, 'approximate':approximate}
    r = apiManager.get('/path/' + pathId + '/raster/timestamp/analyse', body, token)
    return r


def add(pathId, token, dateFrom = None, dateTo = None, description= None,  appendToTimestampId = None):
    
    if type(dateFrom) == type(None):
        dateFrom = datetime.datetime.now()
    if type(dateTo) == type(None):
        dateTo = datetime.datetime.now()


    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    dateFrom = sanitize.validDate('dateFrom', dateFrom, True)    
    dateTo = sanitize.validDate('dateTo', dateTo, True)    
    description = sanitize.validString('description', description, False)    
    appendToTimestampId = sanitize.validUuid('appendToTimestampId', appendToTimestampId, False)    

    body = {'dateFrom' : dateFrom, 'dateTo':dateTo, 'description': description, 'appendToTimestampId': appendToTimestampId}    
    r = apiManager.post('/path/' + pathId + '/raster/timestamp'  , body, token)
    return r
    
def edit(pathId, timestampId, token, dateFrom = None, dateTo = None, description= None):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    dateFrom = sanitize.validDate('dateFrom', dateFrom, False)    
    dateTo = sanitize.validDate('dateTo', dateTo, False)    
    description = sanitize.validString('description', description, False)    

    body = {'dateFrom' : dateFrom, 'dateTo':dateTo, 'description': description}    
    r = apiManager.patch('/path/' + pathId + '/raster/timestamp/' + timestampId  , body, token)
    return r

def getBounds(pathId, timestampId, token = None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/bounds'  , None, token)
    r['id'] = 0
    r['properties'] = {}
    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union
    return r

def activate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/raster/timestamp/' + timestampId + '/activate'  , None, token)
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
