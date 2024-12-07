# Vector

```{toctree}
---
maxdepth: 3
---
timestamp/index
style/index
featureProperty/index
```


## add

    ellipsis.path.vector.add()

Adds a vector.

**Mandatory arguments**

- name (string) name for the folder
- token (string), your token

**Optional arguments**

- parentId (uuid) id of folder to place the new folder in
- publicAccess (dict) dictionary describing the public access of the folder
- metadata (dict) dictionary describing the metadata of the folder


## editFilter

    ellipsis.path.vector.editFilter()

Adds indices to a vector so that you can filter on properties

**Mandatory arguments**

- pathId (uuid) id of the vector to edit
- propertyFilter (list) a list of dictionaries describing the filter
- token (string), your token

## editRendering()
Updates the rendering settings in the viewer

**Mandatory arguments**

- pathId (uuid) id of the vector to edit
- maxZoom (int) The max zoomlevel of the layer
- token (string), your token
