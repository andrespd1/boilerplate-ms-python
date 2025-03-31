import pytest
import grpc
from unittest.mock import Mock, patch, MagicMock
from boilerplate_ms_python.services.greeter_service import Greeter
from boilerplate_ms_python.proto_generated.helloworld_pb2 import (
    HelloRequest,
    HelloReply,
)


@pytest.fixture
def greeter_service():
    """Fixture that returns a fresh Greeter instance for each test."""
    return Greeter()


@pytest.fixture
def mock_stub():
    """
    Fixture that returns a mock object simulating an entity with a `.name` attribute.
    """
    stub = Mock()
    stub.configure_mock(name="test_stub")
    return stub


def test_say_hello_with_stub(greeter_service, mock_stub, mocker):
    """Repository returns a stub => the final message shows the stub's name."""
    request = HelloRequest(name="Test User")
    context = Mock(spec=grpc.ServicerContext)

    # Patch `get_cache` to simulate cache miss => return False
    mocker.patch(
        "boilerplate_ms_python.config.redis_client.get_cache", return_value=False
    )
    # Patch `set_cache` so it just returns what the function provides
    mocker.patch(
        "boilerplate_ms_python.config.redis_client.set_cache",
        side_effect=lambda k, v, ttl: v,
    )

    # Also patch the repository call
    mocker.patch.object(
        greeter_service.stub_repository, "get_first_stub", return_value=mock_stub
    )

    response = greeter_service.SayHello(request, context)
    assert response.message == "Hello, Test User! Stub name: test_stub"


def test_say_hello_without_stub(greeter_service, mocker):
    """Repository returns None => final message has 'Stub name: None'."""
    request = HelloRequest(name="Test User")
    context = Mock(spec=grpc.ServicerContext)

    # Cache miss again
    mocker.patch(
        "boilerplate_ms_python.config.redis_client.get_cache", return_value=False
    )
    mocker.patch(
        "boilerplate_ms_python.config.redis_client.set_cache",
        side_effect=lambda k, v, ttl: v,
    )

    mocker.patch.object(
        greeter_service.stub_repository, "get_first_stub", return_value=None
    )

    response = greeter_service.SayHello(request, context)
    assert response.message == "Hello, Test User! Stub name: None"


def test_say_hello_empty_name(greeter_service, mock_stub, mocker):
    """If request.name is empty, the final message includes 'Hello, !'."""
    request = HelloRequest(name="")
    context = Mock(spec=grpc.ServicerContext)

    mocker.patch(
        "boilerplate_ms_python.config.redis_client.get_cache", return_value=False
    )
    mocker.patch(
        "boilerplate_ms_python.config.redis_client.set_cache",
        side_effect=lambda k, v, ttl: v,
    )

    mocker.patch.object(
        greeter_service.stub_repository, "get_first_stub", return_value=mock_stub
    )

    response = greeter_service.SayHello(request, context)
    assert response.message == "Hello, ! Stub name: test_stub"


def test_say_hello_cache_hit(greeter_service, mocker):
    """
    If Redis has a cached HelloReply, we should NOT call the repository.
    """
    request = HelloRequest(name="Cached User")
    context = Mock(spec=grpc.ServicerContext)

    # Mock a cached HelloReply
    cached_reply = HelloReply(message="Hello, Cached User! Stub name: from_cache")

    # `get_cache` returns the cached object => skipping repository call
    mocker.patch(
        "boilerplate_ms_python.config.redis_client.get_cache", return_value=cached_reply
    )

    # `set_cache` should NOT be called if we already have a cache hit, but we can patch it to confirm usage
    mock_set_cache = mocker.patch("boilerplate_ms_python.config.redis_client.set_cache")

    # Also mock the repository to ensure it's NOT called
    mock_repo = mocker.patch.object(greeter_service.stub_repository, "get_first_stub")

    response = greeter_service.SayHello(request, context)
    assert response.message == "Hello, Cached User! Stub name: from_cache"

    # set_cache was never called on a true cache hit
    mock_set_cache.assert_not_called()

    # The repository was not called
    mock_repo.assert_not_called()


def test_say_hello_cache_miss_leads_to_repo_call(greeter_service, mock_stub, mocker):
    """
    If `get_cache` returns False => it's a cache miss.
    => The code calls the repository, then calls `set_cache`.
    """
    request = HelloRequest(name="Missed User")
    context = Mock(spec=grpc.ServicerContext)

    # Cache miss => get_cache returns False
    mocker.patch(
        "boilerplate_ms_python.config.redis_client.get_cache", return_value=False
    )

    # We'll let set_cache just pass the computed value
    mock_set_cache = mocker.patch(
        "boilerplate_ms_python.config.redis_client.set_cache",
        side_effect=lambda k, v, ttl: v,
    )

    # Repo returns our mock stub
    mocker.patch.object(
        greeter_service.stub_repository, "get_first_stub", return_value=mock_stub
    )

    response = greeter_service.SayHello(request, context)
    assert response.message == "Hello, Missed User! Stub name: test_stub"

    # set_cache should have been called exactly once with the newly computed HelloReply
    mock_set_cache.assert_called_once()
