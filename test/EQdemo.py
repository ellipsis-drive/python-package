import ellipsis as el
import pandas as pd

token = el.account.logIn('demo_user', 'demo_user')




change_detection_pathId = '09e66753-efaa-457e-8316-074a842cac86'
change_detection_timestampId = '8881e53f-195a-48c1-8886-30f72612ac2b'

buildings_pathId = '967f5d06-ab32-4812-baab-04411730238a'
buildings_timestampId = 'f3a8a95e-811d-4bb5-8f7b-b024f0d2da96'



def f(params):
    change_detection_timestampId = '8881e53f-195a-48c1-8886-30f72612ac2b'
    buildings_timestampId = 'f3a8a95e-811d-4bb5-8f7b-b024f0d2da96'

    buildings_gpd = params[buildings_timestampId]['vector']
    change_detection_gpd = params[change_detection_timestampId]['vector']

    change_detection_union = change_detection_gpd.unary_union

    buildings_gpd = buildings_gpd[buildings_gpd.intersects(change_detection_union)]

    return buildings_gpd

layers = [{'pathId': change_detection_pathId, 'timestampId': change_detection_timestampId}, {'pathId': buildings_pathId, 'timestampId': buildings_timestampId}]
requirements = []
nodes = 4
interpreter='python3.12'
computeId = el.compute.createCompute(layers=layers, interpreter=interpreter, nodes=nodes, requirements=requirements, token = token)['id']
res = el.compute.execute(computeId=computeId, f=f, token=token)

sh = pd.concat(res)
sh.plot()
sh.shape

el.compute.terminateAll(token=token)

sh.to_file('/home/daniel/Downloads/damaged buildings')

el.path.vector.timestamp.file.a