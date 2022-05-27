import ellipsis as el
import datetime

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

mapId = maps['result'][0]['id']


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

filePath = '/home/daniel/Ellipsis/db/testset/0.tif'
el.path.raster.timestamp.upload.upload(mapId, timestampId, filePath, token)


import backup
backup.uploadRasterFile(mapId, timestampId, filePath, token)


uploads = el.path.raster.timestamp.upload.get(mapId, timestampId, token)
uploadId = uploads[0]['id']
el.path.raster.timestamp.upload.delete(mapId, timestampId, uploadId, token)

filePath = '/home/daniel/Ellipsis/db/testset/0.tif'
el.path.raster.timestamp.upload.upload(mapId, timestampId, filePath, token)


el.path.raster.editBand(mapId, 1, 'hoi', token)

el.path.raster.timestamp.activate(mapId, timestampId, token)


el.path.raster.timestamp.trash(mapId, timestampId, token)
el.path.raster.timestamp.recover(mapId, timestampId, token)
el.path.raster.timestamp.trash(mapId, timestampId, token)
el.path.raster.timestamp.delete(mapId, timestampId, token)


mapId = '59caf510-bab7-44a8-b5ea-c522cfde4ad7'
timestampId = 'f25e120e-ca8f-451f-a5f4-33791db0f2c5'

bounds = el.path.raster.timestamp.getBounds(mapId, timestampId, token)

xMin  = 5.60286
yMin=  52.3031    
xMax  = 5.60315
yMax  = 52.30339

extent = {'xMin':xMin,'yMin':yMin,'xMax':xMax,'yMax':yMax } 

result = el.path.raster.timestamp.getRaster(pathId = mapId, timestampId = timestampId, bounds = extent, token = token)

raster = result['raster']


import ellipsis as el

el.util.plotRaster(raster[0:3,:,:])
