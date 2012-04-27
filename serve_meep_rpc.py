import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import meeplib
import rpc_settings

def add_message(title, message, pid):
    try:
        username = "test"
        user = meeplib.get_user(username)

        new_message = meeplib.Message(title, message, user, pid)
        return new_message.id
    except:
        return -1

def delete_message(id):
    try:
        id2 = meeplib.get_message(id);
    except:
        return rpc_settings.delete_message_failure

    meeplib.delete_message(id2)
    return rpc_settings.delete_message_success

def list_messages():
    try:
        if not meeplib._messages:
            return rpc_settings.list_no_messages

        response = ""
        for message in meeplib.get_all_messages():
            response += "id: {0} \ntitle: {1}\n message: {2}\n\n".format(message.id, message.title, message.post)
        return response
    except:
        return rpc_settings.list_error

def get_messages_length():
    messages = meeplib.get_all_messages()
    return len(messages)

def serve():
    #Create server and initialize meeplib
    #meeplib.load_data()
    server = SimpleXMLRPCServer(("localhost", 8001))

    #Register Functions
    server.register_function(add_message, "add_message")
    server.register_function(delete_message, "delete_message")
    server.register_function(list_messages, "list_messages")
    server.register_function(get_messages_length, "get_messages_length")

    #Serve!
    print "Listening on port 8001..."
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        meeplib.save_data()

serve()