from ellipsis import apiManager
from ellipsis import sanitize



def editFilter(pathId, propertyFilter, token):
    pathId = sanitize.validUuid('pathId', pathId, True) 
    token = sanitize.validString('token', token, True)
    propertyFilter = sanitize.validObject('propertyFilter', propertyFilter, True)
    
    body = {'filter': propertyFilter}
    r = apiManager.post('/path/' + pathId + '/vector/filter' , body, token)
    return r



