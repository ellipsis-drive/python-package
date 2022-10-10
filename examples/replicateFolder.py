import ellipsis as el
import os

token =  el.account.logIn( '', '')


folderToReplicate = '/home/folderName'

replicate(folderLongName = folderToReplicate, folderName = folderToReplicate, parentId = None, token = token)


#recursive function creating the folders and vector layers. Also performing the uploads
def replicate(folderLongName, folderName, parentId, token):
    folderId = el.path.add(pathType = 'folder', name = folderName, token = token, parentId = parentId)['id']

    content = os.listdir(folderLongName)

    for f in content:
        if os.path.isdir(folderLongName + '/' + f):
            replicate(folderLongName = folderLongName + '/' + f, folderName = f, parentId = folderId, token = token)
        else:
            pathId = el.path.add(pathType = 'vector', name = f, token = token, parentId = parentId)['id']
            layerId = el.path.vector.layer.add(pathId = pathId, name = 'my layer', token = token)
            el.path.vector.layer.upload.upload( pathId = pathId, layerId = layerId, filePath = folderLongName, token = token)


