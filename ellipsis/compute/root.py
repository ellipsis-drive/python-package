import dill
import base64
import time

from ellipsis.util.root import recurse
from ellipsis import sanitize
from ellipsis import apiManager
from ellipsis.account import getInfo



def createCluster(layers, token, nodes=None, interpreter='python3.12', requirements= [], awaitTillStarted = True):

    layers = sanitize.validDictArray('layers', layers, True)
    token = sanitize.validString('token', token, True)
    nodes = sanitize.validInt('nodes', nodes, False)
    interpreter = sanitize.validString('interpreter', interpreter, True)
    requirements = sanitize.validStringArray('requirements', requirements, False)

    if type(nodes) == type(None):
        info = getInfo(token=token)
        nodes = info['plan']['maxComputeNodes']
        if nodes == 0:
            raise ValueError('You have no compute nodes in your plan. Please update your subscription')

    requirements = "\n".join(requirements)

    body = {'layers':layers, 'interpreter':interpreter, 'nodes':nodes, 'requirements':requirements}
    r = apiManager.post('/compute', body, token)

    clusterId = r['id']
    while awaitTillStarted:
        res = listClusters(token=token)['result']
        r = [x for x in res if x['id'] == clusterId][0]

        if r['status'] == 'available':
            break
        time.sleep(1)

    return {'id':clusterId}


def execute(clusterId, f, token, awaitTillCompleted=True):
    clusterId = sanitize.validUuid('clusterId', clusterId, True)
    token = sanitize.validString('token', token, True)

    if str(type(f)) != "<class 'function'>":
        raise ValueError('parameter f must be a function')

    f_bytes = dill.dumps(f)
    f_string = base64.b64encode(f_bytes)

    body = { 'file':f_string}
    apiManager.post('/compute/' + clusterId + '/execute', body, token)

    while awaitTillCompleted:
        res = listClusters(token=token)['result']
        r = [x for x in res if x['id'] == clusterId][0]
        if r['status'] == 'completed':
            break
        time.sleep(1)

    return r['result']

def parseResults(r):
    results = []
    for x in r:
        x = base64.b64decode(x)
        x = dill.loads(x)
        results = results + x

    return results

def terminateCluster(clusterId, token, awaitTillTerminated = True):
    clusterId = sanitize.validUuid('clusterId', clusterId, True)
    token = sanitize.validString('token', token, True)


    r = apiManager.post('/compute/' + clusterId + '/terminate', {}, token)

    while awaitTillTerminated:
        res = listClusters(token=token)['result']
        z = [x for x in res if x['id'] == clusterId][0]
        if z['status'] == 'stopped':
            break
        time.sleep(1)

    return r

def getClusterInfo(clusterId, token):
    res = listClusters(token=token)['result']
    r = [x for x in res if x['id'] == clusterId]
    if len(r) ==0:
        raise ValueError('No cluster found for given id')
    return r[0]

def listClusters(token, pageStart = None, listAll = True):
    token = sanitize.validString('token', token, True)


    body = { 'pageStart':pageStart }


    def f(body):
        return apiManager.get('/compute', body, token)

    r = recurse(f, body, listAll)
    for i in range(len(r['result'])):
        if 'result' in r['result'][i]:
            r['result'][i]['result'] = parseResults(r['result'][i]['result'])
    return r

