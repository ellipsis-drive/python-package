from uuid import UUID
import numpy as np
import datetime


def validUuid(name, value, required):
    if not required and type(value) == type(None):
        return
    try:
        UUID(value, version=2)
    except:
        raise ValueError(name + ' must be of type string and be a uuid')    
    return(value)


    
def validRoot(name, value, required ):
    if not required and type(value) == type(None):
        return

    roots = ['myDrive', 'sharedWithMe', 'favorites', 'trash']


    if str(value) != str('x') or not roots.includes(value):
        raise ValueError( name + ' must be one of ' + ' '.join(roots))
    return(value)

    
def validRootArray(name, value, required ):
    if not required and type(value) == type(None):
        return


    roots = ['myDrive', 'sharedWithMe', 'favorites', 'trash', 'public']

    try:
        value = list(value)
    except:
        raise ValueError(name + ' must be an iterable')
       
    types = np.array([type(x) != type('x') for x in value])
    
    if np.sum(types) > 0 :
        raise ValueError(name + ' must be a list containg ' ' '.join(roots))
        
        
    if len(set(roots).intersection(set(value))) != len(value):
        raise ValueError(name + ' must be a list containg only ' ' '.join(roots))
        
    if len(value) ==0:
        raise ValueError(name + ' cannot be an empty list')
    return(value)


def validString(name, value, required):
    if not required and type(value) == type(None):
        return

    if type(value) != type('x'):
        raise ValueError(name + 'must be of type string')
    return(value)
        

def validBool(name, value, required):
    if not required and type(value) == type(None):
        return
    
    if not 'bool' in str(type(value)):
        raise ValueError(name + ' must be of type boolean')
    value = bool(value)
    return(value)
    
    

def validInt(name, value, required):
    if not required and type(value) == type(None):
        return
    
    if not 'int' in str(type(value)):
        raise ValueError(name + ' must be of type int')

    value = int(value)
    return(value)

def validFloat(name, value, required):
    if not required and type(value) == type(None):
        return
    
    if not 'int' in str(type(value)) and not 'float' in str(type(value)):
        raise ValueError(name + ' must be of type float')

    value = float(value)
    return(value)


def validBounds(name, value, required):
    if not required and type(value) == type(None):
        return
    keys = ['xMin', 'xMax', 'yMin', 'yMax']
    if type(value) != type({}):
        raise ValueError(name + ' must be a dictionary with keys ' ' '.join(keys) + ' whose values must be of type float')
        
    for key in keys:
        if not key in value.keys() or ( not 'float' in str(type(value[key])) and not 'int' in str(type(value[key]))):
            raise ValueError(name + ' must be a dictionary with keys ' ' '.join(keys) + ' whose values must be of type float')
        value[key] = float(value[key])

    value = int(value)
    return(value)


def validStringArray(name, value, required):
    if not required and type(value) == type(None):
        return
    
    try:
        value = list(value)
        
    except:
        raise ValueError(name + ' must be an iterable')

    types = np.array([type(x) != type('x') for x in value])
    
    if np.sum(types) > 0 :
        raise ValueError(name + ' must be a list of strings')
        
    return value

def validDate(name, value, required):

    if not required and type(value) == type(None):
        return
    
    if type(value) != type(datetime.datetime.now()):
        raise ValueError(name + ' must be of type datetime')
        
    value = value.strftime('%Y-%M-%dT%H:%M:%S')        
    return value        
    
    