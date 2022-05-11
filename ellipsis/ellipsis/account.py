# login

def logIn(username, password, validFor = None):

        json = {'username': username, 'password': password}

        if validFor is not None:
            json["validFor"] = validFor

        r =s.post(url + '/account/login/', json=json)
        if r.status_code != 200:
            raise ValueError(r.text)
            
        token = r.json()
        token = token['token']
        token = 'Bearer ' + token
        return(token)

# list root?