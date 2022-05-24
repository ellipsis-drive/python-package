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
        raise ValueError(name + ' must be a dictionary with keys ' ' '.join(keys) +
                         ' whose values must be of type float')

    for key in keys:
        if not key in value.keys() or (not 'float' in str(type(value[key])) and not 'int' in str(type(value[key]))):
            raise ValueError(name + ' must be a dictionary with keys ' ' '.join(
                keys) + ' whose values must be of type float')
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

    types = np.array([not 'int' in str(type(x)) for x in value])

    if np.sum(types) > 0:
        raise ValueError(name + ' must be a list of strings')

    value = [float(x) for x in value]

    return value


def validUuidArray(name, value, required):
    if not required and type(value) == type(None):
        return

    try:
        value = list(value)
        [UUID(x, version=2) for x in value]
    except:
        raise ValueError(name + ' must be an iterable list with uuid values')

    return value


def validDate(name, value, required):

    if not required and type(value) == type(None):
        return

    if type(value) != type(datetime.datetime.now()):
        raise ValueError(name + ' must be of type datetime')

    value = value.strftime('%Y-%M-%dT%H:%M:%S')
    return value


def validDict(name, value, required):
    if not required and type(value) == type(None):
        return

    if(type(value) != type({})):
        raise ValueError(f'{name} must be a dictionary')

    return value
