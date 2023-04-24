from __future__ import print_function

import grpc
import tor_pb2
import tor_pb2_grpc

import logging
import threading
import concurrent
import cmd
import os
import rsa
import uuid
import pickle
from encryption import rsa_encrypt, rsa_decrypt, aes_encrypt, aes_decrypt, generate_rsa_key_pair
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class JTor_Client(cmd.Cmd):

    prompt = "JTor> "

    def __init__(self, port):
        super(JTor_Client, self).__init__()

        self.user_session_id = ""
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.stub = tor_pb2_grpc.ClientStub(self.channel)

        self.do_help("")
        self.get_relay_nodes()
        self.build_circuit()

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

    def get_relay_nodes(self):
        print("Getting relay nodes from directory server...")
        channel = grpc.insecure_channel("localhost:50051")
        stub = tor_pb2_grpc.DirectoryServerStub(channel)
        response = stub.GetRelayNodes(tor_pb2.GetRelayNodesRequest())
        self.relay_entry, self.relay_middle, self.relay_exit = response.relay_nodes

    def build_circuit(self):

        self.session_id = str(uuid.uuid4())
        self.relay_channels = [
            grpc.insecure_channel(self.relay_entry.address),
            grpc.insecure_channel(self.relay_middle.address),
            grpc.insecure_channel(self.relay_exit.address)
        ]
        self.relay_stubs = [tor_pb2_grpc.RelayStub(
            channel) for channel in self.relay_channels]

        # Generate RSA key pairs concurrently
        key_sizes = [1024, 1024, 1024]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            encryption_keypairs = list(
                executor.map(generate_rsa_key_pair, key_sizes))

        print(encryption_keypairs)
        # Store keys on the client
        self.publicKeys = [kp[0] for kp in encryption_keypairs]
        self.privateKeys = [kp[1] for kp in encryption_keypairs]
        self.relay_publicKeys = []

        # Send key pairs to the relay nodes and receive their public keys
        for i, stub in enumerate(self.relay_stubs):
            public_key_pem = self.publicKeys[i].public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')

            response = stub.ExchangeKeys(
                tor_pb2.ExchangeKeyRequest(
                    session_id=self.session_id,
                    public_key=public_key_pem))

            relay_public_key = serialization.load_pem_public_key(
                response.public_key.encode('utf-8'),
                backend=default_backend()
            )
            self.relay_publicKeys.append(relay_public_key)

        print('Received public keys from relay nodes', self.relay_publicKeys)
        return

    def send_message(self, message):
        # Construct the onion

        # inner layer
        inner_aes_key = os.urandom(32)
        inner_msg = pickle.dumps({
            "message": message.encode('utf-8'),
            "destination": None  # should be address of the server
        })
        inner_iv, inner_onion = aes_encrypt(inner_aes_key, inner_msg)

        # middle layer
        middle_aes_key = os.urandom(32)
        middle_msg = pickle.dumps({
            "message": inner_onion,
            "destination": self.relay_exit.address,
            "encrypted_key": rsa_encrypt(self.relay_publicKeys[2], inner_aes_key),
            "iv": inner_iv,
        })
        middle_iv, middle_onion = aes_encrypt(middle_aes_key, middle_msg)

        # outer layer
        outer_aes_key = os.urandom(32)
        outer_msg = pickle.dumps({
            "message": middle_onion,
            "destination": self.relay_middle.address,
            "encrypted_key": rsa_encrypt(self.relay_publicKeys[1], middle_aes_key),
            "iv": middle_iv
        })
        print(outer_aes_key)
        outer_iv, outer_onion = aes_encrypt(outer_aes_key, outer_msg)

        outer_aes_encrypted_key = rsa_encrypt(self.relay_publicKeys[0],
                                              outer_aes_key)
        print(type(outer_msg), "outer_msg")
        # Send the onion to the entry relay node
        entry_stub = self.relay_stubs[0]
        print(type(outer_onion), type(outer_aes_encrypted_key))
        entry_stub.ProcessMessage(
            tor_pb2.ProcessMessageRequest(
                encrypted_message=outer_onion,
                encrypted_key=outer_aes_encrypted_key,
                iv=outer_iv,
                session_id=self.session_id.encode('utf-8'))
        )


if __name__ == '__main__':
    logging.basicConfig()
    JTor_Client(5432).cmdloop()
