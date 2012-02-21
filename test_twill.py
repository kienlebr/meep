import twill
import unittest
import meep_example_app
import meeplib
import meepcookie

#twillFiles = ['test_add_message.twill', 'test_add_reply.twill', 'test_delete_message.twill', 'test_search_message.twill', 'test_login.twill']

def run(fileName):
    fp = open(fileName)
    twill.execute_string(fp.read(), initial_url='http://localhost:8000/')

class TestTwill(unittest.TestCase):
    def setUp(self):
        pass

    def test_01_twill_scripts(self):
        print 'LOGGING IN'
        run('Twill Scripts/01_testing_login.twill')
        #print 'ADDING MESSAGE'
        #run('Twill Scripts/02_test_add_message.twill')
        #print 'REPLYING TO MESSAGE'
        ##run('Twill Scripts/03_test_reply_message.twill')
        #print 'DELETING MESSAGE'
        #run('Twill Scripts/04_test_delete_message.twill')
        #print 'CREATING USER'
        #run('Twill Scripts/05_test_create_user.twill')
        #print 'LOGGING OUT'
        #run('Twill Scripts/06_test_logout.twill')
        ##print 'Login Successful'

    def test_02_add_message(self):
        print 'ADDING MESSAGE'
        run('Twill Scripts/02_test_add_message.twill')
        #print 'Add Message Successful'

    #def test_03_reply_message(self):
    #    print 'REPLYING TO MESSAGE'
    #    run('Twill Scripts/03_test_reply_message.twill')
    #    #print 'Reply Message Successful'

    def test_04_delete_message(self):
        print 'DELETING MESSAGE'
        run('Twill Scripts/04_test_delete_message.twill')
        #print 'Delete Message Successful'

    def test_05_create_user(self):
        print 'CREATING USER'
        run('Twill Scripts/05_test_create_user.twill')
        #print 'Create User Successful'

    def test_06_logout(self):
        print 'LOGGING OUT'
        run('Twill Scripts/06_test_logout.twill')
        print 'Logout Successful'

    def teardown(self):
        pass

if __name__ == '__main__':
    unittest.main()