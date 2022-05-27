import ellipsis as el
import datetime

folderId = '46e1e919-8b73-42a3-a575-25c6d45fd93b'

##account
token = el.account.logIn("demo_user", "demo_user")

mapId = el.path.add('raster', 'test', token, parentId = folderId)['id']
el.path.raster.editMap(mapId, token, interpolation = 'nearest')


timestampId = el.path.raster.timestamp.add(mapId, token)['id']



filePath = '/home/daniel/Ellipsis/db/testset/0.tif'

import backup
backup.uploadRasterFile(mapId, timestampId, filePath, token)


