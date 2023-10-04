import pandas as pd
import numpy as np

import ellipsis as el
import laspy

pathId = 'd5ea21a4-26a1-4bba-8571-0c487b20c358'
timestampId = '0c367783-613f-4f09-bfa4-6af74867fd7a'
epsg = 32618

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))



nextPageStart = None
firstTime = True
N=0

while type(nextPageStart) != None or firstTime:
    firstTime = False
    ps = []
    N = N +1
    for i in range(200):
        print('HOI')
        extra_points = el.path.vector.timestamp.listFeatures(pathId=pathId, timestampId=timestampId, listAll=False, pageStart=nextPageStart)
        nextPageStart = extra_points['nextPageStart']
        ps = ps + [extra_points['result']]
        print('nextPageStart',nextPageStart)


    all_points = pd.concat(ps)
    print('trying to facking prin this')
    print(all_points.shape[0])
    print('printed')
    all_points = all_points.to_crs('EPSG:' + str(epsg))

    points = [p.coords._coords[0] for p in all_points['geometry'].values ]
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    z = [p[2] for p in points]
    print('len points', len(x))
    colors = [hex_to_rgb(c) for c in all_points['color'].values ]

    r = [c[0]*255 for c in colors]
    g = [c[1]*255 for c in colors]
    b = [c[2]*255 for c in colors]

    print('len colors', len(r))

    las = laspy.create(point_format=2, file_version='1.2')
    las.x = x
    las.y = y
    las.z = z
    las.red = r
    las.green = g
    las.blue = b
    las.write('/home/daniel/Downloads/output/' + str(N) + '.las')


