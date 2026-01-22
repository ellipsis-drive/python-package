def blackBoxVectorExtraction(outputRasters, extent):
    import numpy as np
    from skimage.transform import resize
    from shapely.geometry import Point
    import geopandas as gpd

    out = outputRasters[0]['raster'][1,:,:]
    out = np.squeeze(out)
    for r in outputRasters:
        r = r['raster'][0,:,:]
        r = np.squeeze(r)
        r = resize(r, (out.shape[0], out.shape[1]), order=0, preserve_range=True, mode='edge')
        out = out + r
    out = np.floor(out)
    out = out %3

    indices = np.where(out ==2)

    coordsX = [extent['xMin'] + (extent['xMax'] - extent['xMin']) * x / out.shape[0] for x in indices[0]  ]
    coordsY = [extent['yMin'] + (extent['yMax'] - extent['yMin']) * y / out.shape[1] for y in indices[1]  ]

    points = [Point(p) for p in zip(coordsX, coordsY)]
    sh = gpd.GeoDataFrame({'geometry': points })
    return sh




import ellipsis as el

token = el.account.logIn('demo_user', 'demo_user')


extent = {"xMin":5.06243,"yMin":52.083825,"xMax":5.065256,"yMax":52.08491}

results = el.path.search(pathTypes=['raster'], root=['myDrive', 'sharedWithMe'], resolution={'min':0, 'max':1}, extent = extent, token = token)['result']

outputRasters = []
for result in results:
    layerId = result['id']
    timestampId = result['raster']['timestamps'][0]['id']
    print('fetching', result['name'])
    out = el.path.raster.timestamp.getRaster(pathId = layerId, timestampId=timestampId, extent = extent, epsg = 4326, token=token)
    outputRasters = outputRasters + [out]

sh = blackBoxVectorExtraction(outputRasters, extent)

projectFolderId = '4a7e0bc8-c044-4ba2-b3ec-5bd7b1fc09d8'

targetLayerId = el.path.vector.add('extracted vectors', token = token, parentId=projectFolderId)['id']
targetTimestampId = el.path.vector.timestamp.add(pathId = targetLayerId, token= token)['id']

el.path.vector.timestamp.feature.add(pathId = targetLayerId, timestampId=targetTimestampId, features=sh, token = token)



############

extent={"xMin":-2.978171,"yMin":43.226417,"xMax":-2.869982,"yMax":43.2926}

results = el.path.search(pathTypes=['raster'], root=['myDrive', 'sharedWithMe'], resolution={'min':0, 'max':11}, extent = extent, token = token)['result']

layers = [{'timestampId': r['raster']['timestamps'][0]['id'] , 'pathId': r['id'] } for r in results]

requirements = ['numpy', 'shapely', 'geopandas', 'ellipsis', 'scikit-image']

targetLayerId = el.path.vector.add(name = 'large extent output', token = token, parentId=projectFolderId)['id']
targetTimestampId = el.path.vector.timestamp.add(pathId=targetLayerId, token=token)['id']

computeId = el.compute.createCompute(layers=layers, requirements=requirements, token=token, largeResult=True, nodes=3)['id']

def f(params):
    import io
    import numpy as np
    import ellipsis as el

    outputRasters = [params[k] for k in params]
    extent = {"xMin": -2.978171, "yMin": 43.226417, "xMax": -2.869982, "yMax": 43.2926}

    def blackBoxVectorExtraction(outputRasters):
        import numpy as np
        from skimage.transform import resize
        from shapely.geometry import Point
        import geopandas as gpd
        extent = outputRasters[0]['extent']
        out = outputRasters[0]['raster'][1,:,:]
        out = np.squeeze(out)
        for r in outputRasters:
            r = r['raster'][0,:,:]
            r = np.squeeze(r)
            r = resize(r, (out.shape[0], out.shape[1]), order=0, preserve_range=True, mode='edge')
            out = out + r
        out = np.floor(out)
        out = out %3

        indices = np.where(out ==2)

        coordsX = [extent['xMin'] + (extent['xMax'] - extent['xMin']) * x / out.shape[0] for x in indices[0]  ]
        coordsY = [extent['yMin'] + (extent['yMax'] - extent['yMin']) * y / out.shape[1] for y in indices[1]  ]

        points = [Point(p) for p in zip(coordsX, coordsY)]
        sh = gpd.GeoDataFrame({'geometry': points })
        return sh

    sh = blackBoxVectorExtraction(outputRasters)
    sh.crs = 'EPSG:3857'
    sh = sh.to_crs('EPSG:4326')
    sh = sh[  np.logical_and(  np.logical_and( sh.bounds['minx'] < extent['xMax'], sh.bounds['maxx'] > extent['xMin']  ), np.logical_and( sh.bounds['miny'] < extent['yMax'], sh.bounds['maxy'] > extent['yMin']  ))  ]

    memfile = io.BytesIO()

    outFile = el.util.saveVector(targetFile=memfile, features=sh)
    return outFile


el.compute.execute(computeId=computeId, f=f, token=token, writeToLayer={'pathId': targetLayerId, 'timestampId':targetTimestampId, 'file': {'format' :'gpkg'}})

el.compute.terminateCompute(computeId=computeId, token=token)

el.compute.terminateAll(token=token)

