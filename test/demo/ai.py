from keras import layers
import keras
import  ellipsis as el


token = el.account.logIn('demo_user', 'demo_user')

def get_model(img_size, num_classes):
    inputs = keras.Input(shape=img_size + (4,))


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



model_json = model.to_json()

model_file = '/home/daniel/Downloads/model_json.json'
with open(model_file, 'w') as c:
    c.write(model_json)


projectFolderId = 'd439e896-5a2b-47f4-bfa0-987184b7781f'

modelFileId = el.path.file.add(token, filePath = model_file, parentId = projectFolderId)['id']

layerToSegmentId = '9ca35534-491c-409d-9f02-47ddf3251f99'
timestampToSegmentId = '1703b3aa-87c4-4e0a-a6b5-16aae433de1a'

files = [modelFileId]
layers = [{'pathId' : layerToSegmentId, 'timestampId': timestampToSegmentId}]
requirements = ['numpy', 'tensorflow', 'keras', 'ellipsis']

computeId = el.compute.createCompute(layers=layers, token = token, files=files, nodes=3, requirements = requirements, largeResult = True)['id']


targetLayerId = el.path.raster.add(name = 'classificationLayer', token=token, parentId = projectFolderId)['id']
targetTimestampId = el.path.raster.timestamp.add(pathId = targetLayerId, token= token)['id']


def f(params):
    import tensorflow as tf
    import io
    import ellipsis as el
    import numpy as np
    import math

    model_file = params['93ce239c-f517-4827-89d0-904292194a9f']
    r = params['1703b3aa-87c4-4e0a-a6b5-16aae433de1a']['raster']
    transform = params['1703b3aa-87c4-4e0a-a6b5-16aae433de1a']['transform']


    x = model_file.read()
    model_string = x.decode()
    model = tf.keras.models.model_from_json(model_string)
    r = np.transpose(r, [1, 2, 0])

    output = np.zeros((r.shape[0], r.shape[1]))

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
            im = r[i_start:i_end, j_start:j_end, :]
            im = np.expand_dims(im, axis=0)
            val_preds = model.predict(im)
            val_preds = np.squeeze(val_preds)

            mask = np.argmax(val_preds[i], axis=-1)
            output[i_start:i_end, j_start:j_end] = mask

    memFile = io.BytesIO()
    output = np.expand_dims(output, axis=0)
    outFile = el.util.saveRaster(output, transform=transform, targetFile=memFile, epsg=3857)

    return outFile


el.compute.execute(computeId, f, token, writeToLayer = {'pathId': targetLayerId, 'timestampId':targetTimestampId})

el.path.editPublicAccess(pathId=targetLayerId, access= {'accessTier':'view'}, token = token)
el.path.invite.send(pathId = targetLayerId, access = {'accessTier':'view', 'processingUnits':10*1000}, email = 'daniel@ellipsis-drive.com', token = token)

print('for users with access the result can now be seen at https://app.ellipsis-drive.com/view?pathId=' + targetLayerId)

el.compute.terminateCompute(computeId, token)

el.compute.terminateAll(token)