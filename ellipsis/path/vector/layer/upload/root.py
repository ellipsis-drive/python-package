from ellipsis import apiManager
from ellipsis import sanitize
import os

def upload(pathId, layerId, filePath, token, epsg = None, fileFormat = 'geojson', dateColumns = None, datePatterns = None):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 
    filePath = sanitize.validString('filePath', filePath, True)
    epsg = sanitize.validInt('epsg', epsg, False)    
    fileFormat = sanitize.validString('fileFormat', fileFormat, False)    
    dateColumns = sanitize.validStringArray('dateColumns', dateColumns, False)    
    datePatterns = sanitize.validStringArray('datePatterns', datePatterns, False)    
        
    seperator = os.path.sep    
    fileName = filePath.split(seperator)[len(filePath.split(seperator))-1 ]
    
    body = {'fileName':fileName, 'epsg':epsg, 'format':fileFormat, 'dateColumns': dateColumns, 'datePatterns':datePatterns}
    apiManager.upload('/path/' + pathId + '/vector/layer/' + layerId + '/upload' , filePath, body, token)


def get(pathId, layerId, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    layerId = sanitize.validUuid('layerId', layerId, True) 

    r = apiManager.get('/path/' + pathId, + '/vector/layer/' + layerId + '/upload', None, token)    
    return r

