from boilerplate_ms_python.proto_generated import helloworld_pb2_grpc, helloworld_pb2


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)
