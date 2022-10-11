# usage

## getActiveUsers

    ellipsis.path.usage.getActiveUsers()

Get users that used the given path.

**Mandatory arguments**

- pathId (uuid)
- hashtag (string), the hashtag to add
- token (string)

**Optional arguments**

- pageStart (uuid)
- listAll (boolean)

## getUsage

    ellipsis.path.usage.getUsage()

Get usage history of a specific user on a path.

**Mandatory arguments**

- pathId (uuid)
- userId (uuid)
- token (string)

## getAggregatedUsage

    ellipsis.path.usage.getAggregatedUsage()

Get aggregated usage history.

**Mandatory arguments**

- pathId (uuid)
- token (string)

**Optional arguments**

- loggedIn (boolean) default True

