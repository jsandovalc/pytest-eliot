"""Tests that replicate the eliot documentation:

https://eliot.readthedocs.io/en/stable/generating/testing.html

"""

import pytest
from eliot import log_message
from eliot import write_traceback


from eliot import MemoryLogger, start_action
from contextlib import AbstractContextManager

from decimal import Decimal


def test_eliot_test_logger(eliot_test_logger) -> None:
    """We get a `MemoryLogger` for testing."""
    assert isinstance(eliot_test_logger, MemoryLogger)


def test_raises(eliot_capture_logging):
    """`eliot_capture_logging` raises exceptions."""
    with pytest.raises(TypeError):
        with eliot_capture_logging():
            with start_action(action_type="insert_decimal", dec=Decimal()):
                pass

def test_message_has_fields(eliot_capture_logging):
    """Check if message has fields."""
    with eliot_capture_logging() as logger:
        log_message(message_type="user_registration", username="test", password="test_pass", age=12)

        assert len(logger.messages) == 1

        msg = logger.messages[0]

        assert {"username": "test", "password": "test_pass", "age": 12}.items() <= msg.items()


def test_flush_tracebacks(eliot_capture_logging):
    with eliot_capture_logging() as logger:
        with start_action(action_type="exception"):
            try:
                raise OSError
            except:
                write_traceback()

            messages = logger.flush_tracebacks(OSError)

            assert len(messages) == 1


def test_has_message(eliot_capture_logging, eliot_has_message):
    with eliot_capture_logging() as logger:
        log_message(message_type="user_registration", username="test", password="test_pass", age=12)

        assert eliot_has_message(logger, message_type="user_registration", fields={"username": "test", "password": "test_pass", "age": 12})


def test_failed_message():
    pass

def test_has_action(eliot_capture_loggin, eliot_has_action):
    pass
