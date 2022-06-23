# members

## get

    ellipsis.path.member.get()

Retrieves the users a path has been shared with.

**Mandatory arguments**

- pathId (uuid), the id of the block or folder

**Optional arguments**
- memberType (array of strings),  can contain "interited" and "direct"  
- token (uuid), your token

## delete

    ellipsis.path.member.delete()

Removes a member from a path

**Mandatory arguments**

- pathId (uuid), the id of the block or folder
- userId (uuid),  the id of the user to delete  
- token (uuid), your token

## edit

    ellipsis.path.member.edit()

Edits permissions of a user on a given path.

**Mandatory arguments**

- pathId (uuid), the id of the block or folder
- userId (uuid), the id of the user whose access to be edited
- access (object), Object with optional properties accessLevel, processingUnits, canShare, geoFence, with the changes in access. geoFence should be an object with tiles and maxZoom. Tiles should be an array of objects with tileX, tileY and zoom.
- token (uuid), your token