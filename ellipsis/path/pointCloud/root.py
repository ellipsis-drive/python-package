from ellipsis import apiManager
from ellipsis import sanitize


def add( name, token, parentId = None, publicAccess =None, metadata=None):
    name = sanitize.validString('name', name, True)
    token = sanitize.validString('token', token, True)
    parentId = sanitize.validUuid('parentId', parentId, False)
    metadata = sanitize.validObject('metadata', metadata, False)
    publicAccess = sanitize.validObject('publicAccess', publicAccess, False)

    body = {'name': name, 'parentId':parentId, 'publicAccess':publicAccess, 'metadata':metadata }

    return apiManager.post('/path/pointCloud', body, token)


