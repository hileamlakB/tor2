import grpc
from concurrent import futures
import tor_pb2
import tor_pb2_grpc

import argparse
import rsa
import codecs

class RelayServicer(tor_pb2_grpc.RelayServicer):
    def ProcessOutboundMessage(self, request, context):
        # Process messages going from client to destination
        print(f"DEBUG: Encrypted msg:\n{request.encrypted_message}\n")
        encrypted_msg = request.encrypted_message[2:-1]
        print(f"DEBUG: trimmed\n{encrypted_msg}\n")
        # encrypted_msg = codecs.escape_decode(bytes(encrypted_msg, 'utf-8'))[0].decode('utf-8')
        # encrypted_msg = bytes(encrypted_msg, 'utf-8').decode('unicode_escape')
        print(f"DEBUG: after bytes converstion:\n{encrypted_msg}")
        # Decrypt a layer of the onion using the private key
        decrypted_message = rsa.decrypt(request.encrypted_message, rsa.PrivateKey.load_pkcs1(self.private_key))
        print(f"DEBUG: decrypted message {decrypted_message}")
        print(f"DEBUG: decrypted message decoded {decrypted_message.decode('utf-8')}")
        # Figure out the next node
            # If next node == null, then reached the exit node, forward the request to the internet
            # Else
                # Establish connection to next node
                # Send remainder of onion to that next node

        return tor_pb2.ProcessMessageResponse(encrypted_message="Response TODO") # Return simply that the message was forwarded?

    def ProcessReturnMessage(self, request, context):
        # Process messages going back to client from destination

        # Encrypt the onion with an additional layer using the public key

        # Figure out the return node

        # Establish connection to return node

        # Send onion to return node

        return tor_pb2.ProcessMessageResponse(encrypted_message="Response TODO")
    
    def AcceptKey(self, request, context):
        if request.key_type == tor_pb2.PUBLIC:
            print("DEBUG: Public key received:\n" + str(request.key))
            self.public_key = request.key
        if request.key_type == tor_pb2.PRIVATE:
            print("DEBUG: Private key received:\n" + str(request.key))
            # print("DEBUG: HELLO!!!")
            self.private_key = request.key
        # print("DEBUG: returning out of relay_node")
        return tor_pb2.AcceptKeyResponse(response="Success!")

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
