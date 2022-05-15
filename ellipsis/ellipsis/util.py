import requests
import warnings
import geopandas as gpd
from shapely.geometry import Polygon
from rasterio.features import rasterize
from geopy.distance import geodesic

URL = 'https://api.ellipsis-drive.com/v2'

session = requests.Session()
warnings.filterwarnings("ignore")

def dictAdd(dictionary, key, value):
    ''' Adds key with value to the dictionary if the value is not None '''
    if value is not None:
        dictionary[key] = value
    print(dictionary)

def plotPolys(polys, xMin = None,xMax = None,yMin=None,yMax= None, alpha = None, image = None, colors = {0:(0,0,255)} , column= None):
    polys.crs = {'init': 'epsg:4326'}

    if str(type(xMin)) == str(type(None)):
        polys_union = polys.unary_union
        bbox = gpd.GeoDataFrame({'geometry':[polys_union]})
        xMin = bbox.bounds['minx'].values[0]
        yMin = bbox.bounds['miny'].values[0]
        xMax = bbox.bounds['maxx'].values[0]
        yMax = bbox.bounds['maxy'].values[0]
        
    bbox = gpd.GeoDataFrame( {'geometry': [Polygon([(xMin,yMin), (xMax, yMin), (xMax, yMax), (xMin, yMax)])]} )
    bbox.crs = {'init': 'epsg:4326'}
    bbox = bbox.to_crs({'init': 'epsg:3785'})
    polys = polys.to_crs({'init': 'epsg:3785'})

    if str(type(image)) == "<class 'NoneType'>":
        if (xMax-xMin) > (yMax - yMin):
            image = np.zeros((1024,1024* int((xMax-xMin)/(yMax-yMin)),4))
        else:
            image = np.zeros((1024* int((yMax-yMin)/(xMax-xMin)),1024,4))
            
    image = image/255
    if column == None:
        column = 'extra'
        polys[column] = 0
    
    transform = rasterio.transform.from_bounds(bbox.bounds['minx'], bbox.bounds['miny'], bbox.bounds['maxx'], bbox.bounds['maxy'], image.shape[1], image.shape[0])
    rasters = np.zeros(image.shape)
    for key in colors.keys():
        sub_polys = polys.loc[polys[column] == key]
        if sub_polys.shape[0] >0:
            raster = rasterize( shapes = [ (sub_polys['geometry'].values[m], 1) for m in np.arange(sub_polys.shape[0]) ] , fill = 0, transform = transform, out_shape = (image.shape[0], image.shape[1]), all_touched = True )
            raster = np.stack([raster * colors[key][0]/255, raster*colors[key][1]/255,raster*colors[key][2]/255, raster ], axis = 2)
            rasters = np.add(rasters, raster)
     
    rasters = np.clip(rasters, 0,1)

    image_out = rasters
    image_out[image_out[:,:,3] == 0, :] = image [image_out[:,:,3] == 0, :]
    if alpha != None:
        image_out = image * (1 - alpha) + image_out*alpha 

    image_out = image_out *255
    image_out = image_out.astype('uint8')
    return(image_out)


def chunks(l, n = 3000):
    result = list()
    for i in range(0, len(l), n):
        result.append(l[i:i+n])
    return(result)
    

 
def cover(bounds, w):
    if str(type(bounds)) == "<class 'shapely.geometry.polygon.Polygon'>" :
        bounds = [bounds]
    elif str(type(bounds)) =="<class 'shapely.geometry.multipolygon.MultiPolygon'>":
        bounds = bounds
    else:
        raise ValueError('bounds must be a shapely polygon or multipolygon')

    bound = bounds[0]
    coords_total = pd.DataFrame()
    for bound in bounds:
         x1, y1, x2, y2  = bound.bounds

         step_y =  w/geodesic((y1,x1), (y1 - 1,x1)).meters
         parts_y = math.floor((y2 - y1)/ step_y + 1)

         y1_vec = y1 + np.arange(0, parts_y )*step_y
         y2_vec = y1 + np.arange(1, parts_y +1 )*step_y
             
         steps_x = [   w/geodesic((y,x1), (y,x1+1)).meters for y in y1_vec  ]

         parts_x = [math.floor( (x2-x1) /step +1 ) for step in steps_x ]      
             
     
         coords = pd.DataFrame()
         for n in np.arange(len(parts_x)):
             x1_sq = [ x1 + j*steps_x[n] for j in np.arange(0,parts_x[n]) ]
             x2_sq = [ x1 + j*steps_x[n] for j in np.arange(1, parts_x[n]+1) ]
             coords_temp = {'x1': x1_sq, 'x2': x2_sq, 'y1': y1_vec[n], 'y2':y2_vec[n]}
             coords = coords.append(pd.DataFrame(coords_temp))
         coords_total = coords_total.append(coords)

    cover = [Polygon([ (coords_total['x1'].iloc[j] , coords_total['y1'].iloc[j]) , (coords_total['x2'].iloc[j] , coords_total['y1'].iloc[j]), (coords_total['x2'].iloc[j] , coords_total['y2'].iloc[j]), (coords_total['x1'].iloc[j] , coords_total['y2'].iloc[j]) ]) for j in np.arange(coords_total.shape[0])]
     


    coords = gpd.GeoDataFrame({'geometry': cover, 'x1':coords_total['x1'], 'x2':coords_total['x2'], 'y1':coords_total['y1'], 'y2':coords_total['y2'] })

    coords.crs = {'init': 'epsg:4326'}

    return(coords)
    

    
def loadingBar(count,total):
    if total == 0:
        return
    else:
        percent = float(count)/float(total)*100
        sys.stdout.write("\r" + str(int(count)).rjust(3,'0')+"/"+str(int(total)).rjust(3,'0') + ' [' + '='*int(percent) + ' '*(100-int(percent)) + ']')
