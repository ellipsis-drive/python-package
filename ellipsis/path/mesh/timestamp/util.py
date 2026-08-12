import numpy as np
import imageio
import tifffile
import io
import math

def addTransparent(im, dtype, as_jpg, w = 256):
    if dtype == 'uint8':
        trans = np.full((1,w,w),255)
        trans[:, np.any(im > 250, axis = 0)]=0
    elif dtype == 'float32':
        trans =np.full((1,w,w),1)
        trans[:, np.isnan(im[0,:,:]) ] = 0
    elif dtype == 'uint16':
        trans = np.full((1,w,w),2**16-1)
        trans[:,im[0,:,:] == 2**16-1 ] = 0
    elif dtype == 'int16':
        trans = np.full((1,w,w),2**15-1)
        trans[:,im[0,:,:] == 2**15-1 ] = 0
        
    im[:,trans[0,:,:]==0] = 0
    im = np.concatenate([im, trans], axis = 0)
    return(im)
    
def constructImage(N, stream, as_jpg, num_bands, dtype):
        FILES_IN_ARCHIVE = [0] + list( np.cumsum(np.array([4**x for x in np.arange(10) ])))

        old_im = np.zeros((num_bands-1,256*2**N,256*2**N))

        counter = FILES_IN_ARCHIVE[N]
        for i in np.arange(2**N):
            for j in np.arange(2**N):
                numTile = FILES_IN_ARCHIVE[N] + i * 2**(N) + j
                file_start = int.from_bytes(stream[numTile*8:(numTile+1)*8], 'big')
                file_end = int.from_bytes(stream[(numTile+1)*8:(numTile+2)*8], 'big')
                if file_start != file_end:
                    fileStream = stream[file_start:file_end]
                    if as_jpg:
                       im_sub = imageio.imread(fileStream)
                       im_sub = np.transpose(im_sub, [2,0,1])
                    else:
                       im_sub = tifffile.imread(io.BytesIO(fileStream))
                    old_im[:, j*256 : (j+1)*256 , i*256: (i+1)*256] = im_sub
                    
                counter = counter + 1
        old_im = addTransparent(im = old_im, dtype = dtype, as_jpg = as_jpg, w = 256*2**N)            
        return(old_im)
    
    
cutOffDegrees = [60, 75.5, 83.1]

def degreeToTile(y):
    z = 0
    r  = 2**z / (2* math.pi) * ( math.pi - math.log( math.tan(math.pi / 4 + y/360 * math.pi  ) ) )
    return(r)


cutOfTiles = [degreeToTile(d) for d in cutOffDegrees]

def cutOffs(zoom):
    starts = []
    ends= []    
    for k in [1,2,3]:
        cutOffStart = round(cutOfTiles[k-1] * 2**zoom - (cutOfTiles[k-1] * 2**zoom) % 2**k)
        cutOffEnd = 2**zoom - cutOffStart-1
        starts = starts + [cutOffStart]
        ends = ends + [cutOffEnd]
    ends = ends + [2**zoom-1]
    starts = starts + [0]

    return( {'zoom': zoom, 'total': 2**zoom, 'start': np.array(starts), 'end': np.array(ends) } )



cutOfTilesPerZoom = [ cutOffs(i)  for i in np.arange(40)]

