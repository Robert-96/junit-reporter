"""High level decorators for generating test results in the standard JUnit XML format for use with Jenkins and other
build integration servers.

"""

import atexit
import logging
import functools

from .xml import TestCase, TestSuite, JUnitReporter


logger = logging.getLogger(__name__)


class ReporterFactory:
    reporters = {}

    @classmethod
    def get(cls, filename=None, prettyprint=True):
        if not filename:
            filename = "report.xml"

        reporter = cls.reporters.get(filename, None)

        if not reporter:
            reporter = JUnitReporter()
            cls.reporters[filename] = reporter

            atexit.register(reporter.write, filename=filename, prettyprint=prettyprint)

        return reporter


class TestSuiteFactory:
    test_suites = {}

    @classmethod
    def get(cls, name, **kwargs):
        test_suite = cls.test_suites.get(name, None)

        if not test_suite:
            test_suite = TestSuite(name, **kwargs)
            cls.test_suites[name] = test_suite

        return test_suite


def test_case(*args, test_suite=None, **kwargs):
    """Create a new test case.

    Args:
        test_suite: The name of the test suite.

    """

    test_suite = TestSuiteFactory.get(test_suite)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            test_case = test_suite.create_test_case(func.__name__)
            test_case.start()

            try:
                result = func(*args, **kwargs)
            except AssertionError as error:
                test_case.finish()
                test_case.add_failure(message=str(error), error_type=error.__class__.__name__)
                raise
            except Exception as error:
                test_case.finish()
                test_case.add_error(message=str(error), error_type=error.__class__.__name__)
                raise

            test_case.finish()

            return result
        return wrapper
    return decorator


def test_suite(name=None, reporter=None, **kwargs):
    """Create a new test suite.

    Args:
        name (:obj:`string`, optional): The name of the tests case. If not set will use the name of the decorated
            method/function.
        reporter: The filename of the reporter.

    """

    reporter = ReporterFactory.get(reporter)

    def decorator(func):
        test_suite_name = name or func.__name__
        test_suite = TestSuiteFactory.get(test_suite_name, **kwargs)
        reporter.add_test_suite(test_suite)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            return value
        return wrapper
    return decorator


def junit_reporter(filename, prettyprint=True):
    """Create a JunitReporter instance.

    Args:
        filename (:obj:`str`): The filename to write the JUnit report to.
        prettyprint (:obj:`bool`, optional): If set to true will generate a "pretty" version of the JUnit report.
            Defaults to ``True``.

    """

    reporter = ReporterFactory.get(filename, prettyprint=prettyprint)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
