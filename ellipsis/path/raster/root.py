from ellipsis import apiManager
from ellipsis import sanitize


def add( name, token, parentId = None, publicAccess =None, metadata=None):
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    parentId = sanitize.validUuid('parentId', parentId, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)

    body = {'name': name, 'parentId':parentId, 'publicAccess':publicAccess, 'metadata':metadata }

    return apiManager.post('/path/raster', body, token)


def editBand(pathId, bandNumber, name, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    bandNumber = sanitize.validInt('bandNumber', bandNumber, True)
    name = sanitize.validString('name', name, True)
    body = {'name':name}
    r = apiManager.put('/path/' + pathId + '/raster/band/' + str(bandNumber) + '/name', body, token)
    return(r)

# /path/{pathId}/raster
def edit(pathId, token, interpolation = None, includesTransparent = None, compressionQuality = None):

    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    interpolation = sanitize.validString('interpolation', interpolation, False)
    includesTransparent = sanitize.validBool('includesTransparent', includesTransparent, False)
    compressionQuality = sanitize.validInt('compressionQuality', compressionQuality, False)

    body = {'interpolation':interpolation, 'includesTransparent':includesTransparent, 'compressionQuality':compressionQuality}
    r = apiManager.patch('/path/' + pathId + '/raster' , body, token)
    return(r)
    