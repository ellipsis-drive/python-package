
import ellipsis as el
import os



token = el.account.logIn('demo_user', 'demo_user')

folderId = '44a40d37-5c66-4a29-b2f2-995aeeae9cc2' #id of the Ellipsis Drive folder you wish to place content in, should be None when you wish to place it in the root
path = '/home/daniel/Downloads/test' #path to the folder on your local disk you wish to write to Ellipsis Drive

vectorFiles = ['gpkg'] #file extenstions you wish to create vector layers for
rasterFiles = ['tif'] #file extenstions you wish to create reaster layers for


#recusrive function
def f(pathId, path, token):
    files = os.listdir(path)
    for file in files:
        if os.path.isdir( path + '/' + file):
            newPathId = el.path.folder.add(file, token, parentId = pathId)['id']
            f(newPathId, path + '/' + file, token)
        else:
            fileFormat = file.split('.')[-1]
            if fileFormat in vectorFiles:
                layerId = el.path.vector.add(file, token, parentId=pathId)['id']
                timestampId = el.path.vector.timestamp.add(pathId=layerId, token = token)['id']
                el.path.vector.timestamp.file.add(pathId = layerId, timestampId=timestampId, token = token, filePath = path + '/' + file, fileFormat = fileFormat)
            elif fileFormat in rasterFiles:
                layerId = el.path.raster.add(file, token, parentId=pathId)['id']
                timestampId = el.path.raster.timestamp.add(pathId=layerId, token = token)['id']
                el.path.raster.timestamp.file.add(pathId = layerId, timestampId=timestampId, token = token, filePath = path + '/' + file, fileFormat = fileFormat)
                el.path.raster.timestamp.activate(pathId = layerId, timestampId=timestampId, token=token)

f(folderId, path, token)
