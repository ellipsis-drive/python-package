import ellipsis as el
import datetime
import os
import time
import numpy as np
import pandas as pd

from test.pointCloud import timestampId

el.path.folder.listFolder()

import dill
with open('/home/daniel/Downloads/nonTrivial.dill', "rb") as dill_file:
 f = dill.load(dill_file)
f(r , None, None)


import os

token = 'epat_S8uBdcJ8GqjUeh5ycJqXurMKHYnrs5BZT002G4nWWQu6Enl6TrDvtAzK1I9RPQmk'
file = '/home/daniel/Ellipsis/db/zone0.tif'


pathId = 'cc889803-e643-4384-9b73-a89c8f09dd65'
timestampId = 'cc889803-e643-4384-9b73-a89c8f09dd65'
el.path.raster.timestamp.file.add(pathId=pathId, timestampId=timestampId, fileFormat='tif', filePath = file, token = token)



file = '/home/daniel/Ellipsis/keys/admin'
with open(file,'r') as c:
    password = c.read()
password = password[0:-1]
token = el.account.logIn('admin', password)


####################################

#python3 setup.py sdist bdist_wheel
#twine upload --repository pypi dist/*


##access token
el.account.accessToken.create(description = 'hoi', accessList = [{'pathId': '46e1e919-8b73-42a3-a575-25c6d45fd93b' , 'access':{'accessTier':'view'}}], token = token)
tokenId = el.account.accessToken.get(token, listAll = True)['result'][0]['id']
el.account.accessToken.revoke(accessTokenId = tokenId, token = token)

folderId = '46e1e919-8b73-42a3-a575-25c6d45fd93b'



##account
demo_token = el.account.logIn("demo_user", "demo_user")
admin_token = el.account.logIn(username = 'admin', password='')
daan_token = el.account.logIn('daan', "")

el.account.listRoot('myDrive', pathTypes = ['raster'], token = demo_token)

el.account.listRoot('sharedWithMe',pathTypes = ['folder'], token = demo_token)

r_raster = el.path.search(pathTypes = ['raster'], token=token);

r_vector = el.path.search(pathTypes = ['vector'], token=token);


#domains

pathId = '1eea3d2f-27b3-4874-b716-87852c3407c1'
setDomains(pathId = pathId, token = daan_token, domains = ['hoi'])
setDomains(pathId = pathId, token = daan_token, domains = None)


####account
token = logIn('admin', 'k67cFGK1ued6aPP')

layers = [{'pathId':'07c6ad34-9e0b-494f-9c8c-3f5cfbc1b76f', 'timestampId':'7cf1c34b-b863-419f-9dd5-33eb6ab8b2ac'}]
clusterId = createCluster(layers = layers, token=token, requirements = ['numpy'], nodes = 2)['id']

def f(params):
    r = params['7cf1c34b-b863-419f-9dd5-33eb6ab8b2ac']['raster']
    z = np.max(r)
    return z

out = execute(clusterId=clusterId, f=f, token = token)


###files
filePath = '/home/daniel/Ellipsis/db/testset/0.tif'
pathId = el.path.file.add(filePath, demo_token)['id']
time.sleep(10)
el.path.file.download(pathId = pathId, filePath =  '/home/daniel/Downloads/out.tif')
el.path.trash(pathId, demo_token)
el.path.delete(pathId, demo_token)


##user

result = el.user.search('daan')
daanId = [x for x in result if x['username'] == 'daan'][0]['id']
el.user.get(daanId)


##path
rasterInfo = el.path.get('59caf510-bab7-44a8-b5ea-c522cfde4ad7', token)

info = el.path.get(folderId, token)

folderId = info['id']
maps = el.path.folder.listFolder(folderId, pathTypes=['raster', 'vector', 'pointCloud'], token = token, listAll = True)
folders = el.path.folder.listFolder(folderId, pathTypes=['folder'], token = token, listAll = True)

mapId = [ m for m in maps['result'] if not m['trashed'] ][0]['id']


#crash


el.path.editMetadata(pathId = mapId, token = token, description = 'test')

addedFolderId = el.path.folder.add(  'test', token = token, parentId = folderId)['id']

el.path.trash(addedFolderId, token)
el.path.recover(addedFolderId, token)

addedRasterId = el.path.raster.add(  'test2', token = token, parentId = folderId)['id']

el.path.move([addedRasterId], addedFolderId, token)


el.path.trash(addedFolderId, token)
el.path.delete(pathId = addedFolderId, token = token, recursive = True)


el.path.editPublicAccess(pathId = folderId, token = token, access={'accessTier':'none'}, hidden = False)
el.path.editPublicAccess(pathId = folderId, token = token, access= {'accessTier':'view'}, hidden = True)

folderId = '58f62140-5aad-44b0-b6dc-996a9a84a601'
el.path.editPublicAccess(pathId = folderId, token = token, access= {'accessTier':'view'}, hidden = True, recursive=True)

while True:
    r = el.path.folder.listFolder(pathId= '4a46947c-eb49-435d-af79-71d238df0bc5', listAll=True, token = token)['result']
    print(r)

el.path.favorite(folderId, token=token)
el.path.unfavorite(folderId, token=token)

###invites
inviteId =  el.path.invite.send(pathId = folderId, token=token, userId = daanId, access = {'accessTier': 'view+', 'processingUnits':10000})['id']

el.path.invite.getPathInvites(folderId, token)


el.path.invite.getYourInvites(daan_token)

el.path.invite.revoke(pathId = folderId, inviteId = inviteId, token = token)


inviteId =  el.path.invite.send(pathId = folderId, token=token, userId = daanId, access = {'accessTier': 'view+', 'processingUnits':10000})['id']

el.path.invite.decline(folderId, inviteId, daan_token)


inviteId =  el.path.invite.send(pathId = folderId, token=token, userId = daanId, access = {'accessTier': 'view+', 'processingUnits':10000})['id']
el.path.invite.accept(folderId, inviteId, daan_token)

##members
members = el.path.member.get(folderId, token, memberType = ['direct'])


daanMemberId = [m['user']['id'] for m in members if m['user']['username'] == 'daan'][0]

el.path.member.edit(pathId = folderId, userId = daanMemberId, access = {'accessTier' : 'view+'} ,token = token)

el.path.member.delete(folderId, daanMemberId, token)

##usage
pathId = '8a11c27b-74c3-4570-bcd0-64829f7cd311'

users = el.path.usage.getActiveUsers(pathId = pathId, token = token, listAll=True)
el.path.usage.getUsage(pathId = pathId, userId = users['result'][0]['user']['id'], token =token)
el.path.usage.getAggregatedUsage(pathId = pathId, loggedIn = False, token = token)

###pointclouds
import ellipsis as el
mapId = el.path.pointCloud.add( 'test', token, parentId = folderId)['id']
timestampId = el.path.pointCloud.timestamp.add(mapId, token)['id']
dateFrom = datetime.datetime.now()
dateTo = datetime.datetime.now()
el.path.pointCloud.timestamp.edit(mapId, timestampId, token, description = 'hoi', date={'from': dateFrom, 'to':dateTo})

filePath = '/home/daniel/Ellipsis/db/testset/jpn_tokyo/Ellipsoid/vricon_point_cloud/data/1394041e_354047n_20200624T091403Z_ptcld.laz'
uploadId = el.path.pointCloud.timestamp.file.add(pathId = mapId, timestampId = timestampId, filePath = filePath, fileFormat = 'laz', epsg= 3095, token = token)['id']
time.sleep(10)
el.path.pointCloud.timestamp.file.download(pathId = mapId, timestampId = timestampId, fileId = uploadId, filePath = '/home/daniel/Downloads/out.laz', token = token)
os.remove('/home/daniel/Downloads/out.laz')
el.path.pointCloud.timestamp.file.trash(pathId = mapId, timestampId = timestampId, fileId= uploadId, token = token)
el.path.pointCloud.timestamp.file.recover(pathId = mapId, timestampId = timestampId, fileId= uploadId, token = token)
el.path.pointCloud.timestamp.file.trash(pathId = mapId, timestampId = timestampId, fileId= uploadId, token = token)
el.path.pointCloud.timestamp.file.delete(mapId, timestampId, uploadId, token)
uploadId = el.path.pointCloud.timestamp.file.add(pathId = mapId, timestampId = timestampId, filePath = filePath, fileFormat = 'laz', epsg= 3095, token = token)['id']

uploads = el.path.pointCloud.timestamp.file.get(mapId, timestampId, token)


el.path.pointCloud.timestamp.activate(mapId, timestampId, token)

while el.path.get(mapId, token)['pointCloud']['timestamps'][0]['status'] != 'active':
    time.sleep(2)

el.path.pointCloud.timestamp.deactivate(mapId, timestampId, token)
while el.path.get(mapId, token)['pointCloud']['timestamps'][0]['status'] != 'passive':
    time.sleep(2)
el.path.pointCloud.timestamp.activate(mapId, timestampId, token)

info = el.path.get(mapId, token)
timestamp = info['pointCloud']['timestamps'][0]
while timestamp['status'] != 'active':
    time.sleep(1)
    info = el.path.get(mapId, token)
    timestamp = info['pointCloud']['timestamps'][0]



el.path.pointCloud.timestamp.trash(mapId, timestampId, token)
el.path.pointCloud.timestamp.recover(mapId, timestampId, token)
el.path.pointCloud.timestamp.trash(mapId, timestampId, token)
el.path.pointCloud.timestamp.delete(mapId, timestampId, token)

el.path.trash(mapId, token)
el.path.recover(mapId, token)
el.path.trash(mapId, token)
el.path.delete(mapId, token)

####data fetching
import ellipsis as el
pathId = 'fe5cb352-ccda-470b-bb66-12631c028def'
timestampId = '7dd94eac-f145-4a8a-b92d-0a22a289fe21'
extent = {    'xMin':5.7908,'xMax':5.79116,'yMin':51.93303,'yMax':51.93321}
epsg = 4326
token = None
zoom = None


df = el.path.pointCloud.timestamp.fetchPoints(pathId, timestampId, extent, token= None, epsg = epsg, zoom = zoom)

el.util.plotPointCloud(df, method = 'cloud')
el.util.plotPointCloud(df, method = 'voxel')
el.util.plotPointCloud(df, method = 'mesh', scale = 0.06)

##raster and uploads
mapId = el.path.raster.add( 'test', token, parentId = folderId)['id']
el.path.raster.edit(mapId, token, interpolation = 'nearest')


timestampId = el.path.raster.timestamp.add(mapId, token)['id']


dateFrom = datetime.datetime.now()
dateTo = datetime.datetime.now()
el.path.raster.timestamp.edit(mapId, timestampId, token, description = 'hoi', date={'from': dateFrom, 'to':dateTo})

filePath = '/home/daniel/Ellipsis/python-package/test/0.tif'
uploadId = el.path.raster.timestamp.file.add(pathId = mapId, timestampId = timestampId, filePath = filePath, fileFormat = 'tif', token = token,noDataValue = -1)['id']
time.sleep(10)
el.path.raster.timestamp.file.download(pathId = mapId, timestampId = timestampId, fileId = uploadId, filePath = '/home/daniel/Downloads/out.tif', token = token)
os.remove('/home/daniel/Downloads/out.tif')
el.path.raster.timestamp.file.trash(pathId = mapId, timestampId = timestampId, fileId= uploadId, token = token)
el.path.raster.timestamp.file.recover(pathId = mapId, timestampId = timestampId, fileId= uploadId, token = token)
el.path.raster.timestamp.file.trash(pathId = mapId, timestampId = timestampId, fileId= uploadId, token = token)
el.path.raster.timestamp.file.delete(mapId, timestampId, uploadId, token)
uploadId = el.path.raster.timestamp.file.add(pathId = mapId, timestampId = timestampId, filePath=filePath, fileFormat='tif', token = token)['id']

uploads = el.path.raster.timestamp.file.get(mapId, timestampId, token)


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

import ellipsis as el
token = el.account.logIn('demo_user', 'demo_user')


mapId = '0ce1a67a-3d10-4970-967b-c8880e3c7d67'
timestampId = 'dfb56c4e-5d3f-436e-9676-701843c09456'




xMin  = 4.35431
yMin=  51.81081
xMax  = 6.47156
yMax  = 53.00261

extent = {'xMin':xMin,'yMin':yMin,'xMax':xMax,'yMax':yMax } 


result = el.path.raster.timestamp.getRaster(pathId = mapId, timestampId = timestampId,  extent = extent, token = token, epsg = 4326)
raster = result['raster']
el.util.plotRaster(raster[0,:,:])

r = el.path.raster.timestamp.getSampledRaster(pathId = mapId, timestampId=timestampId, extent = extent, width = 1024, height = 1024, epsg=4326, token = token)
raster = r['raster']
el.util.plotRaster(raster[0,:,:])

res = el.path.raster.timestamp.contour(pathId = mapId, timestampId = timestampId, extent = extent, epsg = 4326, bandNumber = 1, token = token)
res.plot()

bounds = el.path.raster.timestamp.getBounds(mapId, timestampId, token)

data = el.path.raster.timestamp.analyse(mapId, [timestampId], bounds, token=token, epsg = 4326)

locations = [[5.32394, 52.11856],[5.32394, 52.11856],[5.32394, 52.11856]]

results = el.path.raster.timestamp.getLocationInfo(pathId = mapId, timestampId = timestampId, locations = locations, epsg = 4326, token= token)


###raster downloads
mapId = '1eea3d2f-27b3-4874-b716-87852c3407c1'
timestampId = "ba5b418a-a39e-4d84-9411-e23c096085a3"
uploads = el.path.raster.timestamp.file.get(mapId, timestampId, token)
uploadId = uploads['result'][0]['id']

file_out = '/home/daniel/Downloads/out.tif'
time.sleep(10)
el.path.raster.timestamp.file.download(pathId = mapId, timestampId = timestampId, token = token, fileId = uploadId, filePath = file_out)
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
mapId = el.path.vector.add( 'test3', token)['id']


layerId = el.path.vector.timestamp.add(mapId,  token = token)['id']

el.path.vector.timestamp.edit(mapId, layerId, token, description = 'adsfd')

el.path.vector.timestamp.trash(mapId, layerId, token)
el.path.vector.timestamp.recover(mapId, layerId, token)
el.path.vector.timestamp.trash(mapId, layerId, token)
el.path.vector.timestamp.delete(mapId, layerId, token)
layerId = el.path.vector.timestamp.add(mapId, description = 'test', token = token)['id']


###vector uploads
filePath = '/home/daniel/Ellipsis/python-package/test/test.zip'
uploadId = el.path.vector.timestamp.file.add(pathId = mapId, timestampId = layerId, filePath = filePath, token = token, fileFormat = 'zip')['id']
time.sleep(10)
file_out = '/home/daniel/Downloads/out.zip'
el.path.vector.timestamp.file.download(pathId = mapId, timestampId = layerId, fileId = uploadId, filePath = file_out, token = token)
os.remove(file_out)

upload = el.path.vector.timestamp.file.get(pathId = mapId,  timestampId = layerId, token = token)['result'][0]
while upload['status'] != 'completed':
    time.sleep(1)
    upload = el.path.vector.timestamp.file.get(pathId = mapId,  timestampId = layerId, token = token)['result'][0]


#layer methods
bounds = el.path.vector.timestamp.getBounds(mapId, layerId, token)

xMin = bounds.bounds[0]
yMin = bounds.bounds[1]
xMax = bounds.bounds[2]
yMax = bounds.bounds[3]

bounds = {'xMin':xMin, 'xMax':xMax, 'yMin':yMin, 'yMax':yMax}
sh = el.path.vector.timestamp.getFeaturesByExtent(pathId = mapId, timestampId = layerId, extent =  bounds, token = token, listAll = False, epsg = 4326)
sh = el.path.vector.timestamp.getFeaturesByExtent(pathId = mapId, timestampId = layerId, extent =  bounds, token = token, listAll = False, pageStart = sh['nextPageStart'], epsg = 4326)

sh['result'].plot()
time.sleep(30)
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

el.path.vector.timestamp.feature.add(mapId, layerId, features, token, cores = 10)

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
el.path.delete(mapId, token)




########3some more specific bounds tests
rasterId = '56e20fa2-f014-44c1-b46a-cde78e7e6b7e'
timestampId = el.path.get(rasterId,token)['raster']['timestamps'][0]['id']
el.path.raster.timestamp.file.get(pathId = rasterId, timestampId = timestampId, token = token)

el.path.raster.timestamp.getBounds(pathId = rasterId, timestampId = timestampId, token=token)

vectorId = '67e66823-8bbc-4ace-816a-c4e34282676c'
timestampId = 'bc73c75a-cc74-4bb5-a609-ef01992bcc9a'

el.path.vector.timestamp.file.get(pathId = vectorId, timestampId = timestampId, token = token)

el.path.vector.timestamp.getBounds(pathId = vectorId, timestampId = timestampId, token=token)




###hashtags
pathId = '59caf510-bab7-44a8-b5ea-c522cfde4ad7'
el.path.hashtag.add(pathId = pathId, hashtag = 'xxx', token = token)
el.path.hashtag.search('x')
el.path.hashtag.delete(pathId = pathId, hashtag = 'xxx', token = token)

####bookmarks

import ellipsis as el
token = el.account.logIn('demo_user', 'demo_user')
pId = '075eb94f-741f-4f4a-8ce5-731c9a72a324'
bookmark = {'layers':  [{'type':'ellipsis', 'id':pId, 'selected':True }, {'type':'base', 'selected':True }], 'dems':[]}
bookmarkId = el.path.bookmark.add( name = 'temp',bookmark=bookmark, token = token)['id']

info = el.path.bookmark.get(pathId = bookmarkId, token = token)

dems = [{'type':'ellipsis', 'id':pId, 'selected':False }]
el.path.bookmark.edit(pathId = bookmarkId, token = token, dems = dems)

el.path.trash(pathId= bookmarkId, token = token)



import ellipsis as el
import numpy as np
from io import BytesIO
import geopandas as gpd

token = el.account.logIn('demo_user', 'demo_user')

r = np.zeros((4,100,1000))

extent = {'xMin':0, 'xMax':10, 'yMin':0, 'yMax':10}
out = el.util.saveRaster(r, targetFile= BytesIO(), epsg =  3857, extent=extent)

el.path.raster.timestamp.file.add(pathId = 'f3f55c63-4f22-4dac-8d96-cd9a38069ee2', timestampId='edadda02-e4c1-4577-b349-aa3a8679c843', memFile=out, token = token, fileFormat='tif', name = 'test.tif')


sh = gpd.read_file('/home/daniel/Ellipsis/db/testset/buildings_mini')
b = BytesIO()
out = el.util.saveVector(features = sh, targetFile = b)
el.util.saveRaster()
el.path.vector.timestamp.file.add(pathId = 'c6a341e1-59bf-44f8-a0d7-0962415a8fa2', timestampId= 'ad490f78-0cf0-426e-9238-e0ef803c7371', token = token, fileFormat='gpkg', memFile=out, name = 'test.gpkg')



###add series
import geopandas as gpd
import numpy as np
import pandas as pd
import datetime
layerId = el.path.vector.add(name = 'series test', token = token)['id']
timestampId = el.path.vector.timestamp.add(pathId = layerId, token = token)['id']

features = gpd.read_file('/home/daniel/Ellipsis/db/testset/buildings_mini')

featureIds = el.path.vector.timestamp.feature.add(pathId = layerId, timestampId=timestampId, features=features, token = token)
N = 1000
x = [float(x) for x in np.arange(N)]
featureId = np.repeat(featureIds[0], N)
date = np.repeat( datetime.datetime.now(),N)
seriesData = pd.DataFrame({'date':date, 'featureId': featureId, 'x':x })
seriesData['x'].values[4] = np.nan
el.path.vector.timestamp.feature.series.add(pathId = layerId, timestampId = timestampId, uploadAsFile = True, seriesData=seriesData, token=token)

t = pd.read_csv('/home/daniel/Downloads/test.csv')


import ellipsis as el
pathId = '3a5351e8-0333-47c6-9124-06b9971c9f99'
timestampId = '78c9a95a-57a7-4db6-a029-33c85a3f75e3'

token = el.account.logIn('demo_user', 'demo_user')

#wijzig alle namen binnen een extent

#haal de huidige features op
extent = {'xMin':2, 'xMax':6, 'yMin':53, 'yMax':54}
features = el.path.vector.timestamp.getFeaturesByExtent(pathId, timestampId, extent)['result']
featuresIds = features['id'].values
#update de features hoe je wil
features['bottum'] = 'up'
#submit de aangepaste features
el.path.vector.timestamp.feature.edit(pathId, timestampId, featureIds, token, newFeatures)

import ellipsis as el
r = el.path.raster.timestamp.getRaster(pathId = '07125c90-bfde-4036-b85e-b1fdee861ca6', timestampId= 'aa23ec66-91bb-4276-a98c-1b45b6a962fb', extent= {'xMin':70.75458, 'yMin':29.17649 , 'xMax':81.69791, 'yMax': 31.97394 }, epsg=4326)

el.util.plotRaster(r['raster'])
