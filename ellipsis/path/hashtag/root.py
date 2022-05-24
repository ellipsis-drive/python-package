from ...util import *
from ....ellipsis import apiManager, sanitize


def add(pathId=None, token=None, hashtag=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    hashtag = sanitize.validString('hashtag', hashtag, True)

    return apiManager.post(f'/path/{pathId}/hashtag', {
        'hashtag': hashtag
    }, token)


def remove(pathId=None, token=None, hashtag=None):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    hashtag = sanitize.validString('hashtag', hashtag, True)
    return apiManager.delete(f'/path/{pathId}/hashtag/{hashtag}', None, token)


def search(token=None, hashtag=None):
    token = sanitize.validString('token', token, False)
    hashtag = sanitize.validString('hashtag', hashtag, True)
    return apiManager.get('/path/hashtag', {
        'hashtag': hashtag
    }, token)
