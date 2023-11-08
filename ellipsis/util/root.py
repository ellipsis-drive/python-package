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
import pygltflib
from skimage.transform import resize
import os
import random
import subprocess
from concurrent.futures import ProcessPoolExecutor as Pool
import multiprocessing
import warnings
import uuid
import shapely
from shapely.ops import cascaded_union


from ellipsis import sanitize
from rasterio.warp import reproject as warp, Resampling, calculate_default_transform

warnings.simplefilter("ignore")

def plotPointCloud(df, method = 'cloud', width = 800, height = 600, scale = 0.003):
    import open3d as o3d

    if type(method) != type('x'):
        raise ValueError('method must be one of cloud, voxel or mesh')
    if not method in ['cloud', 'mesh', 'voxel']:
        raise ValueError('method must be one of cloud, voxel or mesh')
    if type(df) != type(pd.DataFrame()):
        raise ValueError('df must be a dataframe with columns x,y,z, red, green,blue all of type float')


    maxx = np.max(df['x'].values)
    maxy = np.max(df['y'].values)
    maxz = np.max(df['z'].values)
    minx = np.min(df['x'].values)
    miny = np.min(df['y'].values)
    minz = np.min(df['z'].values)


    M = max(maxx - minx,maxy-miny, maxz-minz)


    points = [ [( p[0] - minx  )/M, (p[1]-miny)/M, (p[2] - minz)/M] for p in zip( df['x'].values, df['y'].values, df['z'].values)]
    colors = [  [p[0], p[1], p[2]]  for p in   zip( df['red'].values/ 255, df['green'].values/ 255, df['blue'].values/255)]

    # Initialize a point cloud object
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    vis = o3d.visualization.Visualizer()

    vis.create_window(window_name='Point cloud', width=width, height=height)

    if method == 'cloud':
        # Add the pointcloud to the visualizer
        vis.add_geometry(pcd)
    elif method == 'voxel':
        # Create a voxel grid from the point cloud with a voxel_size of 0.01
        voxel_grid=o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,voxel_size=scale)

        # Add the voxel grid to the visualizer
        vis.add_geometry(voxel_grid)
    elif method == 'mesh':
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, scale)
        mesh.compute_vertex_normals()
        vis.add_geometry(mesh)


    # We run the visualizater
    vis.run()
    vis.destroy_window()








def parseGlb(stream):
    gltf = pygltflib.GLTF2.load_from_bytes(stream)
    binary_blob = gltf.binary_blob()
    translation = gltf.nodes[0].translation

    points_accessor = gltf.accessors[gltf.meshes[0].primitives[0].attributes.POSITION]
    points_buffer_view = gltf.bufferViews[points_accessor.bufferView]
    points = np.frombuffer(
        binary_blob[
        points_buffer_view.byteOffset
        + points_accessor.byteOffset: points_buffer_view.byteOffset
                                      + points_buffer_view.byteLength
        ],
        dtype="float32",
        count=points_accessor.count * 3,
    )

    color_accessor = gltf.accessors[gltf.meshes[0].primitives[0].attributes.COLOR_0]
    color_buffer_view = gltf.bufferViews[color_accessor.bufferView]
    colors = np.frombuffer(
        binary_blob[
        color_buffer_view.byteOffset
        + color_accessor.byteOffset: color_buffer_view.byteOffset
                                     + color_buffer_view.byteLength
        ],
        dtype="float32",
        count=color_accessor.count * 3,
    )

    points = points.reshape((-1, 3))
    points = points.astype('float64')
    colors = colors.reshape((-1, 3))

    red = np.round(np.power(np.array(colors[:, 0]), 1 / 2.2) * 255).astype('uint8')
    green = np.round(np.power(np.array(colors[:, 1]), 1 / 2.2) * 255).astype('uint8')
    blue = np.round(np.power(np.array(colors[:, 2]), 1 / 2.2) * 255).astype('uint8')

    return {'x': np.array(points[:, 0]) + translation[0], 'y': np.array(points[:, 1]) + translation[1],
            'z': np.array(points[:, 2]) + translation[2], 'red': red, 'green': green, 'blue': blue}



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

    

    if raster.shape[0] ==3 or raster.shape[0] ==4:
        raster = raster[0:3,:,:]
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
    features['geometryId'] = [str(uuid.uuid4()) for x in np.arange(features.shape[0])]
    features['tileId'] = str(uuid.uuid4())
    count  = features.shape[0]
    
    types = np.unique(np.array([str(type(x)) for x in features['geometry'].values]))
    chosen = None
    for t in types:
        if 'collection' in t:
            raise ValueError('geometry collections are not allowed')
        if 'polygon' in t:
            newChosen = 'polygon'
            if chosen != None and chosen !=newChosen:
                raise ValueError('Geopandas cannot contain mixed geometry types, use either lines, points of polygons.')
            else:
                chosen = 'polygon'
        if 'line' in t:
            newChosen = 'line'
            if chosen != None and chosen !=newChosen:
                raise ValueError('Geopandas cannot contain mixed geometry types, use either lines, points of polygons.')
            else:
                chosen = 'line'
        if 'point' in t:
            newChosen = 'point'
            if chosen != None and chosen !=newChosen:
                raise ValueError('Geopandas cannot contain mixed geometry types, use either lines, points of polygons.')
            else:
                chosen = 'point'

    

    LEN = 2.003751e+07
    tile = {'xMin' : -LEN, 'xMax': LEN, 'yMin':-LEN, 'yMax':LEN} 
    args = (tile, 0, zoom, features, bounds, cores, buffer, count, chosen)
    sh_end = manageTile(args)
    return sh_end
    
    

def manageTile(args):
    tile, depth, zoom, sh, bounds, cores, buffer, count, chosen = args
    if zoom == depth:
        return sh
    if depth == zoom -1:
        t_buffer = buffer
    else:
        t_buffer = 0


    newTiles = splitTile(tile, t_buffer)
    shs = []
    tile = newTiles[0]
    args = []

    maxCount = 0
    for tile in newTiles:        
        sh_new, bounds_new = cut(sh, bounds, tile, chosen)
        if sh_new.shape[0] > maxCount:
            maxCount = sh_new.shape[0]
        if sh_new.shape[0] > 0:
            args = args + [(tile, depth+1, zoom, sh_new, bounds_new, cores, buffer, count, chosen,)]
    
    
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


def cut(sh, bounds, tile, chosen):
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
        
        #dissolve the geometry collections
        if sh_intersects.shape[0] >0:
            collections = np.array(['collection' in str(type(x)) for x in sh_intersects['geometry']])
            geometryCollections = sh_intersects['geometry'][collections].values
    
            newGeometries = [ cascaded_union([geometry for geometry in collection if chosen in str(type(geometry))]) for collection in geometryCollections   ]
    
            sh_intersects['geometry'][collections] = newGeometries
            
            correct_type = [chosen in str(type(x)) for x in sh_intersects['geometry'].values]
            sh_intersects = sh_intersects[correct_type]
            sh_intersects = sh_intersects[np.logical_not(sh_intersects.is_empty)]
            sh_intersects = sh_intersects[sh_intersects.is_valid]

        
        bounds_intersects = sh_intersects.bounds

        sh_result = pd.concat([sh_intersects, sh_within])
        sh_result['tileId'] = str(uuid.uuid4())
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
    if cores ==1:
        sh = reprojectSub(args[0])[0]
    else:
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
        if cores ==1:
            sh_new = reprojectSub(args[0])
            shs = shs + [sh_new]
        else:
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
    try:
        sh = sh.to_crs(str(targetCrs))
    except:
        sh = sh.to_crs(targetCrs.replace('EPSG:', ''))


    
    is_poly = ['poly' in str(type(x)) for x in sh['geometry'].values]
    if np.sum(is_poly) > 0:
        sh['geometry'][is_poly] = sh[is_poly].buffer(0)    
    
    bounds = sh.bounds
    return sh, bounds



def getActualExtent(minx, maxx, miny, maxy, crs, out_crs = 3857):
    
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
        df_wgs = df.to_crs('EPSG:' + str(out_crs))
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

def mergeGeometriesByColumn(features, columnName, cores = 1):
    names = np.unique(features[columnName].values)
    N = math.floor(len(names)/cores) + 1
    names_chunks = chunks(names, N)
    args = [{'features': features, 'columnName':columnName, 'names':names_cunk} for names_cunk in names_chunks]
    if cores > 1:
        with Pool(4) as p:
            shs = p.map(mergeGeometriesByColumnPart, args)
        shs = list(shs)
        return pd.concat(shs)

    else:
        return mergeGeometriesByColumnPart( {'features':features, 'columnName':columnName, 'names':names})
    


def mergeGeometriesByColumnPart(args):

    features = args['features']
    columnName = args['columnName']
    names = args['names']
    
    sh_new = []
    for i in np.arange(len(names)):
        name = names[i]
        sh_name = features[features[columnName] == name ]
        sh_name['geometry'] = sh_name.unary_union
        sh_new = sh_new + [sh_name[0:1]]
    sh_new = pd.concat(sh_new)
    return sh_new
        



def simplifyGeometries(features, tolerance, preserveTopology=True, removeIslands = True, cores = 1):
    
    shs = np.array_split(features, cores)
        
    args = [ {'sh': shs[i], 'tolerance':tolerance, 'preserveTopology': preserveTopology, 'removeIslands':removeIslands} for i in np.arange(len(shs))]
    if cores >1:
        with Pool(cores) as p:
            shs = p.map(simplifySub, args)    
            result = pd.concat(list(shs))
    else:
        result = simplifySub(args[0])
    return result
    
    
def simplifySub(args):
    sh_sub = args['sh']
    tolerance = args['tolerance']
    preserveTopology = args['preserveTopology']
    removeIslands = args['removeIslands']

    fractionArea = tolerance**2

    if removeIslands:
        multipolygons = sh_sub['geometry'][sh_sub['geometry'].type == 'MultiPolygon' ]
        newMultiPolygons = [shapely.ops.unary_union([x.buffer(0) for x in multipolygons.values[i] if x.area > fractionArea ]) if len([x for x in multipolygons.values[i] if x.area > fractionArea ]) > 0 else multipolygons.values[i]  for i in np.arange( len(multipolygons))]
        
        #newMultiPolygons = [x if len(x) > 1 else x[0] for x in newMultiPolygons]
        sh_sub['geometry'][sh_sub['geometry'].type == 'MultiPolygon' ] = newMultiPolygons


    sh_sub['geometry'] = sh_sub.simplify(tolerance, preserve_topology=preserveTopology)
    is_poly = ['poly' in str(type(x)) for x in sh_sub['geometry'].values]
    sh_sub['geometry'][is_poly] = sh_sub[is_poly].buffer(0)

    return sh_sub
    
    
