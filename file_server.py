import meeplib
import traceback
import cgi

mimeTable = {"jpg" : "image/jpeg",
             "png" : "image/png",
             "ogg" : "audio/ogg"}

class file_server(object):
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, environ, start_response):
        try:
            fp = open('files/' + self.filename)
        except IOError:
            start_response("404 not found", [('Content-type', 'text/html'),])
            return 'file not found'

        data = fp.read()
        start_response("200 OK", [('Content-type', mimeTable.get(self.filename.split('.')[-1]))])
        #data = "<img src='" + self.filename + "' alt='picture'/>"
        #print self.filename

        return data