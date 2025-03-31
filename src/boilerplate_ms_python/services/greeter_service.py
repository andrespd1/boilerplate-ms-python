import grpc
from boilerplate_ms_python.config.redis_client import get_and_set_cache
from boilerplate_ms_python.proto_generated import helloworld_pb2_grpc, helloworld_pb2
from boilerplate_ms_python.repositories.stub_repository import StubRepository


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    stub_repository = StubRepository()

    def SayHello(
        self, request: helloworld_pb2.HelloRequest, context: grpc.ServicerContext
    ):
        def _handle():
            stub_result = self.stub_repository.get_first_stub()
            stub_name = getattr(stub_result, "name", "None")
            return helloworld_pb2.HelloReply(
                message=f"Hello, {request.name}! Stub name: {stub_name}"
            )

        return get_and_set_cache(f"say-hello_name:{request.name}", _handle)
