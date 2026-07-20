import ellipsis as el
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
