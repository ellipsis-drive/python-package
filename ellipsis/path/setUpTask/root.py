from ellipsis import apiManager
from ellipsis import sanitize
import os

def get(token):
    token = sanitize.validString('token', token, False)

    r = apiManager.get('/path/setUpTask', {}, token)
        
    return r


def copernicusImport( parameters, token):
    token = sanitize.validString('token', token, True)
    parameters = sanitize.validObject('parameters', parameters, True)
    r = apiManager.post('/path/setUpTask', {'type':'copernicusImport', 'parameters':parameters}, token)
        
    return r


def fileImport(  token, memFile=None, parentId = None, filePath=None, fileFormat = 'geopackage', name = None):
    token = sanitize.validString('token', token, True)
    parentId = sanitize.validUuid(('parentId', parentId, False))
    filePath = sanitize.validString('filePath', filePath, False)
    name = sanitize.validString('name', name, False)
    fileFormat = sanitize.validString('fileFormat', fileFormat, True)


    if type(memFile) == type(None) and type(filePath) == type(None):
        raise ValueError('You need to specify either a filePath or a memFile')
    if type(memFile) != type(None) and type(name) == type(None):
        raise ValueError('Parameter name is required when using a memory file')

    if type(name) != type(None):
        nameToUse = name
    else:
        seperator = os.path.sep
        nameToUse = filePath.split(seperator)[len(filePath.split(seperator)) - 1]

    parameters = {'name': nameToUse, 'parentId': parentId}
    body = {'type': fileFormat + 'Import', 'parameters': parameters}
    if type(memFile) == type(None):
        r = apiManager.post('/path/setUpTask', body, token)
    else:
        r = apiManager.upload('/path/setUpTask' , filePath , name, body, token, memfile = memFile)
    return r




