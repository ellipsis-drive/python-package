# invites

## send

    ellipsis.path.invite.send()

Invite someone to a path. They will need to accept before they are actually added.

**Mandatory arguments**

- pathId (uuid), the id of the block or folder to share
- access (object), should be an access object, with accessTier, processingUnits and optional geofence.
- token (string), your token

**Semi mandatory arguments (at least one required)**

- userId (string), user id to send the invite to (if no email is given)
- email (string), email to send the invite to (if no userid is given)

## revoke

    ellipsis.path.invite.revoke()

Revoke a sent invitation.

**Mandatory arguments**

- pathId (uuid), the id of the map or folder
- inviteId (uuid), the id of the invite you wish to revoke
- token (string), your token

## accept

    ellipsis.path.invite.accept()

Accept an invite to a map or folder.

**Mandatory arguments**

- pathId (uuid), the id of the map or folder
- inviteId (uuid), the id of the invite you wish to accept
- token (string), your token

## decline

    ellipsis.path.invite.decline()

Decline an invite to a map or folder.

**Mandatory arguments**

- pathId (uuid), the id of the map or folder to share
- inviteId (uuid), the id of the invite you wish to decline
- token (string), your token

## getYourInvites

    ellipsis.path.invite.getYourInvites()

Retrieve pending invites.

**Mandatory arguments**

- token (string), your token

## getPathInvites

    ellipsis.path.invite.getPathInvites()

Retrieve pending invites to a map.

**Mandatory arguments**

- pathId (uuid), the id of the block or folder
- token (string), your token
