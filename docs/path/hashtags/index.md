# hashtags

## add

    ellipsis.path.hashtags.add()

Adds a hashtag to a map.

**Mandatory arguments**

- pathId (uuid), the id of the map to add the hashtag to
- hashtag (string), the hashtag to add
- token (string), your token

## delete

    ellipsis.path.hashtags.delete()

Removes a hashtag to a map.

**Mandatory arguments**

- pathId (uuid), the id of the map from which to remove the hashtag
- hashtag (string), the hashtag to remove
- token (string), your token

## search

    ellipsis.path.hashtags.search()

Retrieves all existing hashtags that contain a given string.

**Mandatory arguments**

- hashtag (string), the string to search for
