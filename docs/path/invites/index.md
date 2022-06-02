# invites

## send

    ellipsis.path.invite.send()

### Mandatory arguments

- pathId (uuid), the id of the block or folder to share
- access (object), should be an object with properties canShare, geoFence, monthlyFee, accessLevel and processingUnits defining the access given to the user. geoFence should be an object with tiles and maxZoom. Tiles should be an array of objects with tileX, tileY and zoom.
- token (string), your token

### Semi mandatory arguments (at least one required)

- userId (string), user id to send the invite to (if no email is given)
- email (string), email to send the invite to (if no userid is given)

## revoke

    ellipsis.path.invite.revoke()

### Mandatory arguments

- pathId (uuid), the id of the map or folder
- inviteId (uuid), the id of the invite you wish to revoke
- token (string), your token

## accept

    ellipsis.path.invite.accept()

### Mandatory arguments

- pathId (uuid), the id of the map or folder
- inviteId (uuid), the id of the invite you wish to accept
- token (string), your token

## decline

    ellipsis.path.invite.decline()

### Mandatory arguments

- pathId (uuid), the id of the map or folder to share
- inviteId (uuid), the id of the invite you wish to decline
- token (string), your token

## getYourInvites

    ellipsis.path.invite.getYourInvites()

### Mandatory arguments

- token (string), your token

## getPathInvites

    ellipsis.path.invite.getPathInvites()

### Mandatory arguments

- pathId (uuid), the id of the block or folder
- token (string), your token
