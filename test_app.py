import unittest
import meep_example_app
import meeplib

class TestApp(unittest.TestCase):
    def setUp(self):
        meep_example_app.initialize()
        app = meep_example_app.MeepExampleApp()
        self.app = app

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

    def test_login(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/create_user'

        def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Username:' in data
        assert 'Password:' in data

    def test_add_reply(self):
        u = meeplib.User('foo', 'bar')
        m = meeplib.Message('the title', 'the content', u ,'!')
        n = meeplib.Message('the reply title', 'the reply', u, m.id)
        o = meeplib.Message('the 2nd title', 'the 2nd reply', u, n.id)

        assert n.id in m.replies
        assert o.id in n.replies

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
