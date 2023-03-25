"""This module provides high-level decorators to generate test results in the standard JUnit XML format.

"""

import atexit
import functools
import logging

from .xml import JUnitReporter, TestSuite

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

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            suite = TestSuiteFactory.get(test_suite)
            test_case = suite.create_test_case(func.__name__)
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

    def decorator(func):
        test_suite_name = name or func.__name__
        test_suite = TestSuiteFactory.get(test_suite_name, **kwargs)
        reporter2 = ReporterFactory.get(reporter)
        reporter2.add_test_suite(test_suite)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result
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
