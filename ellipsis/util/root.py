import geopandas as gpd
from shapely.geometry import Polygon
from geopy.distance import geodesic
import numpy as np
import pandas as pd
import math
import sys
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image

from ellipsis import sanitize


def recurse(f, body, listAll, extraKey = None):
    
    r = f(body)
    if listAll:
        nextPageStart = r['nextPageStart']
        while nextPageStart != None:
            body['pageStart'] = nextPageStart
            r_new = f(body)
            nextPageStart = r_new['nextPageStart']
            if 'size' in r.keys():
                r['size'] = r['size'] + r_new['size']
            if extraKey == None:
                r['result'] =  r['result'] + r_new['result']
            else:
                r['result'][extraKey] = r['result'][extraKey] +  r_new['result'][extraKey]
                
        r['nextPageStart'] = None
    return r


def stringToDate(date):
    date = sanitize.validString('date', date, True)

    try:
        d = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        try:
            d = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        except:
            d = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    return d

def dateToString(date):
    date = sanitize.validDate('date', date , True)
    
    d = date.strftime(date, "%Y-%m-%d %H:%M:%S.%fZ")
    return d

def plotRaster(raster):
    raster = sanitize.validNumpyArray('raster', raster, True)

    if len(raster.shape) != 3:
        raise ValueError('raster must have 3 dimensions')

    if raster.shape[0] != 1 and raster.shape[0] != 3:
        raise ValueError('raster must have either 1 band or 3 bands')

    

    if raster.shape[0] ==3:
        raster = np.transpose(raster, [1,2,0])
        minimum = np.min(raster)
        maximum = np.max(raster)
        if minimum == maximum:
            maximum = minimum + 1
        raster = raster - minimum
        raster = raster / (maximum-minimum)
        raster = raster * 255
        image = Image.fromarray(raster.astype('uint8'))
        image.show()

    else:
        plt.imshow(raster[0,:,:], interpolation='none')
        plt.show()
    
def plotFeatures(features):
    features = sanitize.validGeopandas('features', features, True)
    features.plot()


def chunks(l, n = 3000):
    l = sanitize.validList('l', l, True)
    n = sanitize.validInt('n', n , False)
    result = list()
    for i in range(0, len(l), n):
        result.append(l[i:i+n])
    return(result)
    

 
def cover(bounds, w):
    
    w = sanitize.validInt('w',w, True)
    bounds = sanitize.validBounds('bounds',bounds, True)

    x1 = bounds['xMin']
    y1 = bounds['yMin']
    x2 = bounds['xMax']
    y2  = bounds['yMax']

    step_y =  w/geodesic((y1,x1), (y1 - 1,x1)).meters
    parts_y = math.floor((y2 - y1)/ step_y + 1)

    y1_vec = y1 + np.arange(0, parts_y )*step_y
    y2_vec = y1 + np.arange(1, parts_y +1 )*step_y
        
    steps_x = [   w/geodesic((y,x1), (y,x1+1)).meters for y in y1_vec  ]

    parts_x = [math.floor( (x2-x1) /step +1 ) for step in steps_x ]      
        

    coords = pd.DataFrame()
    for n in np.arange(len(parts_x)):
        x1_sq = [ x1 + j*steps_x[n] for j in np.arange(0,parts_x[n]) ]
        x2_sq = [ x1 + j*steps_x[n] for j in np.arange(1, parts_x[n]+1) ]
        coords_temp = {'x1': x1_sq, 'x2': x2_sq, 'y1': y1_vec[n], 'y2':y2_vec[n]}
        coords = coords.append(pd.DataFrame(coords_temp))

    cover = [Polygon([ (coords['x1'].iloc[j] , coords['y1'].iloc[j]) , (coords['x2'].iloc[j] , coords['y1'].iloc[j]), (coords['x2'].iloc[j] , coords['y2'].iloc[j]), (coords['x1'].iloc[j] , coords['y2'].iloc[j]) ]) for j in np.arange(coords.shape[0])]
     


    coords = gpd.GeoDataFrame({'geometry': cover, 'x1':coords['x1'], 'x2':coords['x2'], 'y1':coords['y1'], 'y2':coords['y2'] })

    coords.crs = {'init': 'epsg:4326'}

    return(coords)
    

    
def loadingBar(count,total):
    
    count = sanitize.validInt('count', count, True)
    total = sanitize.validInt('total', total, True)
    
    if total == 0:
        return
    else:
        percent = float(count)/float(total)*100
        sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent) + ' '*(100-int(percent)) + ']')
