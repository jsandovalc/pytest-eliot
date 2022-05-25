# Pytest-eliot

Fixtures to use eliot from pytest.

# Testing your logging
pytest-eliot allows using eliot with pytest. The usage is kind of different and
adapted to pytest style.

https://eliot.readthedocs.io/en/stable/generating/testing.html

## Linting your logs
pytest-eliot provides a fixture that can be used as a context manager. The eliot
capture_logging is provided as the fixture eliot_capture_logging.

The context manager will ensure that:

1. You haven't logged anything that isn't JSON serializable.
2. There are no unexpected tracebacks, indicating a bug somewhere in your code.

```python
def test_mytest(eliot_capture_logging):
    with eliot_capture_logging():
        call_my_function()
```

## Making assertions about the logs

You can also ensure the correct messages were logged.

```python
from eliot import log_message

class UserRegistration(object):

    def __init__(self):
        self.db = {}

    def register(self, username, password, age):
        self.db[username] = (password, age)
        log_message(message_type="user_registration",
                    username=username, password=password,
                    age=age)

```

Here's how we'd test it:

```python
from myapp.registration import UserRegistration

def test_registration(eliot_capture_logging):
    registry = UserRegistration()

    with eliot_capture_logging() as logger:
        registry.register("john", "password", 12)

        msg = logger.messages[0]

        fields = {"username": "john",
                  "password": "password",
                  "age": 12}

        assert fields.items() <= msg.items()  # Fields items is a subset of msg items.

    assert registry.db["john"] == ("password", 12)

```

## Testing tracebakcs
Eliot provides utilities for making assertions about the structure of individual
messages and actions. The simplest method is using the assertHasMessage utility
function which asserts that a message of a given message type has the given
fields:

```python
def test_badpath(eliot_capture_logging):
    mything = MyThing()

    with eliot_capture_logging() as logger:
        mything.load("/nonexistant/path")

        messages = logger.flush_tracebacks(OSError)
        assert len(messages) == 1
```

## Testing Message and Action Structure

`pytest-eliot` provides utilities for making assertions about the structure of
individual messages and actions. The simplest method is using the
`eliot_has_message` utility function which asserts that a message of a given
message type has the given fields:

``` python
def test_registration(eliot_capture_logging, eliot_has_message):
    with eliot_capture_logging() as logger:
        registry = UserRegistration()
        registry.register("john", "password", 12)

        assert eliot_has_message(
            logger, message_type="user_registration",
            fields={
                "username": "john",
                "password:" "password",
                "age": 12
            }
        )
```

## Custom JSON encoding

## Custom testing setup

Must wrap all low level functions here as fixtures.
