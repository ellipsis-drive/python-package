#importing packages
import ellipsis as el
import pandas as pd
import time
import random

t1 = time.time()

# token and ids for the hail layer
token_hail = 'epat_YrkSvIBdOZ6Elup1UUUH3wHGEGd4iM5UpqH6U1l2BxdZp6E9BulaGMVhX2UvBhAG'
pathId_hail = 'f015c614-54e8-4ba6-8204-d50ce37e0f58'
timestampId_hail = '14c7ec8a-9ae8-4ae7-be3d-fac3b214b0fa'

#token and ids for the insured locations layer
pathId_locations = '6d81d8ed-8d57-4455-9795-359ed59f8f15'
timestampId_locations = 'ec179761-54f0-4e55-bd84-43fabc58838a'
token_locations = 'epat_KB8TEw6C4JJjpxdTqOumtQYlQAiMYQbaGMedJoD7wGAALDJuj96Nxbck5vCGNoqh'

#find extent of the hail storm
info = el.path.get(pathId_hail, token_hail)
extent = info['vector']['timestamps'][0]['extent']

#retrieve locations within the area page by page and filter them based on whether they fell within the hail storm contours
shs = []
pageStart = None
while True:
    #fetch some locations
    r = getFeaturesByExtent(pathId_locations, timestampId=timestampId_locations, token = token_locations, extent = extent, listAll=False, pageStart=pageStart, pageSize = 300)
    sh = r['result']
    locations = [ p for p in zip(sh.bounds['minx'].values.tolist(), sh.bounds['miny'].values.tolist()) ]
    #find what hail storm contours they intersect with
    r_info = getLocationInfo(pathId = pathId_hail, timestampId=timestampId_hail, token = token_hail, locations=locations)
    sh['hail_impact'] = r_info
    #remove all locations that did not intersect with any contour
    keep = [ x != [] for x in r_info]
    sh = sh[keep]
    #place the found locations in the list togehter with the information of the intersecting hail contour
    shs.append(sh)
    #store the nextPage start for the next iteration
    pageStart = r['nextPageStart']

    #if there is no pagestart exit the loop
    if type(pageStart) == type(None):
        break

#concatenate all results
sh = pd.concat(shs)

#print the number of found locations
print('found ', sh.shape[0], ' impacted locations')

#from all intersecting contours take the one with the highest impact
sh['hail_impact'] = [ max([z['HAIL_SZ_VA'] for z in x])  for x  in sh['hail_impact'].values ]

#print resulting dataframe
print(sh)

t2 = time.time()
print('Execution time was', t2-t1, ' seconds')


#we can now write these impacted locations to a new layer to share with others

outputFolderId = '1b35b457-f143-449d-a528-cdda1098829c'
outputName = 'impacted locations ' + str(random.randint(1,1000))

layerId = el.path.vector.add(name=outputName, token=token_locations, parentId=outputFolderId)['id']
timestampId = el.path.vector.timestamp.add(pathId = layerId, token = token_locations)['id']


el.path.vector.timestamp.feature.add(pathId = layerId, timestampId=timestampId, token = token_locations, features=sh)


print('locations can now be viewed at https://app.ellipsis-drive.com/view?pathId=' + layerId)
