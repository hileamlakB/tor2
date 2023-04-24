from __future__ import print_function

import grpc
import tor_pb2
import tor_pb2_grpc

import logging
import threading
import cmd
import rsa

# implement client logic preferably
# using the cmd module to create a command line interface
class JTor_Client(cmd.Cmd):
    def get_relay_nodes(self):
        channel = grpc.insecure_channel("localhost:50051") # directory server lives here
        stub = tor_pb2_grpc.DirectoryServerStub(channel)
        response = stub.GetRelayNodes(tor_pb2.GetRelayNodesRequest())
        return response.relay_nodes

    # TODO: Implement Key sharing with relays
    # this might require adding more services on the relays side
    # for key sharing
    # message encryption and sending logic
    def request_circuit(self):
        # Simple key-sharing scheme on initialization involes simply sending
        # the keys over in plaintext to the various relay nodes

        # Establish connection with entry relay node
        entry_channel = grpc.insecure_channel(f'localhost:{self.relay_entry.address}')
        entry_stub = tor_pb2_grpc.RelayStub(entry_channel)

        # Establish connection with middle relay node
        middle_channel = grpc.insecure_channel(f'localhost:{self.relay_middle.address}')
        middle_stub = tor_pb2_grpc.RelayStub(middle_channel)

        # Establish connection with exit relay node
        exit_channel = grpc.insecure_channel(f'localhost:{self.relay_exit.address}')
        exit_stub = tor_pb2_grpc.RelayStub(exit_channel)

        # Generate 3 private/public keypairs for encryption
        publicKey_entry_e, privateKey_entry_e = rsa.newkeys(4096)
        publicKey_middle_e, privateKey_middle_e = rsa.newkeys(1024)
        publicKey_exit_e, privateKey_exit_e = rsa.newkeys(256)

        # Generate 3 private/public keypairs for decryption
        publicKey_entry_d, privateKey_entry_d = rsa.newkeys(256) # 256
        publicKey_middle_d, privateKey_middle_d = rsa.newkeys(256) # 1024
        publicKey_exit_d, privateKey_exit_d = rsa.newkeys(256) # 4096

        # Store keys on the client
        self.publicKey_entry = publicKey_entry_e.save_pkcs1().decode('utf-8')
        self.publicKey_middle = publicKey_middle_e.save_pkcs1().decode('utf-8')
        self.publicKey_exit = publicKey_exit_e.save_pkcs1().decode('utf-8')

        self.debug_key = privateKey_entry_e.save_pkcs1().decode('utf-8')

        self.privateKey_entry = privateKey_entry_d.save_pkcs1().decode('utf-8')
        self.privateKey_middle = privateKey_middle_d.save_pkcs1().decode('utf-8')
        self.privateKey_exit = privateKey_exit_d.save_pkcs1().decode('utf-8')

        # Send the keypairs to the relay nodes
        # TODO: Make this more secure
        response = entry_stub.AcceptKey(tor_pb2.AcceptKeyRequest(key=privateKey_entry_e.save_pkcs1().decode('utf-8'), key_type=tor_pb2.PRIVATE))
        response = entry_stub.AcceptKey(tor_pb2.AcceptKeyRequest(key=publicKey_entry_d.save_pkcs1().decode('utf-8'), key_type=tor_pb2.PUBLIC))

        response = middle_stub.AcceptKey(tor_pb2.AcceptKeyRequest(key=privateKey_middle_e.save_pkcs1().decode('utf-8'), key_type=tor_pb2.PRIVATE))
        response = middle_stub.AcceptKey(tor_pb2.AcceptKeyRequest(key=publicKey_middle_d.save_pkcs1().decode('utf-8'), key_type=tor_pb2.PUBLIC))

        response = exit_stub.AcceptKey(tor_pb2.AcceptKeyRequest(key=privateKey_exit_e.save_pkcs1().decode('utf-8'), key_type=tor_pb2.PRIVATE))
        response = exit_stub.AcceptKey(tor_pb2.AcceptKeyRequest(key=publicKey_exit_d.save_pkcs1().decode('utf-8'), key_type=tor_pb2.PUBLIC))

        # TODO: Persist all keys in case of failures

        print(response.response)

        return response.response

    def send_message(self, message):
        # Construct the onion
        inner_layer = rsa.encrypt(str((message, None)).encode('utf-8'), rsa.PublicKey.load_pkcs1(self.publicKey_exit))
        middle_layer = rsa.encrypt(str((inner_layer, self.relay_exit.address)).encode('utf-8'), rsa.PublicKey.load_pkcs1(self.publicKey_middle))
        outer_onion = rsa.encrypt(str((middle_layer, self.relay_middle.address)).encode('utf-8'), rsa.PublicKey.load_pkcs1(self.publicKey_entry))
        
        decrypted_msg = rsa.decrypt(outer_onion, rsa.PrivateKey.load_pkcs1(self.debug_key))
        # print(f"DEBUG: r3 public key: {rsa.PublicKey.load_pkcs1(self.publicKey_exit)}")
        # print(f"Inner layer:\n{inner_layer}\n{str((message, None)).encode('utf-8')}")
        print(f"Middle layer encrypted:\n{middle_layer}\n")
        print(f"Middle layer raw:\n{str((inner_layer, self.relay_exit.address)).encode('utf-8')}\n")
        print(f"Decrypted msg:\n{decrypted_msg}\n")
        print(f"DEBUG: onion being sent: {outer_onion}")

        # Establish connection with entry relay node
        channel = grpc.insecure_channel(f'localhost:{self.relay_entry.address}')
        stub = tor_pb2_grpc.RelayStub(channel)

        # Send the onion to entry relay
        response = stub.ProcessOutboundMessage(tor_pb2.ProcessMessageRequest(encrypted_message=str(outer_onion), next_relay_node=self.relay_entry))
        return response # response.status?

    def retrieve_message(self, message, relay_nodes):
        # Establish connection with the entry relay node
        channel = grpc.insecure_channel(f'localhost:{self.relay_entry.address}')
        stub = tor_pb2_grpc.RelayStub(channel)

        # Get the return message
        response = stub.ProcessReturnMessage(tor_pb2.ProcessMessageRequest())

        # Deconstruct the onion
        # Use the same private/public keypairs, unpickle the dictionaries
        pass
    
    prompt = "JTor> "

    def __init__(self, port):
        super(JTor_Client, self).__init__()

        self.user_session_id = ""
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.stub = tor_pb2_grpc.ClientStub(self.channel)

        self.do_help("")
        self.do_getNode()
        self.do_exchangeKey()

    def do_getNode(self):
        print("doing getnode")
        relay_nodes = self.get_relay_nodes()
        if relay_nodes[0].node_type == tor_pb2.ENTRY:
            self.relay_entry = relay_nodes[0]
        if relay_nodes[1].node_type == tor_pb2.MIDDLE:
            self.relay_middle = relay_nodes[1]
        if relay_nodes[2].node_type == tor_pb2.EXIT:
            self.relay_exit = relay_nodes[2]

    def do_exchangeKey(self):
        print("exchanging keys")
        self.request_circuit()

    def do_send(self, arg):
        args = arg.split(" ")
        if (len(args) < 1):
            print("Invalid Arguments to command")
            return
        if self.relay_entry is None:
            print("Error: No entry node specified")
            return
        if self.relay_middle is None:
            print("Error: No middle node specified")
            return
        if self.relay_exit is None:
            print("Error: No exit node specified")
            return
        
        url = args[0]
        self.send_message(url)

    def do_exit(self, arg):
        print("Thanks for using JTor! Exiting...")
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
    JTor_Client(5432).cmdloop()
