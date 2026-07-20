#importing packages
import pandas as pd

import ellipsis as el

token = 'epat_KB8TEw6C4JJjpxdTqOumtQYlQAiMYQbaGMedJoD7wGAALDJuj96Nxbck5vCGNoqh'

locations = [
[-88.84611 , 31.49216 ],
[-96.98807 , 35.90982 ],
[-100.6512 , 37.7884 ],
[-112.85443 , 40.57644],
[-149.36952 , 64.70788 ]]


riskMaps = [{'name': 'earthquake','pathId':'32953e9f-4842-487a-82cc-8d1058e356cc', 'timestampId':'b47063f2-06ed-4da9-8105-c25e8e9aaf69', 'layerType':'raster'},
            {'name': 'hurricane','pathId':'f56fdc95-ce5e-452c-9713-cd33496c08e8', 'timestampId':'e78728c5-9162-4c1a-aef6-b6914468b7bb', 'layerType':'vector'},
            {'name': 'landslide','pathId':'1d13deef-8121-4935-8813-8417751d65c4', 'timestampId':'9d1a8363-bc22-4a1d-8a95-c89e692e5c26', 'layerType':'raster'},
            {'name': 'fires','pathId':'a22485e8-d364-4c61-8a00-7a97c34f7f92', 'timestampId':'63bb2fda-4799-4685-8fbf-b31b137a4d88', 'layerType':'vector'},
            ]

df = pd.DataFrame()
df['location'] = locations
r = riskMaps[0]
for r in riskMaps:
    if r['layerType'] == 'vector':
        result = el.path.vector.timestamp.getLocationInfo(pathId = r['pathId'], timestampId = r['timestampId'], token=token, locations=locations)
        severity = [len(x) for x in result]
    else:
        result = el.path.raster.timestamp.getLocationInfo(pathId = r['pathId'], timestampId = r['timestampId'], token=token, locations=locations)
        severity = [x[0] for x in result]

    df[r['name']] = severity

print(df)