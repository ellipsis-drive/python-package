from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse

import os
import numpy as np
import geopandas as gpd

def add(pathId, timestampId, filePath, token, fileFormat, epsg = None, noDataValue = None, mosaicPriority = None):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    filePath = sanitize.validString('filePath', filePath, True)
    noDataValue = sanitize.validFloat('noDataValue', noDataValue, False)    
    epsg = sanitize.validInt('epsg', epsg, False)    
    fileFormat = sanitize.validString('fileFormat', fileFormat, True)    
    mosaicPriority = sanitize.validString('mosaicPriority', mosaicPriority, False)    
        
    seperator = os.path.sep    
    fileName = filePath.split(seperator)[len(filePath.split(seperator))-1 ]
    
    body = {'name':fileName, 'epsg':epsg, 'noDataValue': noDataValue, 'format':fileFormat, 'mosaicPriority':mosaicPriority}
    r = apiManager.upload('/path/' + pathId + '/raster/timestamp/' + timestampId + '/file' , filePath, body, token)
    return r

def get(pathId, timestampId, token, pageStart= None, listAll = True):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    pageStart = sanitize.validObject('pageStart', pageStart, False) 

    def f(body):
        r = apiManager.get('/path/' + pathId + '/raster/timestamp/' + timestampId + '/file', body, token)    
        for i in np.arange( len(r['result'])):
            if 'info' in r['result'][i].keys() and 'bounds' in r['result'][i]['info'].keys() and type(r['result'][i]['info']['bounds']) != type(None):
                r['result'][i]['info']['bounds'] = gpd.GeoDataFrame.from_features([{'id': 0, 'properties':{}, 'geometry':r['result'][i]['info']['bounds']}]).unary_union
        
        return r

    r = recurse(f, {'pageStart':pageStart}, listAll)
    return r
    

def trash(pathId, timestampId, fileId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    fileId = sanitize.validUuid('fileId', fileId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 

    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/file/' + fileId + '/trashed', {'trashed':True}, token)    
    return r


def recover(pathId, timestampId, fileId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    fileId = sanitize.validUuid('fileId', fileId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 

    r = apiManager.put('/path/' + pathId + '/raster/timestamp/' + timestampId + '/file/' + fileId + '/trashed', {'trashed':False}, token)    
    return r



def delete(pathId, timestampId, fileId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    fileId = sanitize.validUuid('fileId', fileId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 

    r = apiManager.delete('/path/' + pathId + '/raster/timestamp/' + timestampId + '/file/' + fileId, None, token)    
    return r

def download(pathId, timestampId, fileId, filePath, token):
    
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    fileId = sanitize.validUuid('fileId', fileId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    filePath = sanitize.validString('filePath', filePath, True)


    apiManager.download('/path/' + pathId + '/raster/timestamp/' + timestampId + '/file/' + fileId + '/data', filePath, token)
