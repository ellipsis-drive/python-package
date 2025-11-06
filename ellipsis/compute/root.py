import dill
import base64
import time

from ellipsis.util.root import recurse
from ellipsis import sanitize
from ellipsis.account import getInfo
from ellipsis import apiManager
from ellipsis.path.raster.timestamp.file import add as addFile
from ellipsis.path.raster.timestamp import activate
from io import BytesIO

def createCompute(layers, token, files = None, nodes=None, interpreter='python3.12', requirements= [], awaitTillStarted = True, largeResult = False):
    layers = sanitize.validDictArray('layers', layers, True)
    files = sanitize.validUuidArray('files', files, False)
    token = sanitize.validString('token', token, True)
    nodes = sanitize.validInt('nodes', nodes, False)
    interpreter = sanitize.validString('interpreter', interpreter, True)
    requirements = sanitize.validStringArray('requirements', requirements, False)
    largeResult = sanitize.validBool('largeResult', largeResult, True)
    if type(nodes) == type(None):
        info = getInfo(token=token)
        nodes = info['plan']['maxComputeNodes']
        if nodes == 0:
            raise ValueError('You have no compute nodes in your plan. Please update your subscription')

    requirements = "\n".join(requirements)

    body = {'layers':layers, 'files':files, 'interpreter':interpreter, 'nodes':nodes, 'requirements':requirements, 'largeResult': largeResult}
    r = apiManager.post('/compute', body, token)

    computeId = r['id']
    while awaitTillStarted:
        print('waiting')
        res = listComputes(token=token)['result']
        r = [x for x in res if x['id'] == computeId][0]
        if r['status'] == 'available':
            break
        if r['status'] == 'errored':
            raise ValueError(r['message'])

        time.sleep(1)

    return {'id':computeId}


def execute(computeId, f, token, awaitTillCompleted=True, writeToLayer = None):
    computeId = sanitize.validUuid('computeId', computeId, True)
    token = sanitize.validString('token', token, True)
    writeToLayer = sanitize.validObject('writeToLayer', writeToLayer, False)
    awaitTillCompleted = sanitize.validBool('awaitTillCompleted', awaitTillCompleted, False)

    if str(type(f)) != "<class 'function'>":
        raise ValueError('parameter f must be a function')
    if type(writeToLayer) != type(None):
        if not 'file' in writeToLayer:
            writeToLayer['file'] = {'format':'tif'}
    f_bytes = dill.dumps(f)
    f_string = base64.b64encode( f_bytes )
    f_string = str(f_string)[2: -1]
    body = { 'file':f_string, 'writeToLayer':writeToLayer}
    apiManager.post('/compute/' + computeId + '/execute', body, token)

    while awaitTillCompleted:
        res = listComputes(token=token)['result']
        r = [x for x in res if x['id'] == computeId][0]
        print('waiting')
        if r['status'] == 'completed':
            break
        if r['status'] == 'errored':
            raise ValueError(str(r['message']))
        time.sleep(1)

    for x in r['result']:
        if x['type'] == 'exception':
            raise x['value']


    values = [ '/compute/' + computeId + '/file/'+ x['value'] if x['type'] == 'file' else x['value'] for x in r['result']]
    return values

def parseResults(r):
    results = []
    for x in r:
        x = base64.b64decode(x)
        x = dill.loads(x)
        results = results + x

    return results

def terminateCompute(computeId, token, awaitTillTerminated = True):
    computeId = sanitize.validUuid('computeId', computeId, True)
    token = sanitize.validString('token', token, True)
    sanitize.validBool('awaitTillTerminated',awaitTillTerminated, True)


    r = apiManager.post('/compute/' + computeId + '/terminate', {}, token)

    while awaitTillTerminated:
        res = listComputes(token=token)['result']
        z = [x for x in res if x['id'] == computeId][0]
        if z['status'] == 'stopped':
            break
        time.sleep(1)

    return r

def terminateAll(token, awaitTillTerminated = True ):
    token = sanitize.validString('token', token, True)
    sanitize.validBool('awaitTillTerminated',awaitTillTerminated, True)

    res = listComputes(token = token)['result']

    for x in res:
        if x['status'] != 'stopped' and x['status'] != 'errored' and x['status'] != 'stopping':

            apiManager.post('/compute/' + x['id'] + '/terminate', {}, token)

            while awaitTillTerminated:
                res = listComputes(token=token)['result']
                z = [x for x in res if x['id'] == x['id']][0]
                if z['status'] == 'stopped':
                    break
                time.sleep(1)



def getComputeInfo(computeId, token):
    res = listComputes(token=token)['result']
    r = [x for x in res if x['id'] == computeId]
    if len(r) ==0:
        raise ValueError('No compute found for given id')
    return r[0]

def listComputes(token, pageStart = None, listAll = True):
    token = sanitize.validString('token', token, True)


    body = { 'pageStart':pageStart }


    def f(body):
        return apiManager.get('/compute', body, token)

    r = recurse(f, body, listAll)
    for i in range(len(r['result'])):
        if 'result' in r['result'][i]:
                r['result'][i]['result'] = parseResults(r['result'][i]['result'])
    return r

def addToLayer(response, pathId, timestampId, token):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, True)

    for url in response:
        print('fetching file ' + url.split('/')[-1])
        memfile = BytesIO()
        memfile = downloadFile(url,  token, memfile=memfile)
        print('read file ' + url.split('/')[-1])
        print('adding file ' + url.split('/')[-1])
        addFile(pathId = pathId, timestampId=timestampId, token = token, fileFormat='tif', memFile=memfile, name= url.split('/')[-1] + '.tif' )
        print('file ' + url.split('/')[-1] + ' added to layer')
    activate(pathId=pathId, timestampId=timestampId, token=token)
    print('layer can now be found at ' + apiManager.baseUrl + '/drive/me?pathId=' + pathId )



def downloadFile(url,  token, filePath = None, memfile = None):

    url = sanitize.validString('url', url, True)
    token = sanitize.validString('token', token, True)
    filePath = sanitize.validString('filePath', filePath, False)
    if memfile == None and filePath == None:
        raise ValueError('Either memfile or filePath is required')

    apiManager.download(url = url, filePath=filePath, memfile=memfile, token = token)

    if memfile != None:
        return memfile