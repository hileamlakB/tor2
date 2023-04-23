import grpc
from concurrent import futures
import tor_pb2
import tor_pb2_grpc

import argparse

class RelayServicer(tor_pb2_grpc.RelayServicer):
    def ProcessOutboundMessage(self, request, context):
        # Implement decryption, forwarding, and circuit building 
        # and onion routing logic
        return tor_pb2.ProcessMessageResponse(encrypted_message=...)

    def ProcessReturnMessage(self, request, context):
        # Process the message going in reverse
        return tor_pb2.ProcessMessageResponse(encrypted_message=...)
    
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
    args = parser.parse_args()
    port = args.port
    serve(port)
