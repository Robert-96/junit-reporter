import pytest
from junit_reporter.decorators import ReporterFactory, TestSuiteFactory, \
    junit_reporter, junit_test_case, junit_test_suite


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

    assert reporter_factory.len() == 0

    junit_reporter(to_be_decorated)

    assert reporter_factory.len() == 1


def test_test_suite_decorator(test_suite_factory):
    def to_be_decorated():
        pass

    assert test_suite_factory.len() == 0

    junit_test_suite(to_be_decorated)

    assert test_suite_factory.len() == 1


def test_test_case_decorator():
    def to_be_decorated():
        pass

    junit_test_case(to_be_decorated)
