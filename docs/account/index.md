# Account


```{toctree}
---
maxdepth: 2
---
accessToken/index
```

## logIn

    ellipsis.account.logIn()

Login to your account.

**Mandatory arguments**

- username (string), your username
- password (string), your password

**Optional arguments**

- validFor (integer), number of seconds the token should be valid for.

Returns a token.

## getInfo

    ellipsis.account.getInfo()

Fet information of your account.

**Mandatory arguments**

- token (string), your token

Returns a dictionary with additional information.

## listRoot

    ellipsis.account.listRoot()

List the items in a root location.

**Mandatory arguments**

- rootName (string), one of "myDrive", "sharedWithMe", "favorites" or "trash"
- token (string) your access token

**Optional arguments**
- pathTypes (list) list containing 'file', 'folder', 'raster' or 'vector'
- pageStart (uuid), from where to start the listing
- listAll (boolean), wether to get all results or only the first page

Returns a JSON object containing the maps in the specified root.


