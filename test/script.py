import ellipsis as el

el.apiManager.baseUrl =  'https://api.tnc.ellipsis-drive.com/v3'



pageStart = '0ebcf770-5806-469a-a91e-55e8c69bc05d'


while True:
    results = el.path.search( pathTypes=['raster', 'vector', 'file'], listAll=False, token = token, pageStart= pageStart, root=['sharedWithMe'])
    pageStart = results['nextPageStart']
    print(pageStart)
    result = results['result']
    r = result[0]
    for r in result:
        h = r['driveLocation']['path'][-2]['name']
        h = h.replace('_','')
        pathId = r['id']
        print(h)
        try:
            el.path.hashtag.add(pathId = pathId, hashtag=h, token=token)
        except Exception as e:
            print(e)












