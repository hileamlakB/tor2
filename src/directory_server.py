import grpc
from concurrent import futures
import tor_pb2
import tor_pb2_grpc

class DirectoryServerServicer(tor_pb2_grpc.DirectoryServerServicer):
    def GetRelayNodes(self, request, context):
        print("returning relay nodes")
        # for the sake of simplicity, we will return a list of relay nodes
        # in reality, we would query the directory server for the list
        entry_node = tor_pb2.RelayNode(address="2525", node_type=tor_pb2.ENTRY)
        middle_node = tor_pb2.RelayNode(address="2526", node_type=tor_pb2.MIDDLE)
        exit_node = tor_pb2.RelayNode(address="2527", node_type=tor_pb2.EXIT)
        return tor_pb2.GetRelayNodesResponse(relay_nodes=[entry_node, middle_node, exit_node])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tor_pb2_grpc.add_DirectoryServerServicer_to_server(DirectoryServerServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
