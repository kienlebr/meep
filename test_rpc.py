import unittest
import client_meep_rpc
import rpc_settings
import meeplib

message_id = -1

class TestRpc(unittest.TestCase):
    def server(self):
        return client_meep_rpc.proxy

    def setUp(self):
        client_meep_rpc.connect()

    def test_add_message(self):
        global message_id

        message_id = int(self.server().add_message("RPC Test Title", "RPC Test Message", "!"))
        assert message_id >= 0

        response = self.server().list_messages()
        print response
        assert response != rpc_settings.list_error
        assert "RPC" in response

    def test_delete_message(self):
        global message_id

        print "MESSAGE ID:" + str(message_id)
        response = self.server().delete_message(message_id)
        print response
        assert response == rpc_settings.delete_message_success

        length = self.server().get_messages_length();
        assert length == 0

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()