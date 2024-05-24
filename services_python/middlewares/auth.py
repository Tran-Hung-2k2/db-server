import os
import grpc
import grpc.aio
import services_python.constants.label as label
from fastapi import Request, HTTPException, status
from services_python.pb.auth_pb2 import VerifyRequest
from services_python.pb.auth_pb2_grpc import AuthServiceStub
import os
import grpc
import grpc.aio
import services_python.constants.label as label
from fastapi import Request, HTTPException, status
from services_python.pb.auth_pb2 import VerifyRequest
from services_python.pb.auth_pb2_grpc import AuthServiceStub

# Lấy địa chỉ của server gRPC từ biến môi trường, nếu không có thì mặc định là "127.0.0.1:50051"
AUTH_GRPC_SERVER = os.getenv("AUTH_GRPC_SERVER", "127.0.0.1:50051")


# Hàm kiểm tra quyền của người dùng
async def verify_role(request: Request, required_roles: list[str]):
    # Lấy access token từ cookie
    access_token = request.cookies.get("access_token")

    # Tạo kết nối đến server gRPC
    async with grpc.aio.insecure_channel(AUTH_GRPC_SERVER) as channel:
        # Tạo stub từ AuthService
        stub = AuthServiceStub(channel)

        # Tạo request với token và danh sách quyền cần kiểm tra
        verify_request = VerifyRequest(token=access_token, roles=required_roles)
        try:
            # Gửi request và nhận về response
            verify_response = await stub.VerifyRole(verify_request)
        except grpc.aio.AioRpcError as e:
            # Xử lý các lỗi có thể xảy ra khi gọi hàm gRPC
            grpc_code = e.code()
            if grpc_code == grpc.StatusCode.UNAUTHENTICATED:
                # Nếu lỗi do chưa xác thực, trả về lỗi 401
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail=e.details()
                )
            elif grpc_code == grpc.StatusCode.PERMISSION_DENIED:
                # Nếu lỗi do không có quyền, trả về lỗi 403
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail=e.details()
                )
            else:
                # Nếu lỗi khác, trả về lỗi 500
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Có lỗi xảy ra, vui lòng thử lại sau.",
                    detail="Xác thực thất bại.",
                )

        # Lấy id và role từ response
        id = verify_response.data.get("id")
        role = verify_response.data.get("role")

        # Lưu id và role vào state của request
        request.state.id = id
        request.state.role = role

    return True
    return True


# Hàm kiểm tra quyền admin
async def verify_admin(request: Request):
    return await verify_role(request, required_roles=[label.role["ADMIN"]])


# Hàm kiểm tra quyền admin
async def verify_admin(request: Request):
    return await verify_role(request, required_roles=[label.role["ADMIN"]])


# Hàm kiểm tra quyền user
async def verify_user(request: Request):
    return await verify_role(request, required_roles=[label.role["USER"]])


# Hàm kiểm tra quyền user
async def verify_user(request: Request):
    return await verify_role(request, required_roles=[label.role["USER"]])


# Hàm kiểm tra quyền admin hoặc user
async def verify_all(request: Request):
    return await verify_role(
        request, required_roles=[label.role["ADMIN"], label.role["USER"]]
    )
