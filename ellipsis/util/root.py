import geopandas as gpd
from shapely.geometry import Polygon
from geopy.distance import geodesic
import numpy as np
import pandas as pd
import math
import sys
from datetime import datetime
from shapely import geometry
import rasterio
import matplotlib.pyplot as plt
from PIL import Image
from skimage.transform import resize
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor as Pool
import multiprocessing
import warnings

from ellipsis import sanitize
from rasterio.warp import reproject as warp, Resampling, calculate_default_transform

warnings.simplefilter("ignore")


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

    if len(raster.shape) != 3 and len(raster.shape) != 2:
        raise ValueError('raster must have 2 or 3 dimensions')

    if len(raster.shape) == 2:
        raster = np.expand_dims(raster, 0)

    

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
    
def plotVector(features):
    features = sanitize.validGeopandas('features', features, True)
    features.plot()


def chunks(l, n = 3000):
    l = sanitize.validList('l', l, True)
    n = sanitize.validInt('n', n , False)
    result = list()
    for i in range(0, len(l), n):
        result.append(l[i:i+n])
    return(result)
    

 
def cover(bounds, width):
    w = width
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

    coords.crs = 'epsg:4326'

    return(coords)
    

    
def loadingBar(count,total):
    
    count = sanitize.validInt('count', count, True)
    total = sanitize.validInt('total', total, True)
    
    if total == 0:
        return
    else:
        percent = float(count)/float(total)*100
        sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent) + ' '*(100-int(percent)) + ']')


def reprojectRaster(r, sourceExtent, targetExtent, targetWidth, targetHeight, sourceEpsg, targetEpsg, interpolation = 'nearest'):
    
    sanitize.validNumpyArray('r', r, True)
    targetExtent, targetCrs = sanitize.validBoundsCrsCombination(['targetExtent', 'targetEpsg'], [targetExtent, 'EPSG:' + str(targetEpsg)], True)
    sourceExtent, sourceCrs = sanitize.validBoundsCrsCombination(['sourceExtent', 'sourceEpsg'], [sourceExtent, 'EPSG:' + str(sourceEpsg)], True)
    targetWidth = sanitize.validInt('targetWidth', targetWidth, True)
    targetHeight = sanitize.validInt('targetHeight', targetHeight, True)
    interpolation = sanitize.validString('interpolation', interpolation, True)
    
    if not interpolation in ['nearest', 'bilinear']:
        raise ValueError('interpolation must be one of nearest or bilinear')
    
    if len(r.shape) !=3:
        raise ValueError('r must be 3 dimensional')
    if interpolation != 'nearest' and interpolation != 'linear':
        raise ValueError('interpolation must be either nearest or linear')
        
        

    src_transform = rasterio.transform.from_bounds(sourceExtent['xMin'], sourceExtent['yMin'], sourceExtent['xMax'], sourceExtent['yMax'], r.shape[2], r.shape[1])
    dst_transform = rasterio.transform.from_bounds(targetExtent['xMin'], targetExtent['yMin'], targetExtent['xMax'], targetExtent['yMax'], targetWidth, targetHeight)
    destination = np.zeros((r.shape[0],targetHeight,targetWidth))

    if interpolation == 'nearest':
        interpolation = Resampling.nearest        
    else:
        interpolation = Resampling.bilinear

    for i in np.arange(r.shape[0]):
        warp(
            r[i,:,:],
            destination[i,:,:],
            src_transform=src_transform,
            src_crs=sourceCrs,
            dst_transform=dst_transform,
            dst_crs=targetCrs,
            resampling=interpolation)
    

    return {'raster':destination, 'transform':dst_transform, 'extent':targetExtent, 'epsg':targetEpsg}


def swapXY(extent):
    return {'xMin': extent['yMin'], 'xMax':extent['yMax'], 'yMin':extent['xMin'], 'yMax':extent['xMax']}


def transformPoint( point, sourceEpsg, targetEpsg):
    sourceCrs = 'EPSG:' + str(sourceEpsg)
    targetCrs = 'EPSG:' + str(targetEpsg)

    try:
        point = geometry.Point(point)
    except:
        raise ValueError('point must be a tuple with two floats')
    df = gpd.GeoDataFrame({'geometry':[point]})    
    try:
        df.crs = sourceCrs
    except:
        raise ValueError('sourceCrs not a valid crs')
    try:
        df = df.to_crs(targetCrs)
    except:
        raise ValueError('targetCrs not a valid crs')
    x = df.bounds['minx'].values[0]
    y = df.bounds['miny'].values[0]

    return(x,y)

#funciton to store image given bounds, and raster and crs
def saveRaster(targetFile, r, epsg, extent = None, transform = None):
    
    if type(extent) == type(None) and type(transform) == type(None):
        raise ValueError('You must provide either an extent or a transform')
        
    crs = 'EPSG:' + str(epsg)
    if type(extent) != type(None):
        sanitize.validBoundsCrsCombination([extent, crs], [extent, crs], True)
        
    r = sanitize.validNumpyArray('r', r, True)
    
    if len(r.shape) != 3:
        raise ValueError('r must be 3 dimensional')

    w = r.shape[2]
    h = r.shape[1]
    if transform == None:
        transform = rasterio.transform.from_bounds(extent['xMin'], extent['yMin'], extent['xMax'], extent['yMax'], w, h)
    con = rasterio.open(targetFile , 'w', driver='Gtiff',compress="lzw",
                    height = h, width = w,
                    count= r.shape[0], dtype=r.dtype,
                    crs=  crs ,
                    transform=transform)
    
    con.write(r)
    con.close()

def saveVector(targetFile, features):
    features.to_file(targetFile)


q_running = multiprocessing.Queue()

def cutIntoTiles(features, zoom, cores = 1, buffer = 0):
    features, bounds = reprojectWithBounds(sh = features, targetCrs = 'EPSG:3857', cores= cores)
    count  = features.shape[0]

    LEN = 2.003751e+07
    tile = {'xMin' : -LEN, 'xMax': LEN, 'yMin':-LEN, 'yMax':LEN} 
    args = (tile, 0, zoom, features, bounds, cores, buffer, count)
    sh_end = manageTile(args)

    return sh_end
    
    

def manageTile(args):
    tile, depth, zoom, sh, bounds, cores, buffer, count = args
    if zoom == depth:
        return sh

    newTiles = splitTile(tile, buffer)
    shs = []
    tile = newTiles[0]
    args = []
    maxCount = 0
    for tile in newTiles:        
        sh_new, bounds_new = cut(sh, bounds, tile)
        if sh_new.shape[0] > maxCount:
            maxCount = sh_new.shape[0]
        if sh_new.shape[0] > 0:
            args = args + [(tile, depth+1, zoom, sh_new, bounds_new, cores, buffer, count)]
    
    
    if q_running.qsize() < cores -1 and  count * 0.2 > maxCount :
        q_running.put('x')        
        with Pool(4) as p:
            shs = p.map(manageTile, args)
        shs = list(shs)
        q_running.get()
    else:
        for arg in args:
            sh_new = manageTile(arg)
            shs = shs + [sh_new]
        
        
    sh_total = pd.concat(shs)
    return sh_total


def cut(sh, bounds, tile):
        #remove things without
        isWithout = np.logical_or( np.logical_or(bounds['minx'].values > tile['xMax'],bounds['maxx'].values < tile['xMin'] ), np.logical_or(bounds['miny'].values > tile['yMax'],bounds['maxy'].values < tile['yMin'] ))
                
        sh_inside = sh[ np.logical_not( isWithout) ]
        bounds_inside = bounds[np.logical_not( isWithout)]
        
        #remove things within
        isWithinX = np.logical_and( np.logical_and(bounds_inside['minx'].values < tile['xMax'],bounds_inside['minx'].values > tile['xMin'] ), np.logical_and(bounds_inside['maxx'].values < tile['xMax'],bounds_inside['maxx'].values > tile['xMin'] ))
        isWithinY = np.logical_and( np.logical_and(bounds_inside['miny'].values < tile['yMax'],bounds_inside['miny'].values > tile['yMin'] ), np.logical_and(bounds_inside['maxy'].values < tile['yMax'],bounds_inside['maxy'].values > tile['yMin'] ))
        isWithin = np.logical_and(isWithinX, isWithinY)

        sh_within = sh_inside[isWithin]        
        bounds_within = bounds_inside[isWithin]
        
        #now intersect
        sh_intersects = sh_inside[np.logical_not(isWithin)]
        poly = tileToPolygon(tile)
        sh_intersects['geometry'] = sh_intersects.intersection(poly)
        bounds_intersects = sh_intersects.bounds

        sh_result = pd.concat([sh_intersects, sh_within])
        bounds_result = pd.concat([bounds_intersects, bounds_within])


        return sh_result, bounds_result

def tileToPolygon(tile):
    return geometry.Polygon([ (tile['xMin'], tile['yMin']), (tile['xMin'], tile['yMax']), (tile['xMax'], tile['yMax']), (tile['xMax'], tile['yMin']) ])    
    

def splitTile(tile, buffer):
    
    b = buffer * (tile['xMax'] - tile['xMin'])
    xMiddle = tile['xMin'] + (tile['xMax'] - tile['xMin'])/2
    yMiddle = tile['yMin'] + (tile['yMax'] - tile['yMin'])/2
    yMin = tile['yMin']
    xMin = tile['xMin']
    yMax = tile['yMax']
    xMax = tile['xMax']
    
    
    T1 = {'xMin': xMin -b, 'xMax':xMiddle+b, 'yMin': yMin-b, 'yMax': yMiddle+b  }
    T2 = {'xMin': xMin-b, 'xMax':xMiddle+b, 'yMin': yMiddle-b, 'yMax': yMax+b  }
    
    T3 = {'xMin': xMiddle-b, 'xMax':xMax+b, 'yMin': yMin-b, 'yMax': yMiddle+b  }
    T4 = {'xMin': xMiddle-b, 'xMax':xMax+b, 'yMin': yMiddle-b, 'yMax': yMax+b  }
    
    
    return [T1, T2, T3, T4]

    

def reprojectVector(features, targetEpsg, cores = 1):
    sh = features
    targetCrs = 'EPSG:' + str(targetEpsg)
    shs = np.array_split(sh, cores)
    args = list(zip(shs, np.repeat(targetCrs, cores) ))
    with Pool(cores) as p:
        shs = p.map(reprojectSub, args )
    
    sh = pd.concat([x[0] for x in shs])
    return sh

def reprojectWithBounds(sh, targetCrs, cores = 1):

    N = max(round(sh.shape[0]/ 50000),1)
    
    shs_1 = np.array_split(sh, N)
    shs_total = []
    for sh in shs_1:
        shs = np.array_split(sh, cores)
        args = list(zip(shs, np.repeat(targetCrs, cores) ))
        with Pool(cores) as p:
            shs = p.map(reprojectSub, args )
        shs = list(shs)
        shs_total = shs_total + shs
        
    sh = pd.concat([x[0] for x in shs_total])
    bounds = pd.concat([x[1] for x in shs_total])
    return sh, bounds


def reprojectSub(args):
    sh = args[0]
    targetCrs = args[1]
    sh = sh.to_crs(targetCrs)
    sh['geometry'] = sh.buffer(0)
    sh = sh[sh.is_valid]
    sh = sh[ np.logical_not(sh.is_empty)]
    bounds = sh.bounds
    
    return sh, bounds



def getActualExtent(minx, maxx, miny, maxy, crs):
    
    LEN = 2.003751e+07
    STEPS = 10
    
    x_step = (maxx - minx) / STEPS
    y_step = (maxy - miny) / STEPS
    
    points = [ geometry.Point((minx + (i) * x_step, miny + (j) * y_step))  for i in np.arange(STEPS+1) for j in np.arange(STEPS+1)]
    df = gpd.GeoDataFrame({'geometry':points})
    try:
        df.crs =  crs
    except:
        return {'status': 400, 'message': 'Invalid epsg code'}
        
    try:
        df_wgs = df.to_crs('EPSG:3857')
    except:
        return {'status': 400, 'message': 'Invalid extent and epsg combination'}


    #in case points fall outside defined area we restrict to the -85, 85, 180, -180 region
    xs = df_wgs.bounds['minx'].values
    ys = df_wgs.bounds['miny'].values
    xs[xs == np.inf] = LEN    
    xs[xs == -np.inf] = -LEN    
    ys[ys == np.inf] = LEN    
    ys[ys == -np.inf] = -LEN    
    
    minX = np.min(xs)
    maxX = np.max(xs)
    minY = np.min(ys)
    maxY = np.max(ys)

    minX = max(-LEN, minX)
    maxX = min(LEN, maxX)
    minY = max(-LEN, minY)
    maxY = min(LEN, maxY)
    
    
    
    return {'status': 200, 'message': {'xMin':minX, 'xMax': maxX, 'yMin': minY, 'yMax':maxY}}
    
