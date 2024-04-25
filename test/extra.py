
import ellipsis as el

el_extent = {'xMin': -3.22, 'xMax':-2.9, 'yMin': 57.46  , 'yMax': 57.62 }


result = el.path.vector.timestamp.getFeaturesByExtent(
    pathId="6096c5f9-4a70-4f79-b6cc-f1e501cfd47b",
    timestampId="ab904298-9d17-4fb6-a6d8-bec07e8c7c17",
    propertyFilter=[{"key": "roadFunction", "operator": "=", "value": "Local Road"}],
    extent=el_extent,
    token=token)['result']

result.plot()

