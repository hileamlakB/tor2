from __future__ import print_function

import grpc
import tor_pb2
import tor_pb2_grpc

import logging
import threading
import cmd

def get_relay_nodes():
    channel = grpc.insecure_channel("localhost:50051")
    stub = tor_pb2_grpc.DirectoryServerStub(channel)
    response = stub.GetRelayNodes(tor_pb2.GetRelayNodesRequest())
    return response.relay_nodes


def send_message(message, relay_nodes):
    # Implement Key sharing with relays
    # this might require adding more services on the relays side
    # for key sharing
    # message encryption and sending logic
    pass

# implement client logic preferably
# using the cmd module to create a command line interface
class JTor_Client(cmd.Cmd):
    prompt = "JTor> "

    def __init__(self, port):
        super(JTor_Client, self).__init__()

        self.user_session_id = ""
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.stub = tor_pb2_grpc.ClientStub(self.channel)

        self.do_help("")

    def do_getNode(self, arg):
        print("doing getnode")
        pass

    def do_send(self, arg):
        args = arg.split(" ")
        if (len(args) < 1):
            print("Invalid Arguments to command")
            return
        
        url = args[0]

    def do_exit(self, arg):
        print("doing exit")
        quit()

    # Print various help messages
    def do_help(self, arg):
        print("Placeholder help message")
        print(arg)

        # HELP_SEND = 'send a url through the network'
        # usage: send <url> <entry_node>

        # HELP_GETNODES = 'get all the relay nodes'
        # usage: getNode

if __name__ == '__main__':
    logging.basicConfig()
    JTor_Client(2625).cmdloop()
