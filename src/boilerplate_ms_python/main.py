import os
import sys
from concurrent import futures
from dotenv import load_dotenv

from boilerplate_ms_python.config.db_client import Base, engine
from boilerplate_ms_python.config.grpc_interceptor import (
    AuthInterceptor,
    LoggerInterceptor,
)
from boilerplate_ms_python.config.logger_config import logger
from grpc_reflection.v1alpha import reflection
from boilerplate_ms_python.config.redis_client import init_redis


load_dotenv(override=True)

proto_generated_path = os.path.join(os.path.dirname(__file__), "proto_generated")
if proto_generated_path not in sys.path:
    sys.path.insert(0, proto_generated_path)

import grpc
from boilerplate_ms_python.services.greeter_service import Greeter
from boilerplate_ms_python.proto_generated import helloworld_pb2_grpc, helloworld_pb2


def serve():
    port = os.getenv("PORT", "50051")
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=(AuthInterceptor(), LoggerInterceptor()),
    )
    """
    Import the generated _pb2_grpc files and add the service to server 
    for each .proto added
    """
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    """
    Add _pb2.DESCRIPTOR.services_by_name["NewServiceName"] for each
    .proto added for server reflection
    """

    service_names = (
        helloworld_pb2.DESCRIPTOR.services_by_name["Greeter"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logger.info(msg=f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    init_redis()
    serve()
