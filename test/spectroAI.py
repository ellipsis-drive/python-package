import ellipsis as el
import random
#state needed ids
pathId = '5f0327be-596a-4b6f-986e-adc59cebc4b1'
timestampId = 'e563ca12-a93f-47e0-9ba0-c58eec90d055'
modelId = '11419456-fb74-4fd4-b843-ed5b00d25e77'

token = el.account.logIn('demo_user', 'demo_user')

#create a compute environment
layers = [{'pathId':pathId, 'timestampId':timestampId}]
files = [modelId]
requirements = ['tensorflow', 'keras', 'numpy', 'ellipsis', 'rasterio']
computeId = el.compute.createCompute(layers = layers, files=files, requirements=requirements, token = token, largeResult=True, nodes = 7)['id']

#define a function to classify the raster
def f(params):
    import keras
    import math
    import numpy as np
    import io
    import tensorflow as tf
    import rasterio
    from rasterio.transform import from_bounds
    import ellipsis as el
    #use the pathId of the file as key to obtain the file as bytesIO
    model_file = params['11419456-fb74-4fd4-b843-ed5b00d25e77']
    #Read the bytesIO object as bytes
    x = model_file.read()
    #parse the bytes to a string
    model_string = x.decode()
    #read the resulting JSON string as a keras model
    model = tf.keras.models.model_from_json(model_string)

    r = params['e563ca12-a93f-47e0-9ba0-c58eec90d055']['raster']
    transform = params['e563ca12-a93f-47e0-9ba0-c58eec90d055']["transform"]


    # we execute the model by using a 256 by 256 sliding window
    output = np.zeros((1,r.shape[1], r.shape[2]))

    r = np.transpose(r, [1, 2, 0])


    for i in range(math.floor(r.shape[0] / 256)):
        if 256 * (i + 1) > r.shape[0]:
            i_start = r.shape[0] - 256
            i_end = r.shape[0]
        else:
            i_start = i * 256
            i_end = (i + 1) * 256

        for j in range(math.floor(r.shape[1] / 256)):
            if 256 * (j + 1) > r.shape[1]:
                j_start = r.shape[1] - 256
                j_end = r.shape[1]
            else:
                j_start = j * 256
                j_end = (j + 1) * 256
            val_preds = model.predict(r[i_start:i_end, j_start:j_end,0:4])
            mask = np.argmax(val_preds, axis=-1)
            output[1,i_start:i_end, j_start:j_end] = mask

    # we store the segementation output in a geotif memory file


    memFile = io.BytesIO()
    outFile = el.util.saveRaster(output, transform=transform, targetFile=memFile, epsg=3857)

    # the function needs to return the memory file, this memory file can be written to layer provided in the writeToLayer parameter in the ellipsis.compute.execute function
    return outFile


#create a layer to write the results to
out_name  = 'output' + str(random.random())
pathId_out = el.path.raster.add(name=out_name, token=token)['id']
timestampId_out = el.path.raster.timestamp.add(pathId = pathId_out, token=token)['id']
writeToLayer = {'pathId':pathId_out, 'timestampId':timestampId_out}

#execute the function
el.compute.execute(computeId=computeId, f=f, token=token, writeToLayer=writeToLayer)


#terminate the environment on the server
el.compute.terminateCompute(computeId= computeId, token = token)
#if the computeId was lost use this function to terminate all environmets
el.compute.terminateAll(token)