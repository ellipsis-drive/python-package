import pandas as pd

from ellipsis import sanitize
from ellipsis import apiManager
from ellipsis.util.root import getActualExtent
from ellipsis.util.root import parseGlb
from ellipsis.util import loadingBar

import geopandas as gpd
import datetime
import math
from io import BytesIO
import  pandas as pd




def fetchPoints(pathId, timestampId, extent, token= None, epsg = 3857, zoom = None, showProgress = True):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    extent = sanitize.validBounds('extent', extent, True)
    epsg = sanitize.validInt('epsg', epsg, True)
    zoom = sanitize.validInt('zoom', zoom, False)
    showProgress = sanitize.validBool('showProgress', showProgress, True)

    xMin = extent['xMin']
    yMin = extent['yMin']
    xMax = extent['xMax']
    yMax = extent['yMax']

    res = getActualExtent(xMin, xMax, yMin, yMax, 'EPSG:' + str(epsg))
    if res['status'] == '400':
        raise ValueError('Invalid epsg and extent combination')

    bounds = res['message']

    xMinWeb = bounds['xMin']
    yMinWeb = bounds['yMin']
    xMaxWeb = bounds['xMax']
    yMaxWeb = bounds['yMax']

    info = apiManager.get('/path/' + pathId, None, token)


    timestamps = info['pointCloud']['timestamps']
    all_timestamps = [item['id'] for item in timestamps]
    if not timestampId in all_timestamps:
        raise ValueError('given timestamp does not exist')

    timestamp = next(item for item in timestamps if item["id"] == timestampId)
    if timestamp['status'] != 'active':
        raise ValueError('timestamp is not active, please active timestamp before making queries to it')
    zoom_n = timestamp['zoom']

    if type(zoom) == type(None):
        zoom = zoom_n

    if zoom > zoom_n:
        raise ValueError('Maximum allowed zoom for this layer is ', str(zoom_n))

    LEN = 2.003751e+07

    x_start = 2**zoom * (xMinWeb + LEN) / (2* LEN)
    x_end = 2**zoom * (xMaxWeb + LEN) / (2* LEN)
    y_end = 2**zoom * (LEN - yMinWeb) / (2* LEN)
    y_start = 2**zoom * (LEN - yMaxWeb) / (2* LEN)

    x1_osm = math.floor(x_start)
    x2_osm = math.floor(x_end)
    y1_osm = math.floor(y_start)
    y2_osm = math.floor(y_end)
    dfs = []
    I = 0
    N = len(range(x1_osm, x2_osm+1)) * len(range(y1_osm, y2_osm+1))*5
    for tileX in range(x1_osm, x2_osm + 1):
        for tileY in range(y1_osm, y2_osm + 1):
            for p in range(5):
                body = {'zipTheResponse':True, 'page': p}
                r = apiManager.get('/path/' + pathId + '/pointCloud/timestamp/' + timestampId + '/tile/' + str(zoom) + '/' + str(tileX) + '/' + str(tileY), body, token, False)

                if r.status_code == 403:
                    raise ValueError('insufficient access')
                elif r.status_code == 204:
                    pass
                elif r.status_code != 200:
                    raise ValueError(r.text)
                else:
                    stream = BytesIO(r.content).read()
                    output = parseGlb(stream)
                    df_n = pd.DataFrame({'x':output['x'], 'y':output['y'], 'z':output['z'], 'red':output['red'], 'green':output['green'], 'blue':output['blue']   })
                    dfs = dfs + [df_n]

                if showProgress:
                    I = I + 1
                    loadingBar(I, N)


    if len(dfs) == 0:
        raise ValueError('No points found in this region. Did you specify the correct epsg code? Given epsg: ' + str(epsg))
    df = pd.concat(dfs)
    return df

def add(pathId, token, description= None, date ={'from': datetime.datetime.now(), 'to': datetime.datetime.now()}):
    

    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    date = sanitize.validDateRange('date', date, True)    
    description = sanitize.validString('description', description, False)    

    body = { 'date': date, 'description': description}    
    r = apiManager.post('/path/' + pathId + '/pointCloud/timestamp'  , body, token)
    return r
    
def edit(pathId, timestampId, token, date=None, description= None):

    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    description = sanitize.validString('description', description, False)    
    date = sanitize.validDateRange('date', date, False)    

    body = {'date':date, 'description': description}    
    r = apiManager.patch('/path/' + pathId + '/pointCloud/timestamp/' + timestampId  , body, token)
    return r

def getBounds(pathId, timestampId, token = None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.get('/path/' + pathId + '/pointCloud/timestamp/' + timestampId + '/bounds'  , None, token)
    r = {'id': 0, 'properties':{}, 'geometry':r}

    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union
    return r

def activate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/pointCloud/timestamp/' + timestampId + '/activate'  , None, token)
    return r

def deactivate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/pointCloud/timestamp/' + timestampId + '/deactivate'  , None, token)
    return r


def delete(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  

    r = apiManager.delete('/path/' + pathId + '/pointCloud/timestamp/' + timestampId  , None, token)
    return r


def trash(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trashed' : True}
    r = apiManager.put('/path/' + pathId + '/pointCloud/timestamp/' + timestampId + '/trashed'  , body, token)
    return r

    
def recover(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trashed' : False}
    r = apiManager.put('/path/' + pathId + '/pointCloud/timestamp/' + timestampId + '/trashed'  , body, token)
    return r
