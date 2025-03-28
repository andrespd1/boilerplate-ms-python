from boilerplate_ms_python.proto_generated import helloworld_pb2_grpc, helloworld_pb2
from boilerplate_ms_python.repositories.stub_repository import StubRepository


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    stub_repository = StubRepository()

    def SayHello(self, request, context):
        stub_result = self.stub_repository.get_first_stub()
        stub_name = getattr(stub_result, "name", "None")
        return helloworld_pb2.HelloReply(
            message=f"Hello, {request.name}! Stub name: {stub_name}"
        )
