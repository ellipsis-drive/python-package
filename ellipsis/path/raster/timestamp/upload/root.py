from ellipsis import apiManager
from ellipsis import sanitize
import os

def upload(pathId, timestampId, filePath, token, epsg = None, noDataValue = None, fileFormat = 'tif'):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    filePath = sanitize.validString('filePath', filePath, True)
    noDataValue = sanitize.validFloat('noDataValue', noDataValue, False)    
    epsg = sanitize.validInt('epsg', epsg, False)    
    fileFormat = sanitize.validString('fileFormat', fileFormat, False)    
        
    seperator = os.path.sep    
    fileName = filePath.split(seperator)[len(filePath.split(seperator))-1 ]
    
    body = {'fileName':fileName, 'epsg':epsg, 'noDataValue':noDataValue, 'format':fileFormat}
    apiManager.upload('/path/' + pathId + '/raster/timestamp/' + timestampId + '/upload' , filePath, body, token)


def get(pathId, timestampId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 

    r = apiManager.get('/path/' + pathId, + '/raster/timestamp/' + timestampId + '/upload', None, token)    
    return r

