import ellipsis as el
import datetime
import os
import time
import numpy as np
import pandas as pd

#python3 setup.py sdist bdist_wheel
#twine upload --repository pypi dist/*




token = el.account.logIn(username = 'admin', password='')

##access token
el.account.accessToken.create(description = 'hoi', accessList = [{'pathId': 'd448bdb5-783a-4919-98bb-caf8092904aa' , 'access':{'accessLevel':100}}], token = token)
tokenId = el.account.accessToken.get(token, listAll = True)['result'][0]['id']
el.account.accessToken.revoke(accessTokenId = tokenId, token = token)

folderId = '46e1e919-8b73-42a3-a575-25c6d45fd93b'




##account
demo_token = el.account.logIn("demo_user", "")
admin_token = el.account.logIn(username = 'admin', password='')
daan_token = el.account.logIn('daan', "")

el.account.listRoot('myDrive', pathType = 'layer', token = demo_token)

el.account.listRoot('sharedWithMe','folder', demo_token)

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
maps = el.path.listPath(folderId, pathType='layer', token = token, listAll = True)
folders = el.path.listPath(folderId, pathType='folder', token = token, listAll = True)

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
inviteId =  el.path.invite.send(pathId = folderId, token=token, userId = daanId, access = {'accessLevel': 200, 'processingUnits':10000})['id']

el.path.invite.getPathInvites(folderId, token)


el.path.invite.getYourInvites(daan_token)

el.path.invite.revoke(pathId = folderId, inviteId = inviteId, token = token)


inviteId =  el.path.invite.send(pathId = folderId, token=token, userId = daanId, access = {'accessLevel': 200, 'processingUnits':10000})['id']

el.path.invite.decline(folderId, inviteId, daan_token)


inviteId =  el.path.invite.send(pathId = folderId, token=token, userId = daanId, access = {'accessLevel': 200, 'processingUnits':10000})['id']
el.path.invite.accept(folderId, inviteId, daan_token)

##members
members = el.path.member.get(folderId, token, memberType = ['direct'])


daanMemberId = [m['user']['id'] for m in members if m['user']['username'] == 'daan'][0]

el.path.member.edit(pathId = folderId, userId = daanMemberId, access = {'accessLevel' : 200} ,token = token)

el.path.member.delete(folderId, daanMemberId, token)

##usage
pathId = '8a11c27b-74c3-4570-bcd0-64829f7cd311'

users = el.path.usage.getActiveUsers(pathId = pathId, token = token, listAll=True)
el.path.usage.getUsage(pathId = pathId, userId = users['result'][0]['user']['id'], token =token)
el.path.usage.getAggregatedUsage(pathId = pathId, loggedIn = False, token = token)

##raster and uploads
mapId = el.path.add('raster', 'test', token, parentId = folderId)['id']
el.path.raster.editMap(mapId, token, interpolation = 'nearest')


timestampId = el.path.raster.timestamp.add(mapId, token)['id']


dateFrom = datetime.datetime.now()
dateTo = datetime.datetime.now()
el.path.raster.timestamp.edit(mapId, timestampId, token, description = 'hoi', date={'from': dateFrom, 'to':dateTo})

filePath = '/home/daniel/Ellipsis/python-package/test/0.tif'
uploadId = el.path.raster.timestamp.upload.add(pathId = mapId, timestampId = timestampId, filePath = filePath, fileFormat = 'tif', token = token)['id']

el.path.raster.timestamp.upload.trash(pathId = mapId, timestampId = timestampId, uploadId= uploadId, token = token)
el.path.raster.timestamp.upload.recover(pathId = mapId, timestampId = timestampId, uploadId= uploadId, token = token)
el.path.raster.timestamp.upload.trash(pathId = mapId, timestampId = timestampId, uploadId= uploadId, token = token)
el.path.raster.timestamp.upload.delete(mapId, timestampId, uploadId, token)
uploadId = el.path.raster.timestamp.upload.add(pathId = mapId, timestampId = timestampId, filePath=filePath, fileFormat='tif', token = token)['id']

uploads = el.path.raster.timestamp.upload.get(mapId, timestampId, token)


el.path.raster.timestamp.activate(mapId, timestampId, token)

while el.path.get(mapId, token)['raster']['timestamps'][0]['status'] != 'active':
    time.sleep(2)

el.path.raster.timestamp.deactivate(mapId, timestampId, token)
while el.path.get(mapId, token)['raster']['timestamps'][0]['status'] != 'passive':
    time.sleep(2)
el.path.raster.timestamp.activate(mapId, timestampId, token)

info = el.path.get(mapId, token)
timestamp = info['raster']['timestamps'][0]
while timestamp['status'] != 'active':
    time.sleep(1)
    info = el.path.get(mapId, token)
    timestamp = info['raster']['timestamps'][0]


el.path.raster.editBand(mapId, 1, 'hoi', token)


el.path.raster.timestamp.trash(mapId, timestampId, token)
el.path.raster.timestamp.recover(mapId, timestampId, token)
el.path.raster.timestamp.trash(mapId, timestampId, token)
el.path.raster.timestamp.delete(mapId, timestampId, admin_token)

el.path.trash(mapId, token)
el.path.recover(mapId, token)
el.path.trash(mapId, token)
el.path.delete(mapId, admin_token)

##raster information retrieval
mapId = '59caf510-bab7-44a8-b5ea-c522cfde4ad7'
timestampId = 'f25e120e-ca8f-451f-a5f4-33791db0f2c5'


styleId = el.path.get(mapId, token)['raster']['styles'][0]['id']

xMin  = 5.60286
yMin=  52.3031    
xMax  = 5.60315
yMax  = 52.30339

extent = {'xMin':xMin,'yMin':yMin,'xMax':xMax,'yMax':yMax } 

result = el.path.raster.timestamp.getRaster(pathId = mapId, timestampId = timestampId, style=styleId, extent = extent, token = token)

raster = result['raster']


el.util.plotRaster(raster[0:3,:,:])

r = el.path.raster.timestamp.getSampledRaster(pathId = mapId, timestampId=timestampId, style=styleId, extent = extent, width = 1024, height = 1024, token = token)
raster = r['raster']
el.util.plotRaster(raster[0:3,:,:])


bounds = el.path.raster.timestamp.getBounds(mapId, timestampId, token)

data = el.path.raster.timestamp.analyse(mapId, [timestampId], bounds, token=token)

###raster downloads
mapId = '1eea3d2f-27b3-4874-b716-87852c3407c1'
timestampId = "ba5b418a-a39e-4d84-9411-e23c096085a3"
uploads = el.path.raster.timestamp.upload.get(mapId, timestampId, token)
uploadId = uploads['result'][0]['id']

downloadId = el.path.raster.timestamp.order.add(mapId, timestampId, token, uploadId = uploadId)['id']

file_out = '/home/daniel/Downloads/out.tif'
el.path.raster.timestamp.order.download(downloadId, file_out, token)
os.remove(file_out)


##from here
pendinDownloads = el.path.raster.timestamp.order.get(token)


####raster styling
parameters = {"angle":45,"bandNumber":1,"alpha":1}
method = "hillShade"
layerId = el.path.raster.style.add(mapId, 'hoi', method, parameters, token,  default = True)['id']

el.path.raster.style.edit(mapId, layerId, method= method, parameters = parameters,token = token, default = False)
el.path.raster.style.delete(mapId, layerId, token)



###vector layers
mapId = el.path.add('vector', 'test2', token)['id']


layerId = el.path.vector.timestamp.add(mapId,  token = token)['id']

el.path.vector.timestamp.edit(mapId, layerId, token, description = 'adsfd')

el.path.vector.timestamp.trash(mapId, layerId, token)
el.path.vector.timestamp.recover(mapId, layerId, token)
el.path.vector.timestamp.trash(mapId, layerId, token)
el.path.vector.timestamp.delete(mapId, layerId, token)
layerId = el.path.vector.timestamp.add(mapId, description = 'test', token = token)['id']


###vector uploads
filePath = '/home/daniel/Ellipsis/python-package/test/test.zip'
el.path.vector.timestamp.upload.add(pathId = mapId, timestampId = layerId, filePath = filePath, token = token, fileFormat = 'zip')


upload = el.path.vector.timestamp.upload.get(pathId = mapId,  timestampId = layerId, token = token)['result'][0]

while upload['status'] != 'completed':
    time.sleep(1)
    upload = el.path.vector.timestamp.upload.get(pathId = mapId, timestampId = layerId, token = token)['result'][0]


#layer methods
bounds = el.path.vector.timestamp.getBounds(mapId, layerId, token)

xMin = bounds.bounds[0]
yMin = bounds.bounds[1]
xMax = bounds.bounds[2]
yMax = bounds.bounds[3]

bounds = {'xMin':xMin, 'xMax':xMax, 'yMin':yMin, 'yMax':yMax}
sh = el.path.vector.timestamp.getFeaturesByExtent(pathId = mapId, timestampId = layerId, extent =  bounds, token = token, listAll = False)
sh['result'].plot()

sh = el.path.vector.timestamp.listFeatures(mapId, layerId, token)

featureIds = sh['result']['id'].values

r =  el.path.vector.timestamp.getFeaturesByIds(mapId, layerId, featureIds, token)


r = el.path.vector.timestamp.getChanges(mapId, layerId, token, listAll = True)

el.path.vector.editFilter(mapId, [{'property':'gml_id'}], token)

r = el.path.get(mapId, token)
blocked = r['vector']['timestamps'][0]['availability']['blocked']
while blocked:
    time.sleep(1)
    r = el.path.get(mapId, token)
    blocked = r['vector']['timestamps'][0]['availability']['blocked']


###feature module
features = sh['result'][1:2]
featureIds = features['id'].values

el.path.vector.timestamp.feature.add(mapId, layerId, features, token)

levelsOfDetail1 = features.simplify(tolerance = 1, preserve_topology = True)
el.path.vector.timestamp.feature.add(pathId = mapId, timestampId =  layerId, features=features, levelOfDetail1=levelsOfDetail1, token=token)



el.path.vector.timestamp.feature.edit(mapId, layerId, featureIds = features['id'].values, token = token, features = features)

el.path.vector.timestamp.feature.trash(mapId, layerId, featureIds, token)
el.path.vector.timestamp.feature.recover(mapId, layerId, featureIds, token)
featureId = featureIds[0]
el.path.vector.timestamp.feature.versions(mapId, layerId, featureId, token)


###message module
el.path.vector.timestamp.feature.message.add(mapId, layerId, featureId, token, text= 'hoi')
image = np.zeros((256,256))
el.path.vector.timestamp.feature.message.add(mapId, layerId, featureId, token, text= 'hoi', image = image)

messages = el.path.vector.timestamp.feature.message.get(mapId, layerId, featureIds=[featureId], token = token)

messageId = [m for m in messages['result'] if m['thumbnail'] != None][0]['id']


el.path.vector.timestamp.feature.message.getImage(mapId, layerId, messageId, token)

el.path.vector.timestamp.feature.message.trash(mapId, layerId, messageId, token)
el.path.vector.timestamp.feature.message.recover(mapId, layerId, messageId, token)


###series module
date = datetime.datetime.now()
seriesData = pd.DataFrame({'x': [1,2,3,4]})
seriesData['date'] = date
el.path.vector.timestamp.feature.series.add(pathId = mapId, timestampId = layerId, featureId = featureId, seriesData = seriesData, token = token)


el.path.vector.timestamp.feature.series.info(mapId, layerId, featureId,token)

r = el.path.vector.timestamp.feature.series.get(mapId, layerId, featureId, token = token, listAll = True)


seriesId = r['result']['id'].values[0]

el.path.vector.timestamp.feature.series.trash(mapId, layerId, featureId, [seriesId], token)

el.path.vector.timestamp.feature.series.recover(mapId, layerId, featureId, [seriesId], token)

el.path.vector.timestamp.feature.series.changelog(mapId, layerId, featureId, token = token)


0
#style module

parameters = {"alpha":0.5,"width":2,"radius":{"method":"constant","parameters":{"value":7}},"property":"gml_id"}
styleId = el.path.vector.style.add(mapId, 'test', 'random', parameters, token = token, default = False)['id']

el.path.vector.style.edit(mapId, styleId, token, name = 'sfd', default = False)
el.path.vector.style.delete(mapId, styleId, token)


## properties module
featurePropertyId = el.path.vector.featureProperty.add(pathId = mapId, name = 'new', featurePropertyType = 'string', token = token)['id']
el.path.vector.featureProperty.trash(mapId,  featurePropertyId, token)

el.path.vector.featureProperty.recover(mapId, featurePropertyId, token)
el.path.vector.featureProperty.edit(mapId, featurePropertyId, token, required = True)

### order module

orderId = el.path.vector.timestamp.order.add(mapId, layerId, token, extent = {'xMin':xMin, 'xMax':xMax, 'yMin':yMin, 'yMax':yMax})['id']

order = el.path.vector.timestamp.order.get(token)[0]
while order['status'] != 'completed':
    time.sleep(1)
    order = el.path.vector.timestamp.order.get(token)[0]

file_out = '/home/daniel/Downloads/out.zip'
el.path.vector.timestamp.order.download(orderId, file_out, token)
os.remove(file_out)    
el.path.trash(mapId, token)




########3some more specific bounds tests
rasterId = '56e20fa2-f014-44c1-b46a-cde78e7e6b7e'
timestampId = el.path.get(rasterId,token)['raster']['timestamps'][0]['id']
el.path.raster.timestamp.upload.get(pathId = rasterId, timestampId = timestampId, token = token)

el.path.raster.timestamp.getBounds(pathId = rasterId, timestampId = timestampId, token=token)

vectorId = '67e66823-8bbc-4ace-816a-c4e34282676c'
timestampId = 'bc73c75a-cc74-4bb5-a609-ef01992bcc9a'

el.path.vector.timestamp.upload.get(pathId = vectorId, timestampId = timestampId, token = token)

el.path.vector.timestamp.getBounds(pathId = vectorId, timestampId = timestampId, token=token)




