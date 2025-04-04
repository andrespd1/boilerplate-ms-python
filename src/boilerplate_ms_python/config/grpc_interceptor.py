import grpc

from boilerplate_ms_python.config.logger_config import logger


def _unary_unary_rpc_terminator(code, details):
    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


class AuthInterceptor(grpc.ServerInterceptor):
    _header = "authentication"
    _terminator = _unary_unary_rpc_terminator(401, "Unauthorized access")

    def intercept_service(self, continuation, handler_call_details):
        # TODO: Implement auth method
        return continuation(handler_call_details)
        # return self._terminator


class LoggerInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        handler = continuation(handler_call_details)
        if handler is None:
            return None

        if handler.unary_unary:

            def logger_handler(request, context):
                logger.info(f"Received request at {handler_call_details.method}: {request}")
                response = handler.unary_unary(request, context)
                logger.info(f"Sending response for {handler_call_details.method}: {response}")
                return response

            return grpc.unary_unary_rpc_method_handler(
                logger_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        return handler
