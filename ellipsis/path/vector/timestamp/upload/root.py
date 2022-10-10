from ellipsis import apiManager
from ellipsis import sanitize
import os
from ellipsis.util.root import recurse

def upload(pathId, timestampId, filePath, token, fileFormat, epsg = None, dateColumns = None, datePatterns = None, method= 'simplify', fastUpload = False):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    filePath = sanitize.validString('filePath', filePath, True)
    epsg = sanitize.validInt('epsg', epsg, False)
    method = sanitize.validString('method', method, True)
    fileFormat = sanitize.validString('fileFormat', fileFormat, True)    
    dateColumns = sanitize.validStringArray('dateColumns', dateColumns, False)    
    datePatterns = sanitize.validStringArray('datePatterns', datePatterns, False)    
    fastUpload = sanitize.validBool('fastUpload', fastUpload, True)
    if fastUpload:
        fastUpload='true'
    else:
        fastUpload = 'false'
        
    seperator = os.path.sep    
    fileName = filePath.split(seperator)[len(filePath.split(seperator))-1 ]
    
    body = {'fileName':fileName, 'epsg':epsg, 'format':fileFormat, 'dateColumns': dateColumns, 'datePatterns':datePatterns, 'fastUpload':fastUpload}
    apiManager.upload('/path/' + pathId + '/vector/timestamp/' + timestampId + '/upload' , filePath, body, token)


def get(pathId, timestampId, token, pageStart = None, listAll = True):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, True)

    body = {'pageStart': pageStart}
    def f(body):    
        r = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/upload', body, token)    
        return r

    r = recurse(f, body, listAll)
    return r