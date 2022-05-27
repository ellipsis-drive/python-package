import ellipsis as el



# el.path.raster.timestamp.order.download

g_token = ""

def test_logIn():
    global g_token
    g_token = el.account.logIn("demo_user", "demo_user")

def test_path_searchRaster():
    r = el.path.searchRaster(token=g_token);

def test_path_searchVector():
    r = el.path.searchVector(token=g_token);

def test_path_searchFolder():
    r = el.path.searchFolder(token=g_token);
    


    
