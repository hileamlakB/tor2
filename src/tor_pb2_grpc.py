# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import tor_pb2 as tor__pb2


class ClientStub(object):
    """Service for clients
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ReceiveMessage = channel.unary_unary(
                '/tor.Client/ReceiveMessage',
                request_serializer=tor__pb2.ProcessMessageRequest.SerializeToString,
                response_deserializer=tor__pb2.Empty.FromString,
                )


class ClientServicer(object):
    """Service for clients
    """

    def ReceiveMessage(self, request, context):
        """listen for incoming messages
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ReceiveMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveMessage,
                    request_deserializer=tor__pb2.ProcessMessageRequest.FromString,
                    response_serializer=tor__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tor.Client', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Client(object):
    """Service for clients
    """

    @staticmethod
    def ReceiveMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tor.Client/ReceiveMessage',
            tor__pb2.ProcessMessageRequest.SerializeToString,
            tor__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class RelayStub(object):
    """Service for relay nodes
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ForwardMessage = channel.unary_unary(
                '/tor.Relay/ForwardMessage',
                request_serializer=tor__pb2.ProcessMessageRequest.SerializeToString,
                response_deserializer=tor__pb2.ProcessMessageResponse.FromString,
                )
        self.BackwardMessage = channel.unary_unary(
                '/tor.Relay/BackwardMessage',
                request_serializer=tor__pb2.ProcessMessageRequest.SerializeToString,
                response_deserializer=tor__pb2.ProcessMessageResponse.FromString,
                )
        self.ExchangeKeys = channel.unary_unary(
                '/tor.Relay/ExchangeKeys',
                request_serializer=tor__pb2.ExchangeKeyRequest.SerializeToString,
                response_deserializer=tor__pb2.ExchangeKeyResponse.FromString,
                )


class RelayServicer(object):
    """Service for relay nodes
    """

    def ForwardMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BackwardMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExchangeKeys(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RelayServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ForwardMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.ForwardMessage,
                    request_deserializer=tor__pb2.ProcessMessageRequest.FromString,
                    response_serializer=tor__pb2.ProcessMessageResponse.SerializeToString,
            ),
            'BackwardMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.BackwardMessage,
                    request_deserializer=tor__pb2.ProcessMessageRequest.FromString,
                    response_serializer=tor__pb2.ProcessMessageResponse.SerializeToString,
            ),
            'ExchangeKeys': grpc.unary_unary_rpc_method_handler(
                    servicer.ExchangeKeys,
                    request_deserializer=tor__pb2.ExchangeKeyRequest.FromString,
                    response_serializer=tor__pb2.ExchangeKeyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tor.Relay', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Relay(object):
    """Service for relay nodes
    """

    @staticmethod
    def ForwardMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tor.Relay/ForwardMessage',
            tor__pb2.ProcessMessageRequest.SerializeToString,
            tor__pb2.ProcessMessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BackwardMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tor.Relay/BackwardMessage',
            tor__pb2.ProcessMessageRequest.SerializeToString,
            tor__pb2.ProcessMessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ExchangeKeys(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tor.Relay/ExchangeKeys',
            tor__pb2.ExchangeKeyRequest.SerializeToString,
            tor__pb2.ExchangeKeyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class DirectoryServerStub(object):
    """Service for the directory server
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetRelayNodes = channel.unary_unary(
                '/tor.DirectoryServer/GetRelayNodes',
                request_serializer=tor__pb2.GetRelayNodesRequest.SerializeToString,
                response_deserializer=tor__pb2.GetRelayNodesResponse.FromString,
                )


class DirectoryServerServicer(object):
    """Service for the directory server
    """

    def GetRelayNodes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DirectoryServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetRelayNodes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRelayNodes,
                    request_deserializer=tor__pb2.GetRelayNodesRequest.FromString,
                    response_serializer=tor__pb2.GetRelayNodesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tor.DirectoryServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DirectoryServer(object):
    """Service for the directory server
    """

    @staticmethod
    def GetRelayNodes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tor.DirectoryServer/GetRelayNodes',
            tor__pb2.GetRelayNodesRequest.SerializeToString,
            tor__pb2.GetRelayNodesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
