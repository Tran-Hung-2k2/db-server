import sys

sys.path.append(".")

import grpc
import grpc.aio
from fastapi import Request, HTTPException, status
from services_python.pb.auth_pb2 import VerifyRequest
from services_python.pb.auth_pb2_grpc import AuthServiceStub


async def verify_role(request: Request, required_roles: list[str]):
    # Lấy access_token từ cookies
    access_token = request.cookies.get("access_token")

    # Gọi service VerifyRole từ gRPC server
    async with grpc.aio.insecure_channel("127.0.0.1:50051") as channel:
        stub = AuthServiceStub(channel)
        verify_request = VerifyRequest(token=access_token, roles=required_roles)
        try:
            verify_response = await stub.VerifyRole(verify_request)
        except grpc.aio.AioRpcError as e:
            # Kiểm tra và xử lý mã lỗi gRPC
            grpc_code = e.code()
            if grpc_code == grpc.StatusCode.UNAUTHENTICATED:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail=e.details()
                )
            elif grpc_code == grpc.StatusCode.PERMISSION_DENIED:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail=e.details()
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Có lỗi xảy ra, vui lòng thử lại sau.",
                )

    return 1


async def verify_admin(request: Request):
    return await verify_role(request, required_roles=["admin"])


async def verify_user(request: Request):
    return await verify_role(request, required_roles=["user"])


async def verify_all(request: Request):
    return await verify_role(request, required_roles=["admin", "user"])
