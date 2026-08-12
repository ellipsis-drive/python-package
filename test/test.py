import ellipsis as el

token = el.account.logIn('demo_user', 'demo_user') #or go to the UI, click the context menu of a folder, click integrate and pick 'create token'. This will create a token that allows to work in that specific folder

#id of the folder to add the layer to, make None if you wish to work in your root
folderId = '44a40d37-5c66-4a29-b2f2-995aeeae9cc2'

#create a layer in the folder and a timestamp in the layer
layerId = el.path.mesh.add(name = 'my mesh', parentId=folderId, token = token)['id']
timestampId = el.path.mesh.timestamp.add(pathId = layerId, token=token)['id']

#upload the file
file = '/home/daniel/Ellipsis/db/3dtiles/tileset.zip'
el.path.mesh.timestamp.file.add(pathId=layerId, timestampId=timestampId, filePath=file, token=token)

#once the upload is completed mind to activate the timestamp
el.path.mesh.timestamp.activate(pathId=layerId, timestampId=timestampId, token=token)


import os

el.apiManager.baseUrl = 'https://acc.api.ellipsis-drive.com/v3'


pathId = '6c9ff302-6834-4a68-b3e4-8be97ad798a5'
timestampId = '9578436a-04ea-4a66-8b16-d8e832c9b31f'

token = 'epat_wnGCPen6Fb7e7CUtKl5ON29uyfEgl8WrhaqD7JdmBG5Ilrjj3yR8Akrzko691pif'

folder = '/home/daniel/Ellipsis/db/tif_files'
files = os.listdir(folder)

N=11

file = folder + '/' + files[N]

el.path.raster.timestamp.file.add(pathId=pathId, timestampId=timestampId, filePath = file, token=token, fileFormat='tif')
el.path.raster.timestamp.activate(pathId=pathId, timestampId=timestampId,  token=token)
