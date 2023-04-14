import datetime

import pytest
from junit_reporter import JUnitTestCase


@pytest.mark.parametrize("enabled", [True, False])
def test_is_enabled(enabled):
    test_case = JUnitTestCase("Test Case #1", enabled=enabled)
    assert test_case.is_enabled == enabled


@pytest.mark.parametrize(
    "errors, expected", [
        ([], False),
        ([{}], False),
        ([{"message": "Error."}], True),
        ([{"output": "Error."}], True),
        ([{"message": "Error."}, {"output": "Error."}], True),
    ]
)
def test_is_error(errors, expected):
    test_case = JUnitTestCase("Test Case #1")

    for error in errors:
        test_case.add_error(**error)

    assert test_case.is_error == expected


@pytest.mark.parametrize(
    "failures, expected", [
        ([], False),
        ([{}], False),
        ([{"message": "Fail."}], True),
        ([{"output": "Fail."}], True),
        ([{"message": "Fail."}, {"output": "Fail."}], True),
    ]
)
def test_is_failure(failures, expected):
    test_case = JUnitTestCase("Test Case #1")

    for failure in failures:
        test_case.add_failure(**failure)

    assert test_case.is_failure == expected


@pytest.mark.parametrize(
    "skips, expected", [
        ([], False),
        ([{"message": "Skip."}], True),
        ([{"output": "Skip."}], True),
        ([{"message": "Skip."}, {"output": "Skip."}], True),
    ]
)
def test_is_skipped(skips, expected):
    test_case = JUnitTestCase("Test Case #1")

    for skip in skips:
        test_case.add_skipped(**skip)

    assert test_case.is_skipped == expected


def test_empty_attributes():
    test_case = JUnitTestCase("Test Case #1")
    expected = {
        "name": "Test Case #1"
    }

    assert test_case.attributes == expected


def test_attributes():
    test_case = JUnitTestCase(
        "Test Case #1",
        status="Failed",
        classname="TestModel",
        filename="test.py",
        line=24,
        assertions=3,
        elapsed_seconds=10,
        timestamp=datetime.datetime(2020, 8, 24)
    )

    expected = {
        "name": "Test Case #1",
        "status": "Failed",
        "classname": "TestModel",
        "file": "test.py",
        "line": "24",
        "assertions": "3",
        "time": "10",
        "timestamp": "2020-08-24 00:00:00"
    }

    assert test_case.attributes == expected
