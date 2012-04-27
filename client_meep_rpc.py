import xmlrpclib
import meeplib
import rpc_settings

proxy = None 
#Setup proxy
def connect():
    global proxy
    proxy = xmlrpclib.ServerProxy("http://localhost:8001/")