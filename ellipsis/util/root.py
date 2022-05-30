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
from ellipsis import sanitize
from rasterio.warp import reproject as warp, Resampling, calculate_default_transform


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


def reprojectRaster(r, sourceExtent, targetExtent, targetWidth, targetHeight, targetCrs, tempFolder, interpolation = 'nearest'):
    
    sanitize.validNumpyArray('r', r, True)
    targetExtent, targetCrs = sanitize.validBoundsCrsCombination(['targetExtent', 'targetCrs'], [targetExtent, targetCrs], True)
    tempFolder = sanitize.validString('tempFolder', tempFolder, True)
    targetWidth = sanitize.validInt('targetWidth', targetWidth, True)
    targetHeight = sanitize.validInt('targetHeight', targetHeight, True)
    interpolation = sanitize.validString('interpolation', interpolation, True)
    
    if not os.path.exists(tempFolder):
        raise ValueError(tempFolder + ' not found')
    if not os.path.isdir(tempFolder):
        raise ValueError(tempFolder + ' must be a path to a folder')
    if len(r.shape) !=3:
        raise ValueError('r must be 3 dimensional')
    if interpolation != 'nearest' and interpolation != 'linear':
        raise ValueError('interpolation must be either nearest or linear')
        
    dtype = r.dtype
    def mercatorBlowUp(y):
       factor = math.cos(y * 2 * math.pi/360)
       return(factor)    
    ###STEP 1
    #calculate zoom
    target_tile = geometry.Polygon([(targetExtent['xMin'],targetExtent['yMin']), (targetExtent['xMin'],targetExtent['yMax']), (targetExtent['xMax'],targetExtent['yMax']), (targetExtent['xMax'], targetExtent['yMin'])])
    target_tile = gpd.GeoDataFrame({"geometry": [target_tile]})
    target_tile.crs = targetCrs
    
    wgs_tile = target_tile.to_crs('epsg:4326')
    minx_wgs = wgs_tile.bounds['minx'].values[0]
    miny_wgs = wgs_tile.bounds['miny'].values[0]
    maxx_wgs = wgs_tile.bounds['maxx'].values[0]
    maxy_wgs = wgs_tile.bounds['maxy'].values[0]
    if minx_wgs < -180 or maxx_wgs > 180 or miny_wgs < -85 or maxy_wgs > 85:
        raise ValueError('Bounds must be within 85 degrees south and 85 degrees north')
    native_transform = rasterio.transform.from_bounds(targetExtent['xMin'], targetExtent['yMin'], targetExtent['xMax'], targetExtent['yMax'], targetWidth, targetHeight)
    source_transform = rasterio.transform.from_bounds(sourceExtent['xMin'], sourceExtent['yMin'], sourceExtent['xMax'], sourceExtent['yMax'], r.shape[2], r.shape[1])


    M = [[native_transform[0], native_transform[1]] , [native_transform[3], native_transform[4]] ]
    bias = [native_transform[2], native_transform[5]]
    Minv = np.linalg.inv(M)

    x_res, y_res = getResolution(minx_wgs, maxx_wgs, miny_wgs, maxy_wgs, targetCrs, Minv, bias)
    resolution = min(x_res, y_res)
    zoom = math.log(40000000 / (resolution*256 )) / math.log(2)
    zoom = math.floor(zoom + 1) #+ 0.85)
    
    zoom = zoom -5
    zoom = max(0, zoom)

    #####STEP 2    
    #step 1 on create raster of zoom - 4 blocks
    source_tile = geometry.Polygon([(sourceExtent['xMin'],sourceExtent['yMin']), (sourceExtent['xMin'],sourceExtent['yMax']), (sourceExtent['xMax'],sourceExtent['yMax']), (sourceExtent['xMax'], sourceExtent['yMin'])])
    source_tile = gpd.GeoDataFrame({"geometry": [source_tile]})
    source_tile.crs = 'epsg:3857'
    
    minx_merc_target = source_tile.bounds['minx'].values[0]
    miny_merc_target = source_tile.bounds['miny'].values[0]
    maxx_merc_target = source_tile.bounds['maxx'].values[0]
    maxy_merc_target = source_tile.bounds['maxy'].values[0]

    LEN = 2.003751e+07

    x_start = 2**zoom * (minx_merc_target + LEN) / (2* LEN)
    x_end = 2**zoom * (maxx_merc_target + LEN) / (2* LEN)
    y_start = 2**zoom * (miny_merc_target + LEN) / (2* LEN)
    y_end = 2**zoom * (maxy_merc_target + LEN) / (2* LEN)

    x1_osm = math.floor(x_start)
    x2_osm = math.floor(x_end)
    y1_osm = math.floor(y_start)
    y2_osm = math.floor(y_end)
    
    raster_merc_x1 = 2*LEN * x1_osm /2**zoom - LEN 
    raster_merc_x2 = 2*LEN * (x2_osm+1) /2**zoom - LEN 
    raster_merc_y1 = 2*LEN * y1_osm /2**zoom - LEN 
    raster_merc_y2 = 2*LEN * (y2_osm +1) /2**zoom - LEN 
    bounds_mercator = {'xMin': raster_merc_x1,'xMax': raster_merc_x2, 'yMin': raster_merc_y1, 'yMax': raster_merc_y2 }
    
        

    w = (x2_osm - x1_osm + 1) * 256*2**5
    h = (y2_osm - y1_osm + 1) * 256*2**5
    
    raster = np.zeros((r.shape[0], h, w), dtype = dtype)

    ###STEP 2    
    #place r on this raster
    x_frac = (x_start - x1_osm) / (x2_osm - x1_osm + 1)
    y_frac = (y2_osm + 1 - y_end) / (y2_osm - y1_osm + 1)
    
    #######33
    full_raster_tile = geometry.Polygon([(raster_merc_x1,raster_merc_y1), (raster_merc_x1, raster_merc_y2), (raster_merc_x2, raster_merc_y2), (raster_merc_x2, raster_merc_y1)])
    full_raster_tile = gpd.GeoDataFrame({"geometry": [full_raster_tile]})
    full_raster_tile.crs = 'EPSG:3857'
    
    xStart = math.floor(w * x_frac)
    xEnd = xStart + r.shape[2]
    yStart = math.floor(h * y_frac)
    yEnd = yStart + r.shape[1]
    
    
    ############################

    newW, newH = getVirtualSize(bounds_mercator, targetCrs, native_transform)
    
    
    
    if 'float' in str(dtype).lower():
        raster[:,:,:] = np.nan
    raster[:, yStart:yEnd,xStart:xEnd] = r


    ##interpolation work
    if interpolation == 'linear':
        order = 1
        resampleMethod = Resampling.bilinear
        interpolationString = '-r bilinear '
    else:
        order = 0
        resampleMethod = Resampling.nearest
        interpolationString = '-r near '
    

    ####STEP 3
    #resize

    raster = np.transpose(raster, [1,2,0])
    raster = resize(raster, ( newH, newW), anti_aliasing= False, order = order, mode = 'edge',preserve_range=True)
    raster = np.transpose(raster, [2,0,1])
    raster = raster.astype(dtype)
    saveRaster( targetFile =  os.path.join(tempFolder,'resized_temp.tif'), r = raster, extent = bounds_mercator, crs = 'EPSG:3857')



    ####step 6 gdalwarp on smaller raster
    
    extent = '-te ' + str(targetExtent['xMin']) + ' ' + str(targetExtent['yMin']) + ' ' + str(targetExtent['xMax']) + ' ' + str(targetExtent['yMax']) + " "
    outsize = '-ts ' + str(targetWidth) + ' ' + str(targetHeight) + " "
    epsgString = " -t_srs " + targetCrs + " "
    

    cmd = "gdalwarp -overwrite " + outsize + interpolationString  +  extent + " -s_srs EPSG:3857 " + epsgString + os.path.join(tempFolder,'resized_temp.tif') + " " + os.path.join(tempFolder, 'output_temp.tif')
    try:
        status = subprocess.check_output(cmd, shell=True)
    except:
        raise ValueError('No gdal instalation found')
    
    del raster
    with rasterio.open(os.path.join(tempFolder, 'output_temp.tif')) as con:
        raster = con.read()

    os.remove( os.path.join(tempFolder,'resized_temp.tif'))
    os.remove( os.path.join(tempFolder,'output_temp.tif'))

    raster = np.transpose(raster, [1,2,0])
    raster = resize(raster, ( targetHeight, targetWidth), anti_aliasing= False, order = order, mode = 'edge',preserve_range=True)
    raster = np.transpose(raster, [2,0,1])
    raster = raster.astype(dtype)



    return {'raster':raster, 'transform':native_transform, 'extent':targetExtent, 'crs':targetCrs}

def getResolution(minx_wgs, maxx_wgs, miny_wgs, maxy_wgs, crs, Minv, bias):
    STEPS = 10
    
    x_step = (maxx_wgs - minx_wgs) / STEPS
    y_step = (maxy_wgs - miny_wgs) / STEPS

    
    pixelPositions = {}
    n=0
    m=0
    for n in [0,1]:
        for m in [0,1]:
            if m != 1 or n !=1:
                points = [ geometry.Point((minx_wgs + (i+n) * x_step, miny_wgs + (j+m) * y_step))  for i in np.arange(STEPS) for j in np.arange(STEPS)]
                df_wgs = gpd.GeoDataFrame({'geometry':points})
                df_wgs.crs = 'epsg:4326'
                df_native = df_wgs.to_crs(crs)
                pixelPositions[str(n) + '_' + str(m)] = np.array([ np.matmul(Minv , [point.x - bias[0], point.y -bias[1]] ) for point in df_native['geometry'].values])

    distances_x = [geodesic( (miny_wgs + j * y_step, minx_wgs + i * x_step), (miny_wgs + j * y_step, minx_wgs + (i+1) * x_step)).m  for i in np.arange(STEPS) for j in np.arange(STEPS)]
    distances_y = [geodesic( (miny_wgs + j * y_step, minx_wgs + i * x_step), (miny_wgs + (j+1) * y_step, minx_wgs + i * x_step)).m  for i in np.arange(STEPS) for j in np.arange(STEPS)]
    dif_pixel_x  = pixelPositions['1_0'] - pixelPositions['0_0']
    dif_pixel_y  = pixelPositions['0_1'] - pixelPositions['0_0']
    
    distances_pixel_x = [math.sqrt( p[0]**2 + p[1]**2) for p in dif_pixel_x]
    distances_pixel_y = [math.sqrt( p[0]**2 + p[1]**2) for p in dif_pixel_y]

    x_res = np.divide(distances_x, distances_pixel_x)
    y_res = np.divide(distances_y, distances_pixel_y)
    
    x_res = np.min(x_res)
    y_res = np.min(y_res)
    
    return x_res, y_res

def getVirtualSize(bounds_mercator, targetCrs, native_transform):
    M = [[native_transform[1], native_transform[2]] , [native_transform[4], native_transform[5]] ]
    bias = [native_transform[0], native_transform[3]]
    
    Minv = np.linalg.inv(M)
    
    #convert bounds_tile to raster crs
    lowerLeft = transformPoint( (bounds_mercator['xMin'],bounds_mercator['yMin']), 'EPSG:3857', targetCrs)
    upperLeft = transformPoint( (bounds_mercator['xMin'],bounds_mercator['yMax']), 'EPSG:3857', targetCrs)
    lowerRight = transformPoint( (bounds_mercator['xMax'],bounds_mercator['yMin']), 'EPSG:3857', targetCrs)
    
    #calculate pixels using inverse transform of 3 points
    lowerLeft_pixel = np.matmul(Minv , [lowerLeft[0] - bias[0], lowerLeft[1] -bias[1]] ) 
    upperLeft_pixel = np.matmul(Minv , [upperLeft[0] - bias[0], upperLeft[1] -bias[1]] ) 
    lowerRight_pixel = np.matmul(Minv , [lowerRight[0] - bias[0], lowerRight[1] -bias[1]] ) 
    
    #calculate pixel distance
    w = math.sqrt( (lowerLeft_pixel[0] - lowerRight_pixel[0] )**2 + (lowerLeft_pixel[1] - lowerRight_pixel[1] )**2 )    
    h = math.sqrt( (lowerLeft_pixel[0] - upperLeft_pixel[0] )**2 + (lowerLeft_pixel[1] - upperLeft_pixel[1] )**2 )    
    
    w = math.floor(w+1)
    h = math.floor(h+1)
    
    return w,h
    

def transformPoint( point, sourceCrs, targetCrs):
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
def saveRaster(targetFile, r, crs, extent = None, transform = None):
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
