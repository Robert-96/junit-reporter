import datetime
from unittest.mock import MagicMock

import pytest

MOCK_DATETIME_START = datetime.datetime(2020, 8, 24, 19, 19, 19)
MOCK_DATETIME_END = MOCK_DATETIME_START + datetime.timedelta(seconds=7)


def assert_not_called_with(mock, *args, **kwargs):
    """
    Assert that a mock object was not called with the specified arguments.

    Args:
        mock (MagicMock): The mock object to check.
        *args: Positional arguments to check against.
        **kwargs: Keyword arguments to check against.

    Raises:
        AssertionError: If the mock was called with the specified arguments.
    """

    with pytest.raises(AssertionError):
        mock.assert_any_call(*args, **kwargs)


@pytest.fixture()
def mock_datetime_now(monkeypatch):
    """A pytest fixture that mocks the `datetime.datetime.now` method to return predefined values.
    This fixture uses `monkeypatch` to temporarily replace the `datetime.datetime` class with a mock object.
    The mock object is configured to return predefined values (`MOCK_DATETIME_START` and `MOCK_DATETIME_END`) when `now()` is called.

    Args:
        monkeypatch (pytest.MonkeyPatch): A pytest fixture used to safely modify or replace attributes.

    Yields:
        None: This is a generator-based fixture that restores the original `datetime.datetime` after use.

    Example:
        def test_example(mock_datetime_now):
            assert datetime.datetime.now() == MOCK_DATETIME_START
            assert datetime.datetime.now() == MOCK_DATETIME_END
    """

    datetime_mock = MagicMock()
    datetime_mock.now.side_effect = [MOCK_DATETIME_START, MOCK_DATETIME_END]

    monkeypatch.setattr(datetime, "datetime", datetime_mock)
    yield
    monkeypatch.delattr(datetime, "datetime")
