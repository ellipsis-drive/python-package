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
- isFolder (boolean), wether to list folders or maps

### Optional parameters

- pageStart (uuid), from where to start the listing

Returns a JSON object containing thefolderes or maps in the specified root.
