import dill as pickle

from ellipsis import sanitize
from ellipsis import apiManager
from ellipsis.path import get as getPath

def createCluster(pathId, timestampId, token, projection = 3857):
    pathId = sanitize.validUuid('pathId', pathId, True)
    timestampId = sanitize.validUuid('timestampId', timestampId, True)
    token = sanitize.validString('token', token, True)
    projection = sanitize.validInt('projection', projection, True)

    body = {'pathId':pathId, 'timestampId':timestampId, 'projection':projection}
    r = apiManager.post('/compute/createCluster', body, token)
    m = getPath(pathId=pathId, token = token)
    if m['type'] == 'vector':
        v = 'sh'
    else:
        v = 'r'
    print(m['type'] + ' loaded in cluster in variable ' + str(v))
    return r


def addPackage(clusterId, packageName, importName, token):
    clusterId = sanitize.validUuid('clusterId', clusterId, True)
    token = sanitize.validString('token', token, True)
    packageName = sanitize.validUuid('packageName', packageName, True)
    importName = sanitize.validUuid('importName', importName, True)

    body = {'clusterId':clusterId, 'packageName':packageName, 'importName':importName}
    r = apiManager.post('/compute/addPackage', body, token)
    return r


def execute(clusterId, f, params, token):
    clusterId = sanitize.validUuid('clusterId', clusterId, True)
    token = sanitize.validString('token', token, True)

    f_bytes = pickle.dumps(f)
    f_string = f_bytes.decode("Windows-1252")

    params_bytes = pickle.dumps(params)
    params_string = params_bytes.decode("Windows-1252")


    body = {'clusterId':clusterId, 'params':params_string, 'f':f_string}
    r = apiManager.post('/compute/execute', body, token)
    r = r['results']
    results = []
    for x in r:
        x = x.encode("Windows-1252")
        x = pickle.loads(x)
        results = results + [x]

    return results

def removeCluster(clusterId, token):
    clusterId = sanitize.validUuid('clusterId', clusterId, True)
    token = sanitize.validString('token', token, True)
    body = {'clusterId':clusterId}
    r = apiManager.delete('/compute/cluster', body, token)
    return r

def listClusters(token):
    token = sanitize.validString('token', token, True)
    r = apiManager.get('/compute/cluster', {}, token)
    return r



