from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse
from ellipsis.util.root import stringToDate
from PIL import Image
from io import BytesIO
import base64


def get(pathId, timestampId, featureIds = None, userId = None, messageIds = None, listAll = True, deleted = False, extent = None, pageStart = None, token = None ):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    token = sanitize.validString('token', token, False)
    userId = sanitize.validUuid('userId', userId, False)
    messageIds = sanitize.validUuidArray('messageIds', messageIds, False)
    featureIds = sanitize.validUuidArray('featureIds', featureIds, False)
    listAll = sanitize.validBool('listAll', listAll, True)
    deleted = sanitize.validBool('deleted', deleted, True)
    extent = sanitize.validBounds('extent', extent, False)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)

    body = {'userId': userId, 'messageIds':messageIds, 'deleted':deleted, 'extent':extent, 'featureIds':featureIds, 'pageStart':pageStart}
    
    def f(body):
        r = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId +  '/feature/message', body, token )
        return r
    
    r = recurse(f, body, listAll)
    
    r['result'] = [{**x, 'date':stringToDate(x['date']) } for x in r['result'] ]
    
    return r

def getImage(pathId, timestampId, messageId, token = None ):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    messageId = sanitize.validUuid('messageId', messageId, True)     
    token = sanitize.validString('token', token, False)

    r = apiManager.get('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/message/' + messageId + '/image', None, token, False)

    if r.status_code != 200:
        raise ValueError(r.text)
        
    im = Image.open(BytesIO(r.content))
 
    return(im)


def add(pathId, timestampId, featureId, token, text = None, image=None):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    featureId = sanitize.validUuid('featureId', featureId, True) 
    token = sanitize.validString('token', token, True)
    text = sanitize.validString('text', text, False)
    image = sanitize.validImage('image', image, False)    

    if type(image) != type(None):
        image = Image.fromarray(image.astype('uint8'))
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = str(base64.b64encode(buffered.getvalue()))
        img_str = 'data:image/jpeg;base64,' + img_str[2:-1]
    else:
        img_str = None


    body = {'image':img_str, 'text':text}
    r = apiManager.post('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/' + featureId + '/message', body, token)
    return r


def trash(pathId, timestampId, messageId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    messageId = sanitize.validUuid('messageId', messageId, True) 
    token = sanitize.validString('token', token, True)
    body = {'trashed': True}
    r = apiManager.put('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/message/' + messageId + '/trashed', body, token)
    return r


def recover(pathId, timestampId, messageId, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    timestampId = sanitize.validUuid('timestampId', timestampId, True) 
    messageId = sanitize.validUuid('messageId', messageId, True) 
    token = sanitize.validString('token', token, True)
    body = {'trashed': False}
    r = apiManager.put('/path/' + pathId + '/vector/timestamp/' + timestampId + '/feature/message/' + messageId + '/trashed', body, token)
    return r


