import grpc
from concurrent import futures
import tor_pb2
import tor_pb2_grpc

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
            print("DEBUG: Public key received" + str(request.key))
            self.public_key = request.key
        if request.key_type == tor_pb2.PRIVATE:
            print("DEBUG: Private key received" + str(request.key))
            self.private_key = request.key
        return tor_pb2.AcceptKeyResponse(response=...)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tor_pb2_grpc.add_RelayServicer_to_server(RelayServicer(), server)
    server.add_insecure_port("localhost:50052")  # TODO: Use a different port for each relay node
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
