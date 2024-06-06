# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import services_python.pb.auth_pb2 as auth__pb2


class AuthServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.VerifyRole = channel.unary_unary(
            "/proto.AuthService/VerifyRole",
            request_serializer=auth__pb2.VerifyRequest.SerializeToString,
            response_deserializer=auth__pb2.VerifyResponse.FromString,
        )


class AuthServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def VerifyRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_AuthServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "VerifyRole": grpc.unary_unary_rpc_method_handler(
            servicer.VerifyRole,
            request_deserializer=auth__pb2.VerifyRequest.FromString,
            response_serializer=auth__pb2.VerifyResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "proto.AuthService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class AuthService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def VerifyRole(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/proto.AuthService/VerifyRole",
            auth__pb2.VerifyRequest.SerializeToString,
            auth__pb2.VerifyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
