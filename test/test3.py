import ellipsis as el
import datetime
import requests

baseUrl = 'https://api.ellipsis-drive.com/v2'
s = requests.Session()


folderId = '46e1e919-8b73-42a3-a575-25c6d45fd93b'

token = el.account.logIn("demo_user", "demo_user")

mapId = el.path.add('raster', 'test', token, parentId = folderId)['id']


timestampId = el.path.raster.timestamp.add(mapId, token)['id']

token = 'Bearer ' + token



filePath = 'test/0.tif'
r = el.path.raster.timestamp.upload.upload(mapId, timestampId, filePath, token)
print(r)

pathId = mapId
url = '/path/' + pathId + '/raster/timestamp/' + timestampId + '/upload'
body = {'fileName':'0.tif', 'format':'tif'}




conn_file = open(filePath, 'rb')


payload = MultipartEncoder(fields = {'timestampId': timestampId, 'mapId':mapId, 'format':'tif', 'fileName':'0.tif', 'fileToUpload': ('0.tif', conn_file, 'application/octet-stream')})
r = s.post(baseUrl + url, headers = {"Authorization":token, "Content-Type": payload.content_type}, data=payload)



files = {'fileToUpload':  conn_file}

r = s.post(baseUrl + url, headers = {"Authorization":token}, data=body, files=files)

r.text

conn_file.close()
