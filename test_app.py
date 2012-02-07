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

    def test_main_page(self):
        u = meeplib.User('foo', 'bar')
        meeplib.Message('the title', 'the content', u ,'!')
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/main_page'

        def fake_start_response(status, headers):
            assert status == "200 OK"
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        print data
        assert "Add Message" in data

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
