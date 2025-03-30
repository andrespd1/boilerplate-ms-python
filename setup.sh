# Usage:
#   ./proto_generator.sh init
#   ./proto_generator.sh generate-proto
#
# Description:
#   - "generate-proto": runs the protoc command to generate Python gRPC files 
#                       from your .proto definitions.
#   - "init": runs "poetry install" and then automatically calls "generate-proto".

set -e

case "$1" in
  generate-proto)
    echo "Generating gRPC Python files..."
    python -m grpc_tools.protoc \
      -I./src/boilerplate_ms_python/protos \
      --python_out=./src/boilerplate_ms_python/proto_generated \
      --pyi_out=./src/boilerplate_ms_python/proto_generated \
      --grpc_python_out=./src/boilerplate_ms_python/proto_generated \
      ./src/boilerplate_ms_python/protos/*.proto
    echo "Generation complete!"
    ;;
  init)
    echo "Running poetry install..."
    poetry install
    echo "Running proto generation..."
    # Call this same script again with generate-proto
    "$0" generate-proto
    ;;
  *)
    echo "Usage: $0 [init | generate-proto]"
    exit 1
    ;;
esac
