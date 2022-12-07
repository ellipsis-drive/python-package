# View

## listViews

    ellipsis.view.listViews()

List your saved views

**Mandatory arguments**

- token (string) a valid token

## get

    ellipsis.view.get()

Retrieve a specific view

**Mandatory arguments**

- viewId (uuid) the id of the view

**Optional arguments**
- token (string) a valid token

## add

    ellipsis.view.add()

Add a view

**Mandatory arguments**

- name (string) a name for the view you create
- persistent (boolean) whether to include the view when you list your views.
- pathId (uuid) the id of the path to use as anchor location
- layers (list) a list of dictionaries containing the properties type 'ellipsis' or 'base' and selected as boolean. In case of type 'ellipsis' a property id should be included. This id should be the (path) id of the ellipsis layer you wish to inlcude to the view.
- dems (list) a list of dictionaries containing the properties id which should be a (path) id of a layer and selected as boolean
- token (string) a valid token


## edit

    ellipsis.view.edit()

Edit an existing view

**Mandatory arguments**
- viewId (uuid) the id of the view
- token (string) a valid token

**Optional arguments**

- name (string) a name for the view you create
- layers (list) a list of dictionaries containing the properties type 'ellipsis' or 'base' and selected as boolean. In case of type 'ellipsis' a property id should be included. This id should be the (path) id of the ellipsis layer you wish to inlcude to the view.
- dems (list) a list of dictionaries containing the properties id which should be a (path) id of a layer and selected as boolean


## delete

    ellipsis.view.delete()

Delete an existing view

**Mandatory arguments**

- viewId (uuid) the id of the view
- token (string) a valid token


