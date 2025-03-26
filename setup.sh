python -m grpc_tools.protoc \
  -I./src/boilerplate_ms_python/protos \
  --python_out=./src/boilerplate_ms_python/proto_generated \
  --pyi_out=./src/boilerplate_ms_python/proto_generated \
  --grpc_python_out=./src/boilerplate_ms_python/proto_generated \
  ./src/boilerplate_ms_python/protos/*.proto