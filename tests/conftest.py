import datetime
from unittest.mock import MagicMock, patch

import pytest

FAKE_NOW = datetime.datetime(2020, 8, 24, 19, 19, 19)
FAKE_NOW_2 = FAKE_NOW + datetime.timedelta(seconds=7)


@pytest.fixture()
def mock_datetime_now(monkeypatch):
    datetime_mock = MagicMock()
    datetime_mock.now.side_effect = [FAKE_NOW, FAKE_NOW_2]

    monkeypatch.setattr(datetime, "datetime", datetime_mock)
    yield
    monkeypatch.delattr(datetime, "datetime")
