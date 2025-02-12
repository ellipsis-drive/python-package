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

def createCompute(layers, token, nodes=None, interpreter='python3.12', requirements= [], awaitTillStarted = True, largeResult = False):
    layers = sanitize.validDictArray('layers', layers, True)
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

    body = {'layers':layers, 'interpreter':interpreter, 'nodes':nodes, 'requirements':requirements, 'largeResult': largeResult}
    r = apiManager.post('/compute', body, token)

    computeId = r['id']
    while awaitTillStarted:
        res = listComputes(token=token)['result']
        r = [x for x in res if x['id'] == computeId][0]
        if r['status'] == 'available':
            break
        if r['status'] == 'errored':
            raise ValueError(r['message'])

        time.sleep(1)

    return {'id':computeId}


def execute(computeId, f, token, awaitTillCompleted=True):
    computeId = sanitize.validUuid('computeId', computeId, True)
    token = sanitize.validString('token', token, True)

    if str(type(f)) != "<class 'function'>":
        raise ValueError('parameter f must be a function')

    f_bytes = dill.dumps(f)
    f_string = base64.b64encode(f_bytes)

    body = { 'file':f_string}
    apiManager.post('/compute/' + computeId + '/execute', body, token)

    while awaitTillCompleted:
        res = listComputes(token=token)['result']
        r = [x for x in res if x['id'] == computeId][0]
        if r['status'] == 'completed':
            break
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

def terminatecompute(computeId, token, awaitTillTerminated = True):
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
        memfile = downloadFile(url,  token)
        addFile(pathId = pathId, timestampId=timestampId, token = token, fileFormat='tif', memFile=memfile, name='out.tif')
    activate(pathId=pathId, timestampId=timestampId, token=token)



def downloadFile(url,  token):
    memfile = BytesIO()
    apiManager.download(url = url, filePath='', memfile=memfile, token = token)
    memfile.seek(0)
    return memfile