import os




def recurse(folder, N, fileType= None):
    content = os.listdir(folder)
    for c in content:
        if os.path.isdir(folder + '/' + c):
            N = recurse(folder + '/' + c, N, fileType)
        else:
            try:
                if fileType == None or fileType in c:
                    num_lines = sum(1 for _ in open( folder + '/' + c))
                else:
                    num_lines = 0
            except:
                num_lines = 0
            N = N + num_lines
    return N

total = 0
api_folder = '/home/daniel/Ellipsis/api'
N = recurse(api_folder,0)
print('api code', N)
total = total + N

compute_folder = '/home/daniel/Ellipsis/compute'
N = recurse(compute_folder,0)
print('compute code api', N)
total = total+N



mapEngine_folder = '/home/daniel/Ellipsis/compute-master'
N = recurse(mapEngine_folder,0)
inDocker_folder = '/home/daniel/Ellipsis/inDocker'
M = recurse(inDocker_folder,0)

print('map Engine', N+M)
total = total+N+M


ui_folder = '/home/daniel/Ellipsis/ellipsis-app/src'
N = recurse(ui_folder,0)
print('ui code', N)
total = total+N


backgroup_process_folder = '/home/daniel/Ellipsis/background-processes'
N = recurse(backgroup_process_folder,0, '.js')
print('background code', N)
total = total+N


plugins = [  '/home/daniel/Ellipsis/folders-package/src', '/home/daniel/Ellipsis/folium/foliumEllipsis', '/home/daniel/Ellipsis/leaflet-package/src/lib', '/home/daniel/Ellipsis/mapboxgljs-package/src/lib', '/home/daniel/Ellipsis/python-package/ellipsis', '/home/daniel/Ellipsis/qgis-plugin/connect', '/home/daniel/Ellipsis/react-leaflet-package/src/lib', '/home/daniel/Ellipsis/R-package/R' ]
T=0
for p in plugins:
    N = recurse(p, 0)
    T = T+N
print('lines code of some plugins (not all plugins are included)', T)

total = total +T

print('total lines', total)




