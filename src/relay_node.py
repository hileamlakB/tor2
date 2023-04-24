import grpc
from concurrent import futures
import tor_pb2
import tor_pb2_grpc

import argparse
import pickle
import rsa
import codecs
from cryptography.hazmat.primitives import serialization
from encryption import rsa_encrypt, rsa_decrypt, aes_encrypt, aes_decrypt, generate_rsa_key_pair


class RelayServicer(tor_pb2_grpc.RelayServicer):

    def __init__(self):
        super().__init__()

        self.relay_public_key, self.relay_private_key = generate_rsa_key_pair(
            1024)
        self.relay_public_key_str = self.relay_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        self.sessions = {

        }

    def ProcessMessage(self, request, context):
        # session_id = request.session_id.decode('utf-8')
        # decrypt the key
        aes_key = rsa_decrypt(self.relay_private_key, request.encrypted_key)
        iv = request.iv

        # peal layer using aes key
        inner = aes_decrypt(aes_key, iv, request.encrypted_message)
        inner_dict = pickle.loads(inner)

        # construct the message for the next node
        if inner_dict['destination'] == None:
            print("DEBUG: Reached destination")
            print("DEBUG: Message", inner_dict['message'])

        else:
            msg = tor_pb2.ProcessMessageRequest(
                encrypted_message=inner_dict['message'],
                encrypted_key=inner_dict['encrypted_key'],
                iv=inner_dict['iv'],
                session_id=request.session_id
            )
            next_relay = inner_dict['destination']
            stub = tor_pb2_grpc.RelayStub(grpc.insecure_channel(next_relay))
            stub.ProcessMessage(msg)

        # create a channel and a stub to communicate to the next node

        # i
        # print("DEBUG: Inner layer", inner_dict)

        return tor_pb2.ProcessMessageResponse()

    def ExchangeKeys(self, request, context):

        session_id = request.session_id
        publickey = request.public_key

        print("DEBUG: Received public key from client", publickey)

        self.sessions[session_id] = publickey
        return tor_pb2.ExchangeKeyResponse(public_key=self.relay_public_key_str)


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tor_pb2_grpc.add_RelayServicer_to_server(RelayServicer(), server)
    server.add_insecure_port(f"localhost:{port}")
    print(f"Starting relay node on localhost:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a relay node")
    parser.add_argument("port", help="Unique port of relay node")
    # parser.add_argument("type", help="Node type: entry (1), middle (2), or exit (3)")
    args = parser.parse_args()
    port = args.port
    # type = args.type
    serve(port)
