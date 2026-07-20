from ellipsis import apiManager
from ellipsis import sanitize
from ellipsis.apiManager import appUrl
from ellipsis.util.root import recurse
import requests
import http.server
import socketserver
import webbrowser
from urllib.parse import urlparse, parse_qs
import uuid

def logIn(username, password, validFor = None):

        username = sanitize.validString('username', username, True)
        password = sanitize.validString('password', password, True)
        validFor = sanitize.validInt('validFor', validFor, False)

        json = {'username': username, 'password': password, 'validFor': validFor}

        r = apiManager.call(requests.post,'/account/login', body=json, token=None, crash=False)
        if r.status_code == 400:
            x = r.json()
            if x['message'] == "No password configured.":
                raise ValueError("You cannot login with your Google credentials in the Python module. You need to configure an Ellipsis Drive specific password. You can do this on https://app.ellipsis-drive.com/account-settings/security")
        if r.status_code != 200:
            raise ValueError(r.text)

        r = r.json()
        token = r['token']

        return(token)

def browserLogin():
    PORT = 8765

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        token_result = None  # class variable

        def do_GET(self):
            parsed = urlparse(self.path)

            if parsed.path == "/callback":
                params = parse_qs(parsed.query)
                self.__class__.token_result = params.get("token", [None])[0]

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Login successful. You can close this tab.</h1>")
            else:
                self.send_response(404)
                self.end_headers()

        # suppress logging to console
        def log_message(self, format, *args):
            return

    with socketserver.TCPServer(("127.0.0.1", PORT), CallbackHandler) as httpd:
        authenticateState = str(uuid.uuid1())

        print("Opening browser, please login...")
        webbrowser.open(f"{appUrl}/login?application=true")

        while CallbackHandler.token_result is None:
            httpd.handle_request()  # waits for next GET

    return CallbackHandler.token_result



def getInfo(token):
    token = sanitize.validString('token', token, True)

    r = apiManager.get( '/account', body={}, token=token)


    return r

def listRoot(rootName, token, pathTypes= None, pageStart = None, listAll = True):
    token = sanitize.validString('token', token, True)
    rootName = sanitize.validString('rootName', rootName, True)
    pageStart = sanitize.validUuid('pageStart', pageStart, False)
    listAll = sanitize.validBool('listAll', listAll, True)        
    pathTypes = sanitize.validObject('pathTypes', pathTypes, False)
    if type(pathTypes) == type(None):
        pathTypes = ['folder', 'raster', 'vector', 'file']
        

    url = "/account/root/" + rootName
    body = {"type": pathTypes, "pageStart": pageStart}


    def f(body):
        r = apiManager.get(url, body, token)
        return r

    r = recurse(f, body, listAll)
        
    return r




