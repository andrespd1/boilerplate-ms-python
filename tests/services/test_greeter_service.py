import pytest
from unittest.mock import Mock
from boilerplate_ms_python.proto_generated import helloworld_pb2
from boilerplate_ms_python.services.greeter_service import Greeter


@pytest.fixture
def greeter_service():
    """Fixture that returns a fresh Greeter instance for each test."""
    return Greeter()


@pytest.fixture
def mock_stub():
    """
    Fixture that returns a mock object simulating an entity with a .name attribute.
    We override the internal Mock 'name' attribute by using configure_mock.
    """
    stub = Mock()
    stub.configure_mock(name="test_stub")
    return stub


def test_say_hello_with_stub(greeter_service, mock_stub, mocker):
    """Test that Greeter says hello properly when a stub is found."""
    request = helloworld_pb2.HelloRequest(name="Test User")
    context = Mock()

    # Patch 'get_first_stub' so it returns 'mock_stub'
    mocker.patch.object(
        greeter_service.stub_repository, "get_first_stub", return_value=mock_stub
    )

    # Act
    response = greeter_service.SayHello(request, context)

    # Assert
    assert response.message == "Hello, Test User! Stub name: test_stub"


def test_say_hello_without_stub(greeter_service, mocker):
    """Test behavior when no stub is returned."""
    request = helloworld_pb2.HelloRequest(name="Test User")
    context = Mock()

    mocker.patch.object(
        greeter_service.stub_repository, "get_first_stub", return_value=None
    )
    response = greeter_service.SayHello(request, context)

    assert response.message == "Hello, Test User! Stub name: None"


def test_say_hello_empty_name(greeter_service, mock_stub, mocker):
    """Test behavior when user name is empty."""
    request = helloworld_pb2.HelloRequest(name="")
    context = Mock()

    mocker.patch.object(
        greeter_service.stub_repository, "get_first_stub", return_value=mock_stub
    )
    response = greeter_service.SayHello(request, context)

    assert response.message == "Hello, ! Stub name: test_stub"
