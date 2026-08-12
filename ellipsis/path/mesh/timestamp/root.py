from ellipsis import sanitize
from ellipsis.util.root import getActualExtent
from ellipsis import apiManager
from ellipsis.util import loadingBar, chunks
from ellipsis.util.root import reprojectRaster
from ellipsis.path.raster.timestamp.util import constructImage
from ellipsis.path.raster.timestamp.util import cutOfTilesPerZoom

from skimage.transform import resize
import json
import numpy as np
from io import BytesIO
import rasterio
import math
import tifffile
import geopandas as gpd
import datetime
import pandas as pd
import time
import requests
from skimage.measure import find_contours
from shapely.geometry import Point, LineString



def add(pathId, token, description= None, date ={'from': datetime.datetime.now(), 'to': datetime.datetime.now()}):

    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    date = sanitize.validDateRange('date', date, True)    
    description = sanitize.validString('description', description, False)    
    body = { 'date': date, 'description': description}
    r = apiManager.post('/path/' + pathId + '/mesh/timestamp'  , body, token)
    return r
    
def edit(pathId, timestampId, token, date=None, description= None):

    
    
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    description = sanitize.validString('description', description, False)    
    date = sanitize.validDateRange('date', date, False)    

    body = {'date':date, 'description': description}    
    r = apiManager.patch('/path/' + pathId + '/mesh/timestamp/' + timestampId  , body, token)
    return r

def getBounds(pathId, timestampId, token = None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.get('/path/' + pathId + '/mesh/timestamp/' + timestampId + '/bounds'  , None, token)
    r = {'id': 0, 'properties':{}, 'geometry':r}

    r  = gpd.GeoDataFrame.from_features([r])
    r = r.unary_union
    return r

def activate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/mesh/timestamp/' + timestampId + '/activate'  , None, token)
    return r

def deactivate(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    r = apiManager.post('/path/' + pathId + '/mesh/timestamp/' + timestampId + '/deactivate'  , None, token)
    return r


def delete(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  

    r = apiManager.delete('/path/' + pathId + '/mesh/timestamp/' + timestampId  , None, token)
    return r


def trash(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trashed' : True}
    r = apiManager.put('/path/' + pathId + '/mesh/timestamp/' + timestampId + '/trashed'  , body, token)
    return r

    
def recover(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)  
    timestampId = sanitize.validUuid('timestampId', timestampId, True)  
    body = {'trashed' : False}
    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/trashed'  , body, token)
    return r
