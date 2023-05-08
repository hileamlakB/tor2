import grpc
from concurrent import futures
import tor_pb2
import tor_pb2_grpc
import threading
import time

class DirectoryServerServicer(tor_pb2_grpc.DirectoryServerServicer):
    
    def __init__(self):
        super().__init__()
        self.nodes = []
        
        # periodically ping relay nodes to check if they are still alive
        threading.Thread(target=self.RelayPing).start()
        
        
    def GetRelayNodes(self, request, context):
        
        relay_nodes = [tor_pb2.RelayNode(address=f"{address}:{port}") for address, port in self.nodes]
        print(relay_nodes)
        return tor_pb2.GetRelayNodesResponse(relay_nodes=[tor_pb2.RelayNode(address=f"{address}:{port}") for address, port in self.nodes])
    
    def RelayRegister(self, request, context):
        self.nodes.append(request.address.split(":"))
        return tor_pb2.Empty()

    def RelayPing(self):

        # Periodically ping all nodes in the list
        while True:
            time.sleep(10)  # Sleep for a bit (10 seconds)
            alive_nodes = []
            for node in self.nodes:
                # Create a channel and stub to communicate with the relay node
                channel = grpc.insecure_channel(node.address)
                stub = tor_pb2_grpc.RelayStub(channel)

                # Send a Ping message to the relay node
                try:
                    response = stub.Ping(tor_pb2.Empty())
                    alive_nodes.append(node)  # If the relay node is alive, add it to the alive_nodes list
                except grpc.RpcError as e:
                    print(f"Node {node.address} is not responding: {e}")

            self.nodes = alive_nodes  # Update the list of alive nodes

            
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tor_pb2_grpc.add_DirectoryServerServicer_to_server(
        DirectoryServerServicer(), server)
    server.add_insecure_port("localhost:50051")
    # get address at port 50051
    import socket
    
    print("Starting directory server on localhost:50051")
    server.start()
    server.wait_for_termination()



if __name__ == "__main__":
    serve()
