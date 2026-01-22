import time
import inspect
import json

from ellipsis.util.root import recurse
from ellipsis import sanitize
from ellipsis.account import getInfo
from ellipsis import apiManager
from ellipsis.path.raster.timestamp.file import add as addFile
from ellipsis.path.raster.timestamp import activate
from io import BytesIO

def createCompute(layers, token, files = None, nodes=None, interpreter='python3.12', requirements= [], awaitTillStarted = True, largeResult = False, enableGpu=False):
    layers = sanitize.validDictArray('layers', layers, True)
    files = sanitize.validUuidArray('files', files, False)
    token = sanitize.validString('token', token, True)
    nodes = sanitize.validInt('nodes', nodes, False)
    interpreter = sanitize.validString('interpreter', interpreter, True)
    requirements = sanitize.validStringArray('requirements', requirements, False)
    largeResult = sanitize.validBool('largeResult', largeResult, True)
    enableGpu = sanitize.validBool('enableGpu', enableGpu, True)
    if type(nodes) == type(None):
        info = getInfo(token=token)
        nodes = info['plan']['maxComputeNodes']
        if nodes == 0:
            raise ValueError('You have no compute nodes in your plan. Please update your subscription')

    requirements = "\n".join(requirements)

    body = {'layers':layers, 'files':files, 'interpreter':interpreter, 'nodes':nodes, 'requirements':requirements, 'largeResult': largeResult, 'enableGpu':enableGpu}
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

    f_text =  inspect.getsource(f)
    f_name = f_text.split('(')[0].replace('def', '').replace(' ', '')
    f_text = f_text.replace('\n', '\n  ')
    f_text = ' ' + f_text

    file = 'def userFunction(params):\n' + f_text + '\n return ' + f_name + '(params)'

    body = { 'file':file, 'writeToLayer':writeToLayer}

    apiManager.post('/compute/' + computeId + '/execute', body, token)

    while awaitTillCompleted:
        res = listComputes(token=token)['result']
        r = [x for x in res if x['id'] == computeId][0]
        if r['status'] == 'completed':
            break
        if r['status'] == 'errored':
            raise ValueError(str(r['message']))
        time.sleep(1)

    for x in r['result']:
        if x['type'] == 'exception':
            raise ValueError( x['value'])


    values = [ '/compute/' + computeId + '/file/'+ x['value'] if x['type'] == 'file' else x['value'] for x in r['result']]
    return values

def parseResults(r):
    results = []
    for x in r:
        arr = []
        for y in x:
            if y['type'] != 'exception' and y['type'] != 'upload':
                    y['value'] = json.loads(y['value'])
            arr.append(y)
        results = results + arr

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
        memfile = BytesIO()
        memfile = downloadFile(url,  token, memfile=memfile)
        addFile(pathId = pathId, timestampId=timestampId, token = token, fileFormat='tif', memFile=memfile, name= url.split('/')[-1] + '.tif' )
    activate(pathId=pathId, timestampId=timestampId, token=token)



def downloadFile(url,  token, filePath = None, memfile = None):

    url = sanitize.validString('url', url, True)
    token = sanitize.validString('token', token, True)
    filePath = sanitize.validString('filePath', filePath, False)
    if memfile == None and filePath == None:
        raise ValueError('Either memfile or filePath is required')

    apiManager.download(url = url, filePath=filePath, memfile=memfile, token = token)

    if memfile != None:
        return memfile