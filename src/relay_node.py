import grpc
from concurrent import futures
import tor_pb2
import tor_pb2_grpc

import argparse
import pickle
from cryptography.hazmat.primitives import serialization
from encryption import rsa_encrypt, rsa_decrypt, aes_encrypt, aes_decrypt, generate_rsa_key_pair
from cryptography.hazmat.backends import default_backend
import os
import requests


def get_page(url):

    response = requests.get(url)

    headers = dict(response.headers)
    content = response.content

    return headers, content


class RelayServicer(tor_pb2_grpc.RelayServicer):

    ENTRY_NODE = 1
    GUARD_NODE = 2
    EXIT_NODE = 3

    def __init__(self, port, relay_type, directory_server):
        super().__init__()

        self.address = f'localhost:{port}'
        self.relay_type = relay_type
        self.relay_public_key, self.relay_private_key = generate_rsa_key_pair(
            1024)
        self.relay_public_key_str = self.relay_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        directory_server_address = ':'.join(list(directory_server))
        # create a stub and channel for the directory server
        channel = grpc.insecure_channel(directory_server_address)
        stub = tor_pb2_grpc.DirectoryServerStub(channel)
        # try to connect to the directory server continuously
        while True:
            try:
                
                response = stub.RelayRegister(tor_pb2.RelayNode(
                    address=self.address, node_type = self.relay_type))
                break
            except Exception as E:
                print("DEBUG: Failed to connect to directory server, retrying...")
                continue
            
        
        
        # register with the directory server
        

        self.session_keys = {

        }

        self.return_addresses = {

        }
    def Ping(self, request, context):
        return tor_pb2.Empty()

    def BackwardMessage(self, request, context):
        return_address = self.return_addresses[request.session_id.decode(
            'utf-8')]
        print("DEBUG: BackwardMessage recieved forwarding to ", return_address)

        aes_key = os.urandom(32)
        msg = pickle.dumps({
            "message": pickle.dumps((request.encrypted_message, request.encrypted_key, request.iv)),
        })
        # encrypt with aes key
        iv, encrypted_message = aes_encrypt(aes_key, msg)

        # encrypt aes key with the session key
        encrypted_key = rsa_encrypt(
            self.session_keys[request.session_id.decode('utf-8')], aes_key)

        msg = tor_pb2.ProcessMessageRequest(
            encrypted_message=encrypted_message,
            encrypted_key=encrypted_key,
            iv=iv,
            session_id=request.session_id,
        )

        return_address = self.return_addresses[request.session_id.decode(
            'utf-8')]
        if self.relay_type == self.ENTRY_NODE:
            print("DEBUG: Reached entry node; sending to client")
            # send to client
            with grpc.insecure_channel(return_address) as channel:
                stub = tor_pb2_grpc.ClientStub(channel)
                stub.ReceiveMessage(msg)
        else:
            # send to the next relay
            stub = tor_pb2_grpc.RelayStub(
                grpc.insecure_channel(return_address))
            stub.BackwardMessage(msg)

        return tor_pb2.ProcessMessageResponse()

    def ForwardMessage(self, request, context):

        client_address = request.return_address
        # store the client's address for later returns
        self.return_addresses[request.session_id.decode(
            'utf-8')] = client_address

        # session_id = request.session_id.decode('utf-8')
        # decrypt the key
        aes_key = rsa_decrypt(self.relay_private_key, request.encrypted_key)
        iv = request.iv

        # peal layer using aes key
        inner = aes_decrypt(aes_key, iv, request.encrypted_message)
        inner_dict = pickle.loads(inner)

        # this probably should be done on a different thread
        # so the relay can continue to receive messages
        # construct the message for the next node
        if self.relay_type == self.EXIT_NODE:
            print("DEBUG: Reached exit node; getting page")
            headers, content = get_page(
                inner_dict['destination'].decode('utf-8'))

            # print(headers, content)
            # send the response back to the client
            inner_aes_key = os.urandom(32)
            inner_msg = pickle.dumps({
                "message": pickle.dumps((headers, content))
            })

            inner_iv, inner_onion = aes_encrypt(inner_aes_key, inner_msg)

            # encrypt the aes key with the client's public key
            inner_aes_encrypted_key = rsa_encrypt(
                self.session_keys[request.session_id.decode('utf-8')], inner_aes_key)

            msg = tor_pb2.ProcessMessageRequest(
                encrypted_message=inner_onion,
                encrypted_key=inner_aes_encrypted_key,
                iv=inner_iv,
                session_id=request.session_id)

            print("DEBUG: Sending back to previous relay: ",
                  self.return_addresses[request.session_id.decode('utf-8')])
            # create a channel and a stup to return the message to the caller
            stub = tor_pb2_grpc.RelayStub(grpc.insecure_channel(
                self.return_addresses[request.session_id.decode('utf-8')]))
            stub.BackwardMessage(msg)

        else:
            msg = tor_pb2.ProcessMessageRequest(
                encrypted_message=inner_dict['message'],
                encrypted_key=inner_dict['encrypted_key'],
                iv=inner_dict['iv'],
                session_id=request.session_id,
                return_address=self.address
            )

            print("DEBUG: Relay Received Message: From", client_address,
                  "; Forwarding To", inner_dict['destination'])

            # create a channel and a stub to communicate to the next node
            next_relay = inner_dict['destination']
            stub = tor_pb2_grpc.RelayStub(grpc.insecure_channel(next_relay))
            stub.ForwardMessage(msg)

        return tor_pb2.ProcessMessageResponse()

    def ExchangeKeys(self, request, context):

        session_id = request.session_id
        publickey = request.public_key

        print("DEBUG: Received public key from client", publickey)

        # decode the public key
        session_public_key = serialization.load_pem_public_key(
            publickey.encode('utf-8'),
            backend=default_backend()
        )

        self.session_keys[session_id] = session_public_key
        return tor_pb2.ExchangeKeyResponse(public_key=self.relay_public_key_str)


def serve(port, relay_type, directory_server):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tor_pb2_grpc.add_RelayServicer_to_server(
        RelayServicer(port, int(relay_type), directory_server), server)
    server.add_insecure_port(f"localhost:{port}")
    print(f"Starting relay node on localhost:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a relay node")
    parser.add_argument("port", help="Unique port of relay node")
    parser.add_argument(
        "type", help="Node type: entry (1), middle (2), or exit (3)")
    parser.add_argument(
        "directory_server", help="Address of the directory server"
    )
    args = parser.parse_args()
    port = args.port
    relay_type = int(args.type)
    directory_server = args.directory_server.split(':')
    serve(port, relay_type, directory_server)
