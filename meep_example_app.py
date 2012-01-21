import meeplib
import traceback
import cgi

def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')

    # create a single message
    meeplib.Message('my title', 'This is my message!', u, "!")

    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'test'

        return ["""you are logged in as user: %s.
                <p>
                <form action = '/m/add' method = 'POST'>
                <input type = 'hidden' name = 'pID' value = '!'>
                <input type = 'submit' value = 'Add Message'>
                </form>
                <p>
                <form  action = '/login'>
                <input type = 'submit' value = 'Login'>
                </form>
                <p>
                <form action = 'logout'>
                <input type = 'submit' value = 'Logout'>
                </form>
                <p>
                <form action = '/m/list'>
                <input type = 'submit' value = 'Show Messages'>
                </form>
                """ % (username,)]

    def login(self, environ, start_response):
        # hard code the username for now; this should come from Web input!
        username = 'test'

        # retrieve user
        user = meeplib.get_user(username)

        # set content-type
        headers = [('Content-type', 'text/html')]
        
        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def logout(self, environ, start_response):
        # does nothing
        headers = [('Content-type', 'text/html')]

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()
        #replies = meeplib.get_all_replies()

        s = []
        for m in messages:
            if(m.pID == "!"):
                s = print_messages(m, s)
            '''for r in replies:
                if(r.id in m.replies):
                    s = print_messages(r, s)'''
            
            s.append('<hr>')

        s.append("""
                 <form action = 'add' method = 'POST'>
                 <input type = 'hidden' name = 'pID' value = '!'>
                 <input type = 'submit' value = 'Add Message'>
                 </form><p>""")
        s.append("""
                 <form action = '../../'>
                 <input type = 'submit' value = 'Index'>
                 </form>""")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]

    def add_message(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        pID = form['pID'].value
        print "PID:" + pID + "!";
        
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        s = []
        s.append("""
                <form action='add_action' method='POST'>
                Title:""")
        if(pID != '!'):
            title = "RE: " + meeplib.get_message(int(pID)).title
            s.append("""
                     <input type='text' name='title' value = %r>
                     """ % title)
        else:
            s.append("""
                     <input type='text' name='title'>
                     """)
        s.append("""
                <br>
                Message:
                <input type='text' name='message'>
                <br>
                <input type='submit'>
                <input type = 'hidden' name = 'pID' value = '%s'>
                </form>
                """ % pID)
        return s

    def add_message_action(self, environ, start_response):
        #print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        pID = form['pID'].value

        print "PID:" + pID + "!";
        
        username = 'test'
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user, pID)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)

        if(pID != '!'):
            return ["Message Added"]
        else:
            return ["Reply Added"]

    def del_message(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        print form
        
        messages = meeplib.get_all_messages()

        s = []
        found = False
        for m in messages:
            if m.id == int(form['id'].value):
                meeplib.delete_message(m)
                s.append("Post Successfully Deleted.")
                if m.pID != "!":
                    meeplib.delete_reply(m)
                found = True
            if found == True:
                break
        
        start_response("200 OK", [('Content-type', 'text/html')])
        s.append("<p><p><a href = '../../'>Return to Index</a>")
        return "".join(s)

    def reply_to_post(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        parentID = form['id'].value;

        s = []


        start_response("200 OK", [('Content-type', 'text/html')])
        s.append("<p><p><a href = '../../'>Return to Index</a>")
        return "".join(s)
        
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/delete': self.del_message
                      #'/m/reply_to_post': self.reply_to_post
                      }

        # see if the URL is in 'call_dict'; if it is, call that function.
        url = environ['PATH_INFO']
        fn = call_dict.get(url)

        if fn is None:
            start_response("404 Not Found", [('Content-type', 'text/html')])
            return ["Page not found."]

        try:
            return fn(environ, start_response)
        except:
            tb = traceback.format_exc()
            x = "<h1>Error!</h1><pre>%s</pre>" % (tb,)

            status = '500 Internal Server Error'
            start_response(status, [('Content-type', 'text/html')])
            return [x]

def print_messages(m, s):
    s.append('id: %d<br/>' % (m.id,))
    s.append('title: %s<br/>' % (m.title))
    s.append('message: %s<br/>' % (m.post))
    s.append('author: %s<br/>' % (m.author.username))
    s.append("""
             <form action="add" method="POST">
             <input type = 'hidden' name ='pID' value = %d>
             <input type = 'submit' value = 'Reply'>
             </form>""" % (m.id))
    s.append("""
             <form action = 'delete' method = 'POST'>
             <input type = 'hidden' name = 'id' value = '%d'>
             <input type = 'submit' value = 'Delete Post'>
             </form>""" % (m.id))

    if(m.replies != []):
        for r in m.replies:
            print_messages(meeplib.get_message(r), s)
            
    return s
