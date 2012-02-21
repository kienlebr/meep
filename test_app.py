import unittest
import meep_example_app
import meeplib

class TestApp(unittest.TestCase):
    def setUp(self):
        meep_example_app.initialize()
        app = meep_example_app.MeepExampleApp()
        self.app = app
        meeplib._reset()

    def test_index(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        #print data
        #assert 'Username:' in data
        #assert 'Password:' in data
        #assert 'Create a user' in data

    def test_create_user(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/create_user'

        def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        #print data
        assert 'Username:' in data
        assert 'Password:' in data

    def test_list_messages(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'

        u = meeplib.User('user', 'name')
        m = meeplib.Message('init title', 'init message', u ,'!')

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        index = 0
        for m in data:
            if "Title: init title" in m:
                index += 1
            if 'Message: init message' in m:
                index += 1
            if 'Author: user' in m:
                index += 1
            if 'ID: 0' in m:
                index += 1

            print index
        assert index is 4

    def test_main_page(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/main_page'

        u = meeplib.User('user', 'name')
        meeplib.set_curr_user(u.username)
        m = meeplib.Message('init title', 'init message', u ,'!')

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        index = 0
        for m in data:
            if "Add Message" in m:
                index += 1
            if 'Create User' in m:
                index += 1
            if 'Logout' in m:
                index += 1
            if 'Show Messages' in m:
                index += 1

            #print m
        assert index is 4
        

    def test_add_reply(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'
        u = meeplib.User('foo', 'bar')
        m = meeplib.Message('the title', 'the content', u ,'!')
        n = meeplib.Message('the reply title', 'the reply', u, m.id)
        o = meeplib.Message('the 2nd title', 'the 2nd reply', u, n.id)

        assert n.id in m.replies
        assert o.id in n.replies

        meeplib.set_curr_user(u.username)
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        index = 0
        '''print data[0]
        for m in data:
                #print m
                if 'Delete Post' in m:
                    index += 1
        print 'INDEX: '
        print index'''
        

    def test_recursive_delete(self):
        u = meeplib.User('foo', 'bar')
        m = meeplib.Message('the title', 'the content', u ,'!')
        n = meeplib.Message('the reply title', 'the reply', u, m.id)
        o = meeplib.Message('the second tier title', 'the second reply', u, n.id)
        
        meeplib.delete_message(m)

        assert n not in meeplib._messages.values()
        assert o not in meeplib._messages.values()
        
    


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
