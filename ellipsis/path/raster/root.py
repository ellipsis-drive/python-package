from ellipsis import apiManager
from ellipsis import sanitize


def editBand(pathId, bandNumber, name, token):
    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    bandNumber = sanitize.validInt('bandNumber', bandNumber, True)
    name = sanitize.validString('name', name, True)
    body = {'name':name}
    r = apiManager.put('/path/' + pathId + '/raster/band/' + str(bandNumber) + '/name', body, token)
    return(r)

# /path/{pathId}/raster
def editMap(pathId, token, interpolation = None, includesTransparent = None):

    token = sanitize.validString('token', token, True)
    pathId = sanitize.validUuid('pathId', pathId, True)
    interpolation = sanitize.validString('interpolation', interpolation, False)
    includesTransparent = sanitize.validBool('includesTransparent', includesTransparent, False)

    body = {'interpolation':interpolation, 'includesTransparent':includesTransparent}
    r = apiManager.patch('/path/' + pathId + '/raster' , body, token)
    return(r)
    