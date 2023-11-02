

import ellipsis as el
import pandas as pd
import numpy as np
import shapely
import geopandas as gpd
from datetime import datetime
import random

def makeStyle(p,sh):
    colors = ["#2A5C84","#74AE56","#FFE733","#FF8C01","#ED2938"]
    max_value = np.max(sh[p].values)
    min_value = np.min(sh[p].values)
    N = 5
    step = (max_value-min_value) /(N-1)
    values = [min_value + step*i for i in np.arange(N) ]
    transitionPoints = [{'color':x[0], 'value':x[1]  } for x in zip(colors, values)]

    style={"method":"transitionPoints","parameters":{"alpha":0.5,"width":2,"radius":{"method":"constant","parameters":{"value":6}},"defaultColor":"#c75b1c","property":p,"continuous":True,"transitionPoints":transitionPoints}}

    return style


def main():
    token  = el.account.logIn('demo_user', 'demo_user')

    file = '/home/daniel/Downloads/Data_Sample2.csv'
    t = pd.read_csv(file)

    #in the first step I make my geometries base on the points
    points = [shapely.geometry.point.Point((t['  X'].values[i], t['  Y'].values[i], t['Z'].values[i])) for i in np.arange(t.shape[0])]
    sh = gpd.GeoDataFrame({ 'geometry':points})
    sh['altitude'] = t['Z']
    sh['displacement'] = t['23-10-23']
    sh.crs = 'EPSG:32755'

    #I create the layer within ED
    pathId = el.path.vector.add(str(random.randint(0, 999999999)), token)['id']
    timestampId = el.path.vector.timestamp.add(pathId = pathId, token = token)['id']

    #I add the geometries to the layer
    featureIds = el.path.vector.timestamp.feature.add(pathId = pathId, timestampId=timestampId, token = token, features=sh)
    t['featureId'] = featureIds

    #lastly I create a table containing time, value and featureId to encode the time series

    del t['  X']
    del t['  Y']
    del t['Z']
    del t['Index']


    seriesData = []
    for c in t.columns:
        if c != 'featureId':
             t_temp = pd.DataFrame({'featureId': t['featureId'].values, 'displacement': t[c]})
             t_temp['date'] = datetime.strptime(c,"%y-%M-%d")
             seriesData = seriesData + [t_temp]

    seriesData = pd.concat(seriesData)

    el.path.vector.timestamp.feature.series.add(pathId = pathId, timestampId=timestampId, token = token, seriesData=seriesData)


    #as a last extra step I will add some styling to the layer

    #one for absolute altitude

    p = 'altitude'
    style = makeStyle(p,sh)
    el.path.vector.style.add(name = p, pathId = pathId,method = style['method'], parameters=style['parameters'], token = token )

    p = 'displacement'
    style = makeStyle(p,sh)
    el.path.vector.style.add(name = p, pathId = pathId,method = style['method'], parameters=style['parameters'], token = token )


main()





