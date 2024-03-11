from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.util.root import recurse

def listViews(token):

    token = sanitize.validString('token', token, True)



    r = apiManager.get('/view', {}, token)

    return r

def get(viewId, token=None):
    token = sanitize.validString('token', token, False)
    viewId = sanitize.validString('viewId', viewId, True)

    r = apiManager.get('/view/' + viewId, {}, token)
        
    return r



def add(pathId, layers, name = None, persistent=False, dems=[], token = None):
    token = sanitize.validString('token', token, False)
    pathId = sanitize.validString('pathId', pathId, True)
    layers = sanitize.validObject('layers', layers, True)
    dems = sanitize.validObject('dems', dems, True)
    name = sanitize.validString('pathId', name, False)
    persistent = sanitize.validBool('persistent', persistent, True)

    r = apiManager.post('/view', {'name':name, 'layers':layers, 'dems':dems, 'pathId':pathId, 'persistent':persistent}, token)
        
    return r


def edit(viewId, token, layers=None, name=None, dems=None):
    viewId = sanitize.validString('viewId', viewId, True)
    token = sanitize.validString('token', token, False)
    layers = sanitize.validObject('layers', layers, False)
    dems = sanitize.validObject('dems', dems, False)
    name = sanitize.validString('pathId', name, False)

    r = apiManager.patch('/view/' + viewId, {'layers':layers, 'dems':dems, 'name':name}, token)
        
    return r



def delete(viewId, token):
    viewId = sanitize.validString('viewId', viewId, True)
    token = sanitize.validString('token', token, False)

    r = apiManager.delete('/view/' + viewId, {}, token)

        
    return r

