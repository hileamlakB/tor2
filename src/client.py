import grpc
import tor_pb2
import tor_pb2_grpc


def get_relay_nodes():
    channel = grpc.insecure_channel("localhost:50051")
    stub = tor_pb2_grpc.DirectoryServerStub(channel)
    response = stub.GetRelayNodes(tor_pb2.GetRelayNodesRequest())
    return response.relay_nodes


def send_message(message, relay_nodes):
    # Implement Key sharing with relays
    # this might require adding more services on the relays side
    # for key sharing
    # message encryption and sending logic
    pass

# implement client logic preferably
# using the cmd module to create a command line interface