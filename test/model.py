from keras import layers
import keras
import tensorflow as tf
from mpl_toolkits.mplot3d.proj3d import transform


def get_model(img_size, num_classes):
    inputs = keras.Input(shape=img_size + (3,))

    ### [First half of the network: downsampling inputs] ###

    # Entry block
    x = layers.Conv2D(32, 3, strides=2, padding="same")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    # Blocks 1, 2, 3 are identical apart from the feature depth.
    for filters in [64, 128, 256]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(filters, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    ### [Second half of the network: upsampling inputs] ###

    for filters in [256, 128, 64, 32]:
        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.UpSampling2D(2)(x)

        # Project residual
        residual = layers.UpSampling2D(2)(previous_block_activation)
        residual = layers.Conv2D(filters, 1, padding="same")(residual)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    # Add a per-pixel classification layer
    outputs = layers.Conv2D(num_classes, 3, activation="softmax", padding="same")(x)

    # Define the model
    model = keras.Model(inputs, outputs)
    return model

img_size = (256,256)
num_classes = 10
# Build model
model = get_model(img_size, num_classes)
model.summary()

model_json = model.to_json()


with open('/home/daniel/Downloads/model_json.json', 'w') as c:
    c.write(model_json)

with open('/home/daniel/Downloads/model_json.json', 'rb') as c:
    x = c.read()

model_string = x.decode()

model = tf.keras.models.model_from_json(model_string)

import numpy as np
im = np.zeros((1,256,256,3))

output = model.predict(im)



import ellipsis as el

el.apiManager.baseUrl =  'https://api.ellipsis-drive.com/v3'





requirements = ['numpy', 'tensorflow', 'keras']
nodes = 1

layers = [ {'pathId':'1493ee0e-27b7-4ec5-bc69-2aad02029573', 'timestampId':'3644ad3f-e0d5-47a1-84f1-3f9957f6c702'}]
files = ['3898d2db-a0aa-4a01-a3b3-41f881047e16']

computeId = el.compute.createCompute(layers = layers, files = files, token=token, nodes = nodes,interpreter='python3.12', requirements = requirements, largeResult=False)['id']


def f(params):
    import tensorflow as tf
    import numpy as np

    model_file = params['3898d2db-a0aa-4a01-a3b3-41f881047e16']
    x = model_file.read()
    model_string = x.decode()
    model = tf.keras.models.model_from_json(model_string)

    im = np.zeros((1, 256, 256, 3))

    output = model.predict(im)
    return float(np.max(output))

r = el.compute.execute(computeId, f, token)

print(r)


el.compute.terminateAll(token=token)



import ellipsis as el






requirements = ['numpy', 'tensorflow', 'keras', 'ellipsis']
nodes = 1

layers = [ {'pathId':'1493ee0e-27b7-4ec5-bc69-2aad02029573', 'timestampId':'3644ad3f-e0d5-47a1-84f1-3f9957f6c702'}]
files = ['3898d2db-a0aa-4a01-a3b3-41f881047e16']


computeId = el.compute.createCompute(layers = layers, files = files, token=token, nodes = nodes,interpreter='python3.12', requirements = requirements, largeResult=True)['id']


def f(params):
    import tensorflow as tf
    import numpy as np
    import ellipsis as el
    from io import BytesIO
    model_file = params['3898d2db-a0aa-4a01-a3b3-41f881047e16']
    x = model_file.read()
    model_string = x.decode()
    model = tf.keras.models.model_from_json(model_string)

    im = np.zeros((1, 256, 256, 3))

    output = model.predict(im)

    r = params['3644ad3f-e0d5-47a1-84f1-3f9957f6c702']['raster']
    transform = params['3644ad3f-e0d5-47a1-84f1-3f9957f6c702']['transform']
    b = BytesIO()
    el.util.saveRaster(output[0,:,:,:], 3857, transform=transform, targetFile=b)

    return b

targetPathId = 'b4acc853-8836-4945-aa9e-631b14ee388b'
targetTimestampId = el.path.raster.timestamp.add(pathId = targetPathId, token =token)['id']

r = el.compute.execute(computeId, f, token, writeToLayer = {'pathId': targetPathId, 'timestampId':targetTimestampId})

#r = el.compute.execute(computeId, f, token)


print(r)


el.compute.terminateAll(token=token)
