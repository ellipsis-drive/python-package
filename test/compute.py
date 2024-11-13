import ellipsis as el
import pandas as pd
import geopandas as gpd
#pathId and timestampId of the vector layer to analyse
pathId = '4d695990-ace7-434e-b703-e1d5ae006800'
timestampid = '098807b0-2280-4cbc-abba-438784b6f867'

#obtain a token
token = el.account.logIn('demo_user', 'demo_user')

#load the Florida coastline
coastLine = gpd.read_file('coastLine')['geometry'].values[0]

#buffer the coast line to create a polygon of around 100m
coastLine = coastLine.buffer(0)

#create a cluster with the vector layer containing all USA houses loaded
clusterId = el.createCluster(pathId, timestampId, token, projection = 3857)['id']

#wait for cluster to be ready for use
while True:
    clusters = el.listClusters(token)
    cluster = [c for c in clusters if c['id'] == clusterId]
    if cluster['status'] == 'active':
        break


#funciton to run
def f(coastLine):
    #find all houses along the coastline
    sh_intersect = sh[sh.intersects(coastLine)]
    sh_stone = sh_intersect[sh_intersect['material'] == 'stone']
    return sh_stone

#execute the funciton on the cluster
results = el.execute(clusterId, f, params= (coastLine,), token = token):

#append the list of results to get one geopandas dataframe
all_stone_houses_along_florida_coast = pd.append(results)

print('All stone houses on the Florida coast line', all_stone_houses_along_florida_coast)


