import unittest.mock as mock

import pytest
from junit_reporter.decorators import (
    ReporterFactory,
    TestSuiteFactory,
    discover,
    is_test_method,
    junit_reporter,
    junit_test_case,
    junit_test_suite
)

from .conftest import assert_not_called_with


class MockTestClass:

    def test_example(self):
        pass

    def other_method(self):
        pass


@pytest.mark.parametrize("name, value, pattern, expected", [
    # Test cases where the method name matches the pattern
    ("test_example", lambda: None, None, True),
    ("test_case", lambda: None, "test_*", True),
    ("test_another_example", lambda: None, "test_*", True),
    ("test_case", lambda: None, None, True),  # Default pattern "test*"
    # Test cases where the method name does not match the pattern
    ("not_a_test", lambda: None, None, False),
    ("example", lambda: None, "test_*", False),
    ("not_a_test", lambda: None, "test_*", False),
    ("example", lambda: None, None, False),  # Default pattern "test*"
    # Test case with non-function value
    ("test_example", "not_a_function", None, False),
])
def test_is_test_method(name, value, pattern, expected):
    assert is_test_method(name, value, pattern) == expected


@pytest.mark.parametrize("cls, test_suite_name, pattern, expected_methods", [
    (
        MockTestClass,
        "MyTestSuite",
        "test_*",
        {"test_example": (True, MockTestClass.test_example), "other_method": (False, MockTestClass.other_method)}
    ),
    (
        MockTestClass,
        "MyTestSuite",
        "other_*",
        {"test_example": (False, MockTestClass.test_example), "other_method": (True, MockTestClass.other_method)}
    ),
    (
        MockTestClass,
        "MyTestSuite",
        "notfound",
        {"test_example": (False, MockTestClass.test_example), "other_method": (False, MockTestClass.other_method)}
    ),
    (
        MockTestClass,
        "MyTestSuite",
        None,
        {"test_example": (True, MockTestClass.test_example), "other_method": (False, MockTestClass.other_method)}
    ),
])
def test_discover(cls, test_suite_name, pattern, expected_methods):
    def mock_side_effect(method, **kwargs):
        return method

    with mock.patch("junit_reporter.decorators.junit_test_case", side_effect=mock_side_effect) as mock_junit_test_case:
        discover(cls, test_suite_name=test_suite_name, pattern=pattern)

        for _, (should_be_called, method) in expected_methods.items():
            if should_be_called:
                mock_junit_test_case.assert_any_call(method, test_suite=test_suite_name)
            else:
                assert_not_called_with(mock_junit_test_case, method, test_suite=test_suite_name)


@pytest.fixture
def reporter_factory():
    ReporterFactory.clear()

    yield ReporterFactory

    ReporterFactory.clear()


@pytest.fixture
def test_suite_factory():
    TestSuiteFactory.clear()

    yield TestSuiteFactory

    TestSuiteFactory.clear()


def test_junit_reporter_decorator(reporter_factory):
    def to_be_decorated():
        pass

    assert reporter_factory.count() == 0

    junit_reporter(to_be_decorated)

    assert reporter_factory.count() == 1


def test_test_suite_decorator(test_suite_factory):
    def to_be_decorated():
        pass

    assert test_suite_factory.count() == 0

    junit_test_suite(to_be_decorated)

    assert test_suite_factory.count() == 1


def test_test_case_decorator():
    def to_be_decorated():
        pass

    junit_test_case(to_be_decorated)
