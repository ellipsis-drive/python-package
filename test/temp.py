import ellipsis as el
import numpy as np

token = el.account.logIn('demo_user', 'demo_user')

#layer id and timestamp id of the layer hosting a (collection of) sentinel 2 asset(s), when using files of your own please create a layer, upload your files to that layer and use the respective id's
pathId = '54cc076b-1d69-4126-9296-52286def7cc0'
timestampId = '523caede-9f96-49fa-a855-3e546bcd365d'

#setup your needed server side environment
#specify the needed PIP packages
requirements = ['numpy']
#specify the number of nodes to parralelize over
nodes = 2
#specify the layer or layers you wish to run you analytics on, in this example we use 1 single layer
layers = [ {'pathId':pathId, 'timestampId':timestampId}]
#now create the environment, make sure to specify lareResult=False as we are performing a mapReduce and hence will be creating a small result
computeId = el.compute.createCompute(layers = layers, token=token, nodes = nodes,interpreter='python3.12', requirements = requirements, largeResult=False)['id']

def f(params):
 import numpy as np
 #the raster as numpy array and extent as dictionary can be found in the input parameters of the function
 r = params['523caede-9f96-49fa-a855-3e546bcd365d']['raster']
 extent = params['523caede-9f96-49fa-a855-3e546bcd365d']['extent']
 #calculate the ndvi
 ndvi = (r[7,:,:] - r[3,:,:])/(r[3,:,:] + r[7,:,:])
 return np.nanmax(ndvi)

#execute the function on serverside environment by referencing the environment id
r = el.compute.execute(computeId=computeId, token=token, f=f)

#The results will be a list, each item in the list is the maximum value within the shard
print(r)

#to get the overall maximum we perform the 'reduce' step and take the maximum of the resulting list
print(np.max(r))

#terminate the environment

el.compute.terminateAll(token)


