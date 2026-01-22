# Compute (Beta release)

## createCompute

    ellipsis.compute.createCompute()

Creates a compute environment.

**Mandatory arguments**

- layers (list), a list of dictionaries with timestampId and corresponding pathId. Should contain all Ellipsis Drive layers and timestamps you wish to be available in your environment.
- token (token), A user token to authenticate with
- Nodes (integer) the number of nodes you wish parallelize over.

**Optional arguments**

- interpreter (string), the Python interpreter to use (default 'python3.12')
- requirements (list), a list with Python package names you wish to be available in your environment.
- awaitTillStarted (boolean), a boolean indicating whether to halt till the environment is available (default True).
- largeResult (boolean), whether the functions you will run on the environment will return a memory file or a simple Python object. If false object may not exceed 2mb. (default False)
- enableGpu (boolean), whether to use the GPU to execute given functions. (default False)

## execute

    ellipsis.compute.execute()

Executes a Python function on the created environment in a parallelized fashion over all nodes

**Mandatory arguments**

- computeId (uuid), the id of the environment as returned by createCompute()
- token (token), A user token to authenticate with
- f (function), A Python function to execute. The parameters of the function will be a dictionary. The keys of this dictionary are the timestampId's as given in the layers parameter in createCompute(). In case of a vector the value of the key will be a geopandas dataframe. In case of a raster the value of the parameter will be a dictionary with raster as numpy array, extent as dictionary with xMin, xMax, yMin, yMax and a transform as rasterio transform.

**Optional arguments**
- awaitTillCompleted (boolean), a boolean indicating whether to halt till the function has executed.
- writeToLayer (dict), a dictionary with pathId and timestampId indicating to what layer and timestamp to add the result.

## terminateCompute

    ellipsis.compute.terminateCompute()

Terminates a created environment.

**Mandatory arguments**

- computeId (uuid), the id of the environment as returned by createCompute()
- token (token), A user token to authenticate with

**Optional arguments**
- awaitTillCompleted (boolean), a boolean indicating whether to halt till the environment has been terminated.


## terminateAll

    ellipsis.compute.terminateCompute()

Terminates all created environments.

**Mandatory arguments**

- token (token), A user token to authenticate with

**Optional arguments**
- awaitTillCompleted (boolean), a boolean indicating whether to halt till all environments have been terminated (default True).

## getComputeInfo

    ellipsis.compute.getComputeInfo()

Fetches status and metadata of a specific environment.

**Mandatory arguments**
- computeId (uuid), the id of the environment as returned by createCompute()
- token (token), A user token to authenticate with

## listComputes()

    ellipsis.compute.listComputes()

Lists all created environments.

**Mandatory arguments**

- token (token), A user token to authenticate with

**Optional arguments**
- listAll (boolean), whether to list all environment or only the first page (default True).
- pageStart (uuid), An id from which to start the listing.


## addLayer()

    ellipsis.compute.addLayer()

Add all resulting files from execute() to a new layer. Mind that in this case execute() needs to be run with largeResult=True.

**Mandatory arguments**
- response (list), the list as returned by execute()
- pathId (uuid), the id of the layer to add the files to.
- timestampId (uuid), the id of the timestamp to add the files to.
- token (token), A user token to authenticate with


