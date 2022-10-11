from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse

import os
import numpy as np
import geopandas as gpd

def add(pathId, timestampId, filePath, token, fileFormat, epsg = None, noDataValue = None):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    filePath = sanitize.validString('filePath', filePath, True)
    noDataValue = sanitize.validFloat('noDataValue', noDataValue, False)    
    epsg = sanitize.validInt('epsg', epsg, False)    
    fileFormat = sanitize.validString('fileFormat', fileFormat, True)    
        
    seperator = os.path.sep    
    fileName = filePath.split(seperator)[len(filePath.split(seperator))-1 ]
    
    body = {'fileName':fileName, 'epsg':epsg, 'noDataValue':noDataValue, 'format':fileFormat}
    r = apiManager.upload('/path/' + pathId + '/raster/timestamp/' + timestampId + '/upload' , filePath, body, token)
    return r

def get(pathId, timestampId, token, pageStart= None, listAll = True):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    pageStart = sanitize.validUuid('pageStart', pageStart, False) 

    def f(body):
        r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/upload', None, token)    
        for i in np.arange( len(r['result'])):
            if 'info' in r['result'][i].keys() and 'bounds' in r['result'][i]['info'].keys() and type(r['result'][i]['info']['bounds']) != type(None):
                r['result'][i]['info']['bounds'] = gpd.GeoDataFrame.from_features([{'id': 0, 'properties':{}, 'geometry':r['result'][i]['info']['bounds']}]).unary_union
        
        return r

    r = recurse(f, {'pageStart':pageStart}, listAll)
    return r
    

def trash(pathId, timestampId, uploadId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    uploadId = sanitize.validUuid('uploadId', uploadId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 

    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/upload/' + uploadId + '/trashed', {'trashed':True}, token)    
    return r


def recover(pathId, timestampId, uploadId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    uploadId = sanitize.validUuid('uploadId', uploadId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 

    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/upload/' + uploadId + '/trashed', {'trashed':False}, token)    
    return r



def delete(pathId, timestampId, uploadId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    uploadId = sanitize.validUuid('uploadId', uploadId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 

    r = apiManager.delete('/path/' + pathId + '/raster/timestamp/' + timestampId + '/upload/' + uploadId, None, token)    
    return r

