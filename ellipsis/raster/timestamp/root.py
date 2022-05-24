from ellipsis import sanitize
import json

def getRasterByBounds(pathId, timestampId, bounds, layer = None):
    sanitize.validUuid('pathId', pathId, True)
    sanitize.validUuid('timestampId', timestampId, True)
    sanitize.validBounds('bounds', bounds, True)

    if type(layer) != type(None):
        try:
            layer_temp = json.dumps(layer)
        except:
            raise ValueError('layer must be a uuid of some predefined layer or a dictionary with parameters for a layer')
        






def getAggregatedData():
    pass

def add():
    pass

def edit():
    pass

def getBounds():
    pass

def activate():
    pass

def delete():
    pass

def trash():
    pass
