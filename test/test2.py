import ellipsis as el
import datetime
import os
import time

folderId = '46e1e919-8b73-42a3-a575-25c6d45fd93b'

##account
token = el.account.logIn("demo_user", "demo_user")
admin_token = el.account.logIn('admin', 'GQkDzhVeCC0aQ9ERyiss')
daan_token = el.account.logIn('daan', 'Brooksrange24')

el.account.listRootMaps('myDrive',token)
el.account.listRootFolders('sharedWithMe',token)

r_raster = el.path.searchRaster(token=token);

r_vector = el.path.searchVector()

r_raster = el.path.searchFolder(token=token);
    

##user

result = el.user.search('daan')
daanId = [x for x in result if x['username'] == 'daan'][0]['id']
el.user.get(daanId)


##path
rasterInfo = el.path.get('59caf510-bab7-44a8-b5ea-c522cfde4ad7', token)

info = el.path.get(folderId, token)

folderId = info['id']
maps = el.path.listMaps(folderId, token = token, listAll = True)
folders = el.path.listFolders(folderId, token = token, listAll = True)

mapId = [ m for m in maps['result'] if not m['trashed'] ][0]['id']


#crash


el.path.editMetadata(pathId = mapId, token = token, description = 'test')

addedFolderId = el.path.add( 'folder', 'test', token = token, parentId = folderId)['id']

el.path.trash(addedFolderId, token)
el.path.recover(addedFolderId, token)

addedRasterId = el.path.add( 'raster', 'test2', token = token, parentId = folderId)['id']

el.path.move([addedRasterId], addedFolderId, token)


el.path.trash(addedFolderId, admin_token)
el.path.delete(pathId = addedFolderId, token = admin_token, recursive = True)


el.path.editPublicAccess(pathId = folderId, token = token, accessLevel=0, hidden = False)
el.path.editPublicAccess(pathId = folderId, token = token, accessLevel=100, hidden = True)

el.path.favorite(folderId, token=token)
el.path.unfavorite(folderId, token=token)

###invites
inviteId =  el.path.invite.sent(pathId = folderId, token=token, userId = daanId, access = {'accessLevel': 200, 'processingUnits':10000})['id']

el.path.invite.getPathInvites(folderId, token)


el.path.invite.getYourInvites(daan_token)

el.path.invite.revoke(pathId = folderId, inviteId = inviteId, token = token)


inviteId =  el.path.invite.sent(pathId = folderId, token=token, userId = daanId, access = {'accessLevel': 200, 'processingUnits':10000})['id']

el.path.invite.decline(folderId, inviteId, daan_token)


inviteId =  el.path.invite.sent(pathId = folderId, token=token, userId = daanId, access = {'accessLevel': 200, 'processingUnits':10000})['id']
el.path.invite.accept(folderId, inviteId, daan_token)

##members
members = el.path.member.get(folderId, token, memberType = ['direct'])


daanMemberId = [m['user']['id'] for m in members if m['user']['username'] == 'daan'][0]

el.path.member.edit(pathId = folderId, userId = daanMemberId, access = {'accessLevel' : 200} ,token = token)

el.path.member.delete(folderId, daanMemberId, token)


##raster and uploads
mapId = el.path.add('raster', 'test', token, parentId = folderId)['id']
el.path.raster.editMap(mapId, token, interpolation = 'nearest')


timestampId = el.path.raster.timestamp.add(mapId, token)['id']


dateFrom = datetime.datetime.now()
dateTo = datetime.datetime.now()
el.path.raster.timestamp.edit(mapId, timestampId, token, description = 'hoi', dateFrom = dateFrom, dateTo = dateTo)

filePath = 'test/0.tif'
uploadId = el.path.raster.timestamp.upload.upload(mapId, timestampId, filePath, token)['id']

el.path.raster.timestamp.upload.delete(mapId, timestampId, uploadId, token)
uploadId = el.path.raster.timestamp.upload.upload(mapId, timestampId, filePath, token)['id']

uploads = el.path.raster.timestamp.upload.get(mapId, timestampId, token)

el.path.raster.timestamp.activate(mapId, timestampId, token)


el.path.raster.editBand(mapId, 1, 'hoi', token)


el.path.raster.timestamp.trash(mapId, timestampId, token)
el.path.raster.timestamp.recover(mapId, timestampId, token)
el.path.raster.timestamp.trash(mapId, timestampId, token)
el.path.raster.timestamp.delete(mapId, timestampId, admin_token)

##raster information retrieval
mapId = '59caf510-bab7-44a8-b5ea-c522cfde4ad7'
timestampId = 'f25e120e-ca8f-451f-a5f4-33791db0f2c5'


xMin  = 5.60286
yMin=  52.3031    
xMax  = 5.60315
yMax  = 52.30339

extent = {'xMin':xMin,'yMin':yMin,'xMax':xMax,'yMax':yMax } 

result = el.path.raster.timestamp.getRaster(pathId = mapId, timestampId = timestampId, bounds = extent, token = token)

raster = result['raster']


el.util.plotRaster(raster[0:3,:,:])

r = el.path.raster.timestamp.getDownsampledRaster(pathId = mapId, timestampId=timestampId, bounds = extent, width = 256, height = 256, token = token)
raster = r['raster']
el.util.plotRaster(raster[0:3,:,:])


bounds = el.path.raster.timestamp.getBounds(mapId, timestampId, token)

data = el.path.raster.timestamp.getAggregatedData(mapId, [timestampId], bounds, token=token)

###raster downloads
mapId = '1eea3d2f-27b3-4874-b716-87852c3407c1'
timestampId = "ba5b418a-a39e-4d84-9411-e23c096085a3"
uploads = el.path.raster.timestamp.upload.get(mapId, timestampId, token)
uploadId = uploads['result'][0]['id']

downloadId = el.path.raster.timestamp.order.order(mapId, timestampId, token, uploadId = uploadId)['id']

file_out = '/home/daniel/Downloads/out.tif'
el.path.raster.timestamp.order.download(downloadId, file_out, token)
os.remove(file_out)

pendinDownloads = el.path.raster.timestamp.order.get(token)

parameters = {"angle":45,"bandNumber":1,"alpha":1}
method = "hillShade"
layerId = el.path.raster.layer.add(mapId, 'hoi', method, parameters, token, 'hoi')['id']

el.path.raster.layer.edit(mapId, layerId, method= method, parameters = parameters,token = token, description =  'doei')
el.path.raster.layer.delete(mapId, layerId, token)



###vector layers
mapId = el.path.add('vector', 'test', token)['id']


layerId = el.path.vector.layer.add(mapId, 'test', token)['id']

el.path.vector.layer.edit(mapId, layerId, token, name = 'test2')

el.path.vector.layer.archive(mapId, layerId, token)
el.path.vector.layer.recover(mapId, layerId, token)
el.path.vector.layer.archive(mapId, layerId, token)
el.path.vector.layer.delete(mapId, layerId, admin_token)
layerId = el.path.vector.layer.add(mapId, 'test', token)['id']


###vector uploads
filePath = 'test/test.zip'
el.path.vector.layer.upload.upload(mapId, layerId, filePath, token, fileFormat = 'zip')


upload = el.path.vector.layer.upload.get(mapId, layerId, token)['result'][0]

while upload['status'] != 'completed':
    time.sleep(1)
    upload = el.path.vector.layer.upload.get(mapId, layerId, token)['result'][0]


#layer methods
bounds = el.path.vector.layer.getBounds(mapId, layerId, token)

xMin = bounds.bounds[0]
yMin = bounds.bounds[1]
xMax = bounds.bounds[2]
yMax = bounds.bounds[3]

bounds = {'xMin':xMin, 'xMax':xMax, 'yMin':yMin, 'yMax':yMax}
sh = el.path.vector.layer.getFeaturesByBounds(mapId, layerId, bounds)
sh['result'].plot()

sh = el.path.vector.layer.listFeatures(mapId, layerId, token)

featureIds = sh['result']['id'].values

r =  el.path.vector.layer.getFeaturesByIds(mapId, layerId, featureIds, token)


r = el.path.vector.layer.getChanges(mapId, layerId, token, listAll = True)

editFilter(mapId, layerId, [{'property':'gml_id'}], token)



###feature module
features = sh['result'][1:2]
featureIds = features['id'].values

el.path.vector.layer.feature.add(mapId, layerId, features, token)


el.path.vector.layer.feature.edit(pathId, layerId, featureIds = features['id'].values, token = token, features = features)

el.path.vector.layer.feature.delete(mapId, layerId, featureIds, token)
el.path.vector.layer.feature.recover(mapId, layerId, featureIds, token)
el.path.vector.layer.feature.versions(mapId, layerId, featureIds[0], token)


###message module

import ellipsis as el




info = el.path.get(mapId, token)
while info['vector']['layers'][0]['status']
