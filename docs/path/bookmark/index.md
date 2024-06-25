# Bookmarks

## add

    ellipsis.path.bookmark.add()

Create a bookmark

**Mandatory arguments**

- name (string) a name for the bookmark
- token (string) a valid token
- bookmark (dict) a dictionary with properties layers and dems.
Layers should be a list of dictionaries containing the properties type, id and selected. Type should be one of 'ellipsis', 'base' or 'external'. Selected should be boolean. Id should be the id of the layer or external layer, in case of type base you can choose between id=1 (open street map) and id=2 (google satellite map).
dems should be a list of dictionaries containing the properties id and selected. Selected should be boolean. Id should be the id of the raster layer.

**Optional arguments**

- parentId (uuid) the id of the folder to create the bookmark in
- publicAccess (dict) dictionary describing the public access of the bookmark
- metadata (dict) dictionary describing the metadata of the bookmark

## get

    ellipsis.path.bookmark.get()

Retrieves bookmark details

**Mandatory arguments**

- pathId (uuid) the id of the bookmark

**Optional arguments**
- token (string) a valid token



## edit

    ellipsis.path.bookmark.edit()

Edit an existing bookmark


**Mandatory arguments**
- pathId (uuid) the id of the bookmark
- token (string) a valid token

**Optional arguments**
- layers (list) a list of dictionaries containing the properties type, id and selected. Type should be one of 'ellipsis', 'base' or 'external'. Selected should be boolean. Id should be the id of the layer or external layer, in case of type base you can choose between id=1 (open street map) and id=2 (google satellite map).
- dems (list) a list of dictionaries containing the properties id and selected. Selected should be boolean. Id should be the id of the raster layer.



