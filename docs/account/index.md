# Account

## logIn

    ellipsis.account.logIn()

Login to your account.

### Mandatory parameters

- username (string), your username
- password (string), your password

### Optional parameters

- validFor (int), number of seconds the token should be valid for.

Returns a token.

## listRootMaps

    ellipsis.account.listRootMaps()

List the items in a root location.

### Mandatory parameters

- rootName (string), one of "myDrive", "sharedWithMe", "favorites" or "trash"

### Optional parameters

- pageStart (uuid), from where to start the listing
- listAll (boolean), wether to get all results or only the first page

Returns a JSON object containing the maps in the specified root.

## listRootFolders

    ellipsis.account.listRootFolders()

List the items in a root location.

### Mandatory parameters

- rootName (string), one of "myDrive", "sharedWithMe", "favorites" or "trash"
- token (string), your token

### Optional parameters

- pageStart (uuid), from where to start the listing
- listAll (boolean), wether to get all results or only the first page

Returns a JSON object containing the folders in the specified root.
