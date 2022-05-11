import util

# TODO: implement all possible parameters?

# opdelen in stukken, path.searchRaster path.searchVector path.searchFolder

# read the docs

def searchPaths(name = None, fuzzySearchOnName = False, root = ['myDrive', 'sharedWithMe', 'favorite'], firstPageOnly = True, bounds = None, userId= None, resolution=None,  dateFrom=None, dateTo= None, hashtag = None, token = None):
    body = {'root': root, 'pageSize':20}

    if name is not None:
        body['name'] = name

    body['fuzzySearchOnName'] = fuzzySearchOnName        

    if userId is not None:
        body['userId'] = userId

    if dateFrom is not None:
        body['dateFrom'] = dateFrom.strftime('%Y-%m-%d %H:%M:%S')

    if dateTo is not None:
        body['dateTo'] = dateTo.strftime('%Y-%m-%d %H:%M:%S')

    if resolution is not None:
        body['resolution'] = resolution

    if hashtag is not None:
        body['hashtag'] = hashtag

    if bounds is not None:
        bounds = {'xMin':float(bounds['xMin']), 'xMax':float(bounds['xMax']), 'yMin':float(bounds['yMin']), 'yMax':float(bounds['yMax'])}
        body['bounds'] = bounds

    keepGoing = True
    results = []
    while keepGoing:
        if token == None:
            r = s.get(url + '/path?' + urllib.parse.urlencode(body) )
        else:
            r = s.get(url + '/path?' + urllib.parse.urlencode(body), headers = {"Authorization":token} )
        
        if r.status_code != 200:
            raise ValueError(r.text)
            
        result = r.json()
        body['pageStart'] = result['nextPageStart']

        results = results + result['result']
        result = result['result']

        if firstPageOnly:
            keepGoing = False
        if len(result) < 20:
            keepGoing = False
        results = results + result


    return(results)