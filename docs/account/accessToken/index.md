# Personal Access Tokens

## create

    ellipsis.account.accessToken.create()

Create an access token.

**Mandatory arguments**

- description (string), a description for the token to be created
- accessList (list), a list of dictionaries. Each dictionary must contain a pathId and an accessLevel.
- token (string)

**Optional arguments**

- validFor (int), number of seconds that the token should remain valid. If None token will remain valid forever.


## revoke

    ellipsis.account.accessToken.revoke()

Revoke a personal access token.

**Mandatory arguments**

- accessTokenId (uuid), the id of the token to invalidate
- token (string)

## get

    ellipsis.account.accessToken.get()

Retrieve all current tokens.

**Mandatory arguments**

- token (string)

**Optional arguments**

- pageStart (uuid)
- listAll (boolean), whether to recursively fetch all tokens, or only one page
