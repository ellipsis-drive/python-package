from uuid import UUID
import numpy as np
import datetime
import json
import geopandas as gpd
import pandas as pd
from shapely import geometry

from ellipsis.util.root import reprojectVector


def validUuid(name, value, required):
    if not required and type(value) == type(None):
        return
    try:
        UUID(value, version=2)
    except:
        raise ValueError(name + ' must be of type string and be a uuid')
    return(value)

def validResolution(name, value, required):
    if not required and type(value) == type(None):
        return

    if type(value) != type({}):
        raise ValueError(name + ' must be of type dictionary with properties min and max as float')

    if 'min' not in value.keys() or 'max' not in value.keys():
        raise ValueError(name + ' must be of type dictionary with properties min and max as float')

    try:
        value = {'min': float(value['min']), 'max':float(value['max']) }        
    except:
        raise ValueError(name + ' must be of type dictionary with properties min and max as float')

    return(value)



def validDateRange(name, value, required):

    if not required and type(value) == type(None):
        return
    
    
    if  ( type(value) != type({}) or 'from' not in value.keys() or 'to' not in value.keys()): 
        raise ValueError('date must be a dictionary with properties from and to that should be of type datetime')

    dateFrom = value['from']
    dateTo = value['to']
    dateFrom = validDate('dateFrom', dateFrom, False)    
    dateTo = validDate('dateTo', dateTo, False)    
    return {'from':dateFrom, 'to':dateTo}

def validUuidArray(name, value, required):
    if not required and type(value) == type(None):
        return

    try:
        value = list(value)        
    except:
        raise ValueError(name + ' must be an iterable')

    for uuid in value:
        try:
            UUID(uuid, version=2)
        except:
            raise ValueError(name + ' must be a list of uuids')    
    return(value)

def validPandas(name, value, required):
    if not required and type(value) == type(None):
        return

    if type(value) != type(pd.DataFrame()):
        raise ValueError(name + 'must be of type pandas data frame')
    return(value)

def validString(name, value, required):
    if not required and type(value) == type(None):
        return

    if type(value) != type('x'):
        raise ValueError(name + 'must be of type string')
    return(value)

def validShapely(name, value, required):
    if not required and type(value) == type(None):
        return

    if not 'shapely' in str(type(value)):
        raise ValueError(name + 'must be a shapely geometry')
    return(value)


def validBoundsCrsCombination(name, value, required):
    if not required and type(value) == type(None):
        return

    bounds = value[0]
    crs = value[1]
    
    value = bounds
    keys = ['xMin', 'xMax', 'yMin', 'yMax']
    if type(value) != type({}):
        raise ValueError(name[0] + ' must be a dictionary with keys ' ' '.join(keys) +
                         ' whose values must be of type float')

    for key in keys:
        if not key in value.keys() or (not 'float' in str(type(value[key])) and not 'int' in str(type(value[key]))):
            raise ValueError(name[0] + ' must be a dictionary with keys ' ' '.join(
                keys) + ' whose values must be of type float')
        value[key] = float(value[key])


    if type(crs) != type('x'):
        raise ValueError('crs must be of type string')

    target_tile = geometry.Polygon([(bounds['xMin'],bounds['yMin']), (bounds['xMin'],bounds['yMax']), (bounds['xMax'],bounds['yMax']), (bounds['xMax'], bounds['yMin'])])
    sh = gpd.GeoDataFrame({'geometry':[target_tile]})    
    try:
        sh.crs = crs
    except:
        raise ValueError(name[0] + ' does not fit with the projection given by ' + name[1])

    return bounds, crs        

def validImage(name, value, required):
    if not required and type(value) == type(None):
        return

    if type(value) != type(np.zeros((2,2))):
        raise ValueError(name + ' must be a numpy array with either 2 or 3 dimensions')
    if len(value.shape) != 2  and len(value.shape) !=3 :
        raise ValueError(name + ' must be a numpy array with either 2 or 3 dimensions')
    if len(value.shape) ==3 and value.shape[2] !=3 and value.shape[2] !=1:
        raise ValueError(name + ' must have either 1 or 3 bands')

    return value

def validDataframe(name, value, required):
    if not required and type(value) == type(None):
        return

    if type(value) != type(pd.DataFrame()):
        raise ValueError(name + ' must be a pandas dataframe')
    value = value.copy()
    return value
        

def validNumpyArray(name, value, required):
    if not required and type(value) == type(None):
        return

    if type(value) != type(np.zeros((2,2) )):
        raise ValueError(name + 'must be a numpy array')

    return value


def validList(name, value, required):
    if not required and type(value) == type(None):
        return

    try:
        value = list(value)

    except:
        raise ValueError(name + ' must be an iterable')
    return value


def validGeoSeries(name, value, required, cores = 1):
    if not required and type(value) == type(None):
        return
    try:
        value = gpd.GeoDataFrame({'geometry':value})
    except:
        raise ValueError(name + ' must be a valid geoseries')
    value = validGeopandas(name, value, True, True)
    return value['geometry']


def validGeopandas(name, value, required, custom = False, cores = 1):
    if not required and type(value) == type(None):
        return

    if not custom and type(value) != type(gpd.GeoDataFrame()):
        raise ValueError(name + 'must be a geopandas dataframe')

    value = value.copy()        
    if str(type(value.crs)) == str(type(None)) and min(value.bounds['minx']) > -180  and max(value.bounds['maxx']) < 180 and min(value.bounds['miny']) > -90  and max(value.bounds['maxy']) < 90:
        print('assuming WGS84 coordinates for ' + name)
        value.crs = {'init': 'epsg:4326'}
    elif str(type(value.crs)) == str(type(None)):
        raise ValueError('Please provide CRS for ' + name)
    else:
        value = reprojectVector(features = value, targetEpsg = 4326, cores = cores)
        
    if 'id' in value.columns:
        del value['id']
    if 'userId' in value.columns:
        del value['userId']
    if 'attribution' in value.columns:
        del value['attribution']
    if 'radius' in value.columns:
        del value['radius']
    if 'color' in value.columns:
        del value['color']
        
    return(value)


def validBool(name, value, required):
    if not required and type(value) == type(None):
        return

    if not 'bool' in str(type(value)):
        raise ValueError(name + ' must be of type boolean')
    value = bool(value)
    return(value)


def validObject(name, value, required):
    if not required and type(value) == type(None):
        return


    try:
        json.dumps(value)
    except:
        raise ValueError(name + ' must be json serializable')
    return value

def validInt(name, value, required):
    if not required and type(value) == type(None):
        return

    if not 'int' in str(type(value)).lower():
        raise ValueError(name + ' must be of type int')

    value = int(value)
    return(value)


def validFloat(name, value, required):
    if not required and type(value) == type(None):
        return

    if not 'int' in str(type(value)).lower() and not 'float' in str(type(value)).lower():
        raise ValueError(name + ' must be of type float')

    value = float(value)
    return(value)


def validBounds(name, value, required):
    if not required and type(value) == type(None):
        return
    keys = ['xMin', 'xMax', 'yMin', 'yMax']
    if type(value) != type({}):
        raise ValueError(name + ' must be a dictionary with keys ' ' '.join(keys) +
                         ' whose values must be of type float')

    for key in keys:
        if not key in value.keys() or (not 'float' in str(type(value[key])) and not 'int' in str(type(value[key]))):
            raise ValueError(name + ' must be a dictionary with keys ' + ' '.join(
                keys) + ' whose values must be of type float')
        value[key] = float(value[key])


    if value['xMin'] >= value['xMax']:
        raise ValueError('xMax must be strictly larger than xMin')

    if value['yMin'] >= value['yMax']:
        raise ValueError('yMax must be strictly larger than yMin')

    return(value)


def validStringArray(name, value, required):
    if not required and type(value) == type(None):
        return

    try:
        value = list(value)        

    except:
        raise ValueError(name + ' must be an iterable')

    types = np.array([type(x) != type('x') for x in value])

    if np.sum(types) > 0:
        raise ValueError(name + ' must be a list of strings')

    return value


def validFloatArray(name, value, required):
    if not required and type(value) == type(None):
        return

    try:
        value = list(value)

    except:
        raise ValueError(name + ' must be an iterable')

    types = np.array([(not 'float' in str(type(x))) and (
        not 'int' in str(type(x))) for x in value])

    if np.sum(types) > 0:
        raise ValueError(name + ' must be a list of strings')

    value = [float(x) for x in value]

    return value


def validIntArray(name, value, required):
    if not required and type(value) == type(None):
        return

    try:
        value = list(value)

    except:
        raise ValueError(name + ' must be an iterable')

    types = np.array([not 'int' in str(type(x)).lower() for x in value])

    if np.sum(types) > 0:
        raise ValueError(name + ' must be a list of integers')

    value = [int(x) for x in value]

    return value


def validDate(name, value, required):

    if not required and type(value) == type(None):
        return

    if type(value) != type(datetime.datetime.now()):
        raise ValueError(name + ' must be of type datetime')

    value = value.strftime('%Y-%m-%dT%H:%M:%S')
    return value



