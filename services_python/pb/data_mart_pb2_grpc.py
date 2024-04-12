# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import data_mart_pb2 as data__mart__pb2


class DataMartServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetDataMart = channel.unary_unary(
                '/proto.DataMartService/GetDataMart',
                request_serializer=data__mart__pb2.GetDataMartRequest.SerializeToString,
                response_deserializer=data__mart__pb2.GetDataMartResponse.FromString,
                )


class DataMartServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetDataMart(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataMartServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetDataMart': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDataMart,
                    request_deserializer=data__mart__pb2.GetDataMartRequest.FromString,
                    response_serializer=data__mart__pb2.GetDataMartResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.DataMartService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DataMartService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetDataMart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.DataMartService/GetDataMart',
            data__mart__pb2.GetDataMartRequest.SerializeToString,
            data__mart__pb2.GetDataMartResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
