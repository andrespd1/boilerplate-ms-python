#!/bin/bash
# Usage:
#   ./proto_generator.sh init-docker
#   ./proto_generator.sh proto
#   ./proto_generator.sh init
#
# Description:
#   - "proto": runs the protoc command to generate Python gRPC files 
#                       from your .proto definitions.
#   - "init-docker": runs "poetry install" and then automatically calls "proto".
#   - "init": runs "poetry install", activates the Poetry venv (handles Linux/Mac/Windows),
#             then runs proto generation, pre-commit install, and pre-commit install --hook-type commit-msg.

set -e

# Function to activate the poetry virtual environment across platforms.
activate_venv() {
  # For Linux/macOS:
  if [ -f ".venv/bin/activate" ]; then
    echo "Activating virtual environment (.venv/bin/activate)..."
    # shellcheck source=/dev/null
    source .venv/bin/activate
  # For Windows:
  elif [ -f ".venv/Scripts/activate" ]; then
    echo "Activating virtual environment (.venv/Scripts/activate)..."
    # shellcheck source=/dev/null
    source .venv/Scripts/activate
  else
    echo "Virtual environment not found. Please ensure Poetry is configured with in-project venv (virtualenvs.in-project true)."
    exit 1
  fi
}

case "$1" in
  proto)
    echo "Generating gRPC Python files..."
    python -m grpc_tools.protoc \
      -I./src/boilerplate_ms_python/protos \
      --python_out=./src/boilerplate_ms_python/proto_generated \
      --pyi_out=./src/boilerplate_ms_python/proto_generated \
      --grpc_python_out=./src/boilerplate_ms_python/proto_generated \
      ./src/boilerplate_ms_python/protos/*.proto
    echo "Generation complete!"
    ;;
  init-docker)
    echo "Running poetry install (Docker mode)..."
    poetry install --no-root --no-interaction
    echo "Running proto generation..."
    "$0" proto
    ;;
  init)
    echo "Running poetry install (local mode)..."
    poetry install
    echo "Activating the virtual environment..."
    activate_venv
    echo "Running proto generation..."
    "$0" proto
    echo "Installing pre-commit hooks..."
    pre-commit install
    echo "Installing commit-msg hook..."
    pre-commit install --hook-type commit-msg
    echo "Local initialization complete!"
    ;;
  *)
    echo "Usage: $0 [init-docker | proto | init]"
    exit 1
    ;;
esac
