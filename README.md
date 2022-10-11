# Ellipsis Drive Python Package

This package is meant to help you interact with the Ellipsis API.

You can install this package using

`pip install ellipsis`

For documentation see https://ellipsis-package.readthedocs.io

This package is meant to ease the use of the Ellipsis Drive API in your Python projects.

# Examples

Below are some code examples.

    import ellipsis as el

    # log in
    token = el.account.logIn("username", "password")

    # retrieve all maps in "My Drive"
    maps = el.account.listRoot("myDrive", pathType='layer',
    token=token)

Another example

    import ellipsis as el

    folderId = '46e1e919-8b73-42a3-a575-25c6d45fd93b'

    token = el.account.logIn("username", "password")

    info = el.path.get(folderId, token)
    layers = el.path.listPath(folderId, pathType='layer', token = token, listAll = True)
    folders = el.path.listPath(folderId, pathType='folder', token = token, listAll = True)
