import pytest

from eliot.testing import swap_logger, check_for_errors, LoggedMessage
from eliot import MemoryLogger
from typing import ContextManager, Iterator
from contextlib import contextmanager


@pytest.fixture
def eliot_test_logger() -> MemoryLogger:
    return MemoryLogger()


@pytest.fixture
def eliot_capture_logging(eliot_test_logger) -> ContextManager:
    """This fixture must check...

    - You haven’t logged anything that isn’t JSON serializable.

    - There are no unexpected tracebacks, indicating a bug somewhere in your
    code.

    """
    @contextmanager
    def _capture_logging() -> Iterator[None]:
        original_logger = swap_logger(eliot_test_logger)

        try:
            yield eliot_test_logger
        finally:
            swap_logger(original_logger)
            check_for_errors(eliot_test_logger)

    return _capture_logging

@pytest.fixture
def eliot_has_message():
    def _has_message(logger, message_type, fields=None) -> bool:
        if fields is None:
            fields = {}

        messages = LoggedMessage.of_type(logger.messages, message_type)

        if not messages:
            return False

        logged_message = messages[0]

        return fields.items() <= logged_message.message.items()

    return _has_message
