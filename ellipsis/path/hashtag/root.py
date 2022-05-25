from ellipsis import apiManager, sanitize


def add(pathId, hashtag, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, True)
    hashtag = sanitize.validString('hashtag', hashtag, True)

    return apiManager.post(f'/path/{pathId}/hashtag', {
        'hashtag': hashtag
    }, token)


def delete(pathId, hashtag, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    token = sanitize.validString('token', token, False)
    hashtag = sanitize.validString('hashtag', hashtag, True)
    return apiManager.delete(f'/path/{pathId}/hashtag/{hashtag}', None, token)


def search(hashtag):
    hashtag = sanitize.validString('hashtag', hashtag, True)
    return apiManager.get('/path/hashtag', {
        'hashtag': hashtag
    }, None)
