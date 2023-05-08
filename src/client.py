from __future__ import print_function

import grpc
import tor_pb2
import tor_pb2_grpc

import threading
import concurrent
import cmd
import os
import uuid
import pickle
from encryption import rsa_encrypt, rsa_decrypt, aes_encrypt, aes_decrypt, generate_rsa_key_pair
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import subprocess
from concurrent import futures
import time


class ClientServicer(tor_pb2_grpc.ClientServicer):

    def __init__(self, client):
        self.client = client
        super().__init__()
        
    def ReceiveMessage(self, request, context):
        print("DEBUG: Recieved message from server")

        # Layer by layer peeling
        # encrypted_message, encrypted_key, iv = pickle.loads(request.message)
        # decrypt aes key with entry node's private key
        aes_key = rsa_decrypt(
            self.client.privateKeys[0], request.encrypted_key)
        # # decrypt message with aes key

        first_layer = pickle.loads(aes_decrypt(
            aes_key, request.iv, request.encrypted_message))
        first_layer_msg = pickle.loads(first_layer['message'])

        # second layer of peeling
        encrypted_msg, encrypted_key, iv = first_layer_msg
        aes_key = rsa_decrypt(self.client.privateKeys[1], encrypted_key)
        second_layer = pickle.loads(aes_decrypt(
            aes_key, iv, encrypted_msg))
        second_layer_msg = pickle.loads(second_layer['message'])

        # third layer of peeling
        encrypted_msg, encrypted_key, iv = second_layer_msg
        aes_key = rsa_decrypt(self.client.privateKeys[2], encrypted_key)
        third_layer = pickle.loads(aes_decrypt(
            aes_key, iv, encrypted_msg))
        third_layer_msg = pickle.loads(third_layer['message'])

        headers, content = third_layer_msg

        # print(content)
        # write content to file
        with open("output.html", "wb") as f:
            f.write(content)
            self.client.response_received = True

        return tor_pb2.Empty()

    def Ping(self, request, context):
        print("DEBUG: Recieved ping from server")
        return tor_pb2.Empty()

class JTor_Client(cmd.Cmd):

    prompt = "JTor> "
    

    def __init__(self, port):
        super(JTor_Client, self).__init__()

        self.user_session_id = ""
        self.address = f'localhost:{port}'
        
        self.num_retries = 10
        self.response_received = False
        self.timeout = 10
        self.current_retries = 0


        # self.do_help("")
        from tor_message import tor_title_basic
        print(tor_title_basic)
        self.get_relay_nodes()
        self.build_circuit()

    def do_send(self, arg):
        args = arg.split(" ")
        if len(args) < 2:
            print("Invalid Arguments to command")
            return
        url = args[0]
        request_type = args[1].upper()

        if request_type not in ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH'):
            # currently we only support GET requests
            print("Error: Invalid request type")
            return

        # You can pass the request_type to the send_message method or use it directly here
        self.send_message(url, request_type)

    def do_exit(self, arg):
        print("Thanks for using JTor! Exiting...")
        quit()

    def do_help(self, arg):
        if arg.lower() == 'send':
            print("Send a URL request through the network.")
            print("Usage: send <url> <request_type>")
            print("Example: send https://example.com GET")
        elif arg.lower() == 'exit':
            print("Exit the JTor client.")
            print("Usage: exit")
        elif arg.lower() == 'help':
            print("Display help messages for available commands.")
            print("Usage: help <command_name>")
        else:
            print("Available commands:")
            print("  send: Send a URL request through the network.")
            print("  exit: Exit the JTor client.")
            print("  help: Display help messages for available commands.")

    def do_shell(self, command):
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        if result.returncode == 0:
            print("Command executed successfully:")
            print(result.stdout)
        else:
            print("Command execution failed with error code:", result.returncode)
            print(result.stderr)

    def get_relay_nodes(self):
        print("Getting relay nodes from directory server...")
        channel = grpc.insecure_channel("localhost:50051")
        stub = tor_pb2_grpc.DirectoryServerStub(channel)
        response = stub.GetRelayNodes(tor_pb2.GetRelayNodesRequest())
        print(type(response.relay_nodes))
        self.relay_entry, self.relay_middle, self.relay_exit = list(response.relay_nodes)[:3]

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

        # print(encryption_keypairs)
        # Store keys on the client
        self.publicKeys = [kp[0] for kp in encryption_keypairs]
        print(self.publicKeys)
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

        print('DEBUG: Received public keys from relay nodes')
        return

    def send_message(self, url, request_type):
        # Construct the onion
        
        # set recieve message to false
        self.response_received = False
        # inner layer
        inner_aes_key = os.urandom(32)
        inner_msg = pickle.dumps({
            "message": request_type.encode('utf-8'),
            # should be address of the server
            "destination": url.encode('utf-8'),


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
            "iv": middle_iv,

        })
        print(outer_aes_key)
        outer_iv, outer_onion = aes_encrypt(outer_aes_key, outer_msg)

        outer_aes_encrypted_key = rsa_encrypt(self.relay_publicKeys[0],
                                              outer_aes_key)
        print(type(outer_msg), "outer_msg")
        # Send the onion to the entry relay node
        entry_stub = self.relay_stubs[0]
        print(type(outer_onion), type(outer_aes_encrypted_key))
        entry_stub.ForwardMessage(
            tor_pb2.ProcessMessageRequest(
                encrypted_message=outer_onion,
                encrypted_key=outer_aes_encrypted_key,
                iv=outer_iv,
                session_id=self.session_id.encode('utf-8'),
                return_address=self.address  # client address)
            )

        )
       
        start_time = time.time()
        
        # start waiting for response 
        while time.time() - start_time < self.timeout:
            if self.response_received:
                break
            else:
                time.sleep(1)

        if not self.response_received:
            self.current_retries += 1
            if self.current_retries < self.max_retries:
                # get new relay nodes
                self.get_relay_nodes()
                self.build_circuit()
                self.send_message(url, request_type)
            else:
                print("Max retries reached, exiting")
                return
            


def serve(port, client_terminal):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tor_pb2_grpc.add_ClientServicer_to_server(
        ClientServicer(client_terminal), server)
    server.add_insecure_port(f"localhost:{port}")
    print(f"Starting client node on localhost:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':

    client_terminal = JTor_Client(5432)
    server_thread = threading.Thread(
        target=serve, args=(5432, client_terminal,))
    server_thread.start()

    client_terminal.cmdloop()
    server_thread.join()
