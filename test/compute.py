import ellipsis as el
import pandas as pd
import geopandas as gpd
#pathId and timestampId of the vector layer to analyse
pathId = '4d695990-ace7-434e-b703-e1d5ae006800'
timestampid = '098807b0-2280-4cbc-abba-438784b6f867'



#obtain a token
token = el.account.logIn('admin', '')


#create a cluster with the vector layer containing all USA houses loaded
layers = [{'pathId':'78cb1955-2910-4ede-9d21-2c6472d0ba71', 'timestampId':'bccf1299-cd42-4dff-bfa5-10fe650dad39' } ]
clusterId = createCluster(layers = layers, token = token, requirements=['numpy','pandas','geopandas'], nodes=1)['id']

def f(params):
    return params

res = execute(clusterId, f, token, awaitTillCompleted=True)

terminateCluster(clusterId, token, awaitTillTerminated = True)


getClusterInfo(clusterId, token)


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


