from ellipsis import sanitize
from ellipsis import apiManager
from ellipsis.util import loadingBar
from ellipsis.util import chunks

import json
from pyproj import Proj, transform
import numpy as np
from io import BytesIO
import rasterio
import math
import tifffile
import threading
from PIL import Image
import geopandas as gpd
import datetime

def getDownsampledRaster(pathId, timestampId, bounds, width, height, layer = None, token = None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, True)
    layer = sanitize.validObject('layer', layer, False)

    body = {'pathId':pathId, 'timestampId':timestampId, 'bounds':bounds, 'width':width, 'height':height}
    r = apiManager.get('/path/' + pathId + '/timestamp/' + timestampId + '/rasterByBounds', body, token, crash = False)
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
    xMinWeb,yMinWeb =  transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMin, yMin)
    xMaxWeb,yMaxWeb = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMax, yMax)


    trans = rasterio.transform.from_bounds(xMinWeb, yMinWeb, xMaxWeb, yMaxWeb, r.shape[2], r.shape[1])

    return {'raster': r, 'transform':trans, 'extent': {'xMin' : xMinWeb, 'yMin': yMinWeb, 'xMax': xMaxWeb, 'yMax': yMaxWeb}, 'crs':"EPSG:3857"}




def getRaster(pathId, timestampId, bounds, layer = None, threads = 1, token = None):

    threads = sanitize.validInt('threads', threads, True)
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    bounds = sanitize.validBounds('bounds', bounds, True)
    layer = sanitize.validObject('layer', layer, False)

        
    xMin = bounds['xMin']
    yMin = bounds['yMin']
    xMax = bounds['xMax']
    yMax = bounds['yMax']
    xMinWeb,yMinWeb =  transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMin, yMin)
    xMaxWeb,yMaxWeb = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), xMax, yMax)

    info = apiManager.get('/path/' + pathId, token)
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
        
    min_x_index = int(math.floor((min_x_osm_precise - min_x_osm)*256))
    max_x_index = max(int(math.floor((max_x_osm_precise- min_x_osm)*256 + 1 )), min_x_index + 1 )
    min_y_index = int(math.floor((min_y_osm_precise - min_y_osm)*256))
    max_y_index = max(int(math.floor((max_y_osm_precise- min_y_osm)*256 +1)), min_y_index + 1)

    r_total = r_total[:,min_y_index:max_y_index,min_x_index:max_x_index]
 
    trans = rasterio.transform.from_bounds(xMinWeb, yMinWeb, xMaxWeb, yMaxWeb, r_total.shape[2], r_total.shape[1])

    return {'raster': r_total, 'transform':trans, 'extent': {'xMin' : xMinWeb, 'yMin': yMinWeb, 'xMax': xMaxWeb, 'yMax': yMaxWeb}, 'crs':"EPSG:3857"}


def getAggregatedData(pathId, timestampIds, geometry, approximate=True, token = None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)    
    timestampIds = sanitize.validUuidArray('timestampIds', timestampIds, True)    
    approximate = sanitize.validBool(approximate, approximate, True)    

    try:
        sh = gpd.GeoDataFrame({'geometry':[geometry]})
        geometry =sh.to_json(na='drop')
        geometry = json.loads(geometry)
        geometry = geometry['features'][0]['geometry']
    except:
        raise ValueError('geometry must be a shapely geometry')


    body = {'timestampIds':timestampIds, 'geometry':geometry, 'approximate':approximate}
    r = apiManager.get('/path/' + pathId + '/timestamp/analyse', body, token)
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

def trash(pathId, timestampId, token, trash):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trash' : True}
    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/trash'  , body, token)
    return r

    
def recover(pathId, timestampId, token, trash):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trash' : False}
    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/trash'  , body, token)
    return r
