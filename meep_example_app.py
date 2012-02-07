import meeplib
import traceback
import cgi
import pickle

def initialize():
    # create a default user
    #u = meeplib.User('test', 'foo')

    # create a single message
    #meeplib.Message('my title', 'This is my message!', u, "!")

    try:
        fp = open('users.pickle')
        try:
            obj = pickle.load(fp)
            while True:
                #print obj
                (a, b) = obj
                
                u = meeplib.User(a, b);
                try:
                    obj = pickle.load(fp)
                except EOFError:
                    break
        except EOFError:
            pass
    except IOError:
        fp = open('users.pickle', "w")
        fp.close()
    
    
    try:
        fp = open('messages.pickle')
        try:
            obj = pickle.load(fp)
            while True:
                (a, b, c, d, e) = obj
                #print obj
                m = meeplib.Message(a,b,meeplib.get_user(c), d)
                m.id = e
                #print m.post + " is " + str(m.id)
                #obj = pickle.load(fp)
                #m.replies = obj
                #print obj
                try:
                    obj = pickle.load(fp)
                except EOFError:
                    break
        except EOFError:
            pass
    except IOError:
        p = open('messages.pickle', "w")
        fp.close()
    

    
    

    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'test'
        
        return ["""<h1>Welcome!</h1><h2>Please Login or create an account.</h2>

        <form action='login' method='POST'>
        Username: <input type='text' name='username'><br>
        Password:<input type='password' name='password'><br>
        <input type='submit' value='Login'></form>

        <p>Don't have an account? Create a user <a href='/create_user'>here</a>"""]

    def main_page(self, environ, start_response):
        try:
            meeplib.get_curr_user()
        except NameError:
            meeplib.delete_curr_user()
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        username = meeplib.get_curr_user()

        #return ["""%s logged in!<p><a href='/m/add'>Add a message</a><p><a href='/create_user'>Create User</a><p><a href='/logout'>Log out</a><p><a href='/m/messages'>Show messages</a><p><a href='/m/delete'>Delete a message</a>""" % (username,)]

        return ["""you are logged in as user: %s.
                <p>
                <form action = '/m/add' method = 'POST'>
                <input type = 'hidden' name = 'pID' value = '!'>
                <input type = 'submit' value = 'Add Message'>
                </form>
                <p>
                <form  action = '/create_user'>
                <input type = 'submit' value = 'Create User'>
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

    

    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("302 Found", headers)
        return """<form action='add_new_user' method='POST'>
        Username: <input type='text' name='username'><br>
        Password:<input type='password' name='password'><br>
        <input type='submit' value='Create User'></form>"""

    def add_new_user(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        returnStatement = "user added"
        try:
            username = form['username'].value
        except KeyError:
            username = None
        try:
            password = form['password'].value
        except KeyError:
            password = None

        #print username
        #print password
        # Test whether variable is defined to be None
        if username is None:
            returnStatement = "username was not set. User could not be created"
        if password is None:
            returnStatement = "password was not set. User could not be created"
        else:
            new_user = meeplib.User(username, password)
            SaveUsers()
        

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/'))
        start_response("302 Found", headers)

        return [returnStatement]

    def login(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        returnStatement = "logged in"
        try:
            username = form['username'].value
        except KeyError:
            username = None
        try:
            password = form['password'].value
        except KeyError:
            password = None

        # Test whether variable is defined to be None
        if username is not None:
             if password is not None:
                 if meeplib.check_user(username, password) is False:
                     k = 'Location'
                     v = '/'
                     returnStatement = """<p>Invalid user.  Please try again.</p>"""
           
                 else:
                     new_user = meeplib.User(username, password)
                     meeplib.set_curr_user(username)
                     k = 'Location'
                     v = '/main_page'
             else:      
                 returnStatement = """<p>password was not set. User could not be created</p>"""
        else:
            returnStatement = """<p>username was not set. User could not be created</p>"""

        #print """isValidafter: %s """ %(meeplib.check_user(username, password),)

        # set content-type
        headers = [('Content-type', 'text/html')]
       
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

        s = []
        for m in messages:
            if(m.pID == "!"):
                s = print_messages(m, s, 0)
        s.append('<hr>')
            
        s.append("""
                 <form action = 'add' method = 'POST'>
                 <input type = 'hidden' name = 'pID' value = '!'>
                 <input type = 'submit' value = 'Add Message'>
                 </form><p>""")
        s.append("""
                 <form action = '../main_page'>
                 <input type = 'submit' value = 'Index'>
                 </form>""")

        '''for m in meeplib.get_all_messages():
            print "Post: " + m.post
            print "Author: " + m.author.username
            print "ID: " + str(m.id)
            print ""'''

        
        if not messages:
            s.append("There are no messages to display.<p>")
        #s.append("<a href='../../main_page'>Go Back to Main Page</a>")
       
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]

    def add_message(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        pID = form['pID'].value
        #print "PID:" + pID + "!";
        
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
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        pID = form['pID'].value

        #print "PID:" + pID + "!";
        
        username = meeplib.get_curr_user()
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user, pID)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        
        SaveMessages()

        

        if(pID != '!'):
            return ["Message Added"]
        else:
            return ["Reply Added"]

    def del_message(self, environ, start_response):
        #print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        #print form
        
        messages = meeplib.get_all_messages()

        s = []
        found = False
        for m in messages:
            if m.id == int(form['id'].value):
                if meeplib.get_curr_user() != m.author.username:
                    #print "i'm here"
                    s.append("Cannot delete message that does not belong to you!")
                    break
                if m.pID != "!":
                    meeplib.delete_reply(m)
                meeplib.delete_message(m)
                s.append("Post Successfully Deleted.")
                #meeplib.ResetMessageIds()
                found = True
            if found == True:
                break
        
        start_response("200 OK", [('Content-type', 'text/html')])
        s.append("<p><p><a href = '/m/list'>Return to Messages</a>")

        SaveMessages()

        return "".join(s)

    '''def reply_to_post(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        parentID = form['id'].value;

        s = []


        start_response("200 OK", [('Content-type', 'text/html')])
        s.append("<p><p><a href = '../../'>Return to Index</a>")
        return "".join(s)
        return ["message added"]'''
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/main_page': self.main_page,
                      '/create_user': self.create_user,
                      '/add_new_user':self.add_new_user,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/delete': self.del_message
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

def print_messages(m, s, level):
    if(level != 0):
        s.append('<blockquote>')
    s.append('id: %d<br>' % (m.id,))
    s.append('title: %s<br>' % (m.title))
    s.append('message: %s<br>' % (m.post))
    s.append('author: %s' % (m.author.username))
    s.append("""
             <form action = 'add' method = 'POST'  style="margin:0;">
             <input type = 'submit' value = 'Reply' />
             <input type = 'hidden' name = 'pID' value = '%d' />
             </form>""" % (m.id))
    s.append("""
             <form action = 'delete' method = 'POST'  style="margin:0;">
             <input type = 'submit' value = 'Delete Post' />
             <input type = 'hidden' name = 'id' value = '%d' />
             </form>
             <hr>""" % (m.id))

    if(m.replies != []):
        print m.replies
        for r in m.replies:
            print_messages(meeplib.get_message(r), s, level + 1)
            s.append('</blockquote>')
            
    return s

def SaveMessages():
    
        #Save Messages
        #
        filename = 'messages.pickle'
        fp = open(filename, 'w')
        m = meeplib.get_all_messages()
        for d in m:
            f = [d.title, d.post, d.author.username, d.pID, d.id]
            pickle.dump(f, fp)
            #f = d.replies
            #pickle.dump(f, fp)
        fp.close()
        return


def SaveUsers():
    #
    #Save Users
    #
    filename = 'users.pickle'
    fp = open(filename, 'w')
    u = meeplib.get_all_users()
    for d in u:
        f = [d.username, d.password]
        #print f
        pickle.dump(f, fp)
    fp.close()
    return
