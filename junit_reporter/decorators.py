"""This module provides high-level decorators to generate test results in the standard JUnit XML format."""

import atexit
import functools
import logging

from .xml import JUnitReporter, JUnitTestSuite

logger = logging.getLogger(__name__)


class ReporterFactory:
    """A factory class for creating and managing JUnitReporters."""

    reporters = {}

    @classmethod
    def get(cls, filename=None, prettyprint=True):
        """Returns a JUnitReporter instance for the given filename."""

        if not filename:
            filename = "report.xml"

        reporter = cls.reporters.get(filename)

        if not reporter:
            logger.debug("Creating a new JUnitReporter instance for {!r}.".format(filename))

            reporter = JUnitReporter()
            cls.reporters[filename] = reporter

            atexit.register(reporter.write, filename=filename, prettyprint=prettyprint)

        return reporter

    @classmethod
    def clear(cls):
        cls.reporters.clear()

    @classmethod
    def len(cls):
        return len(cls.reporters)


class TestSuiteFactory:
    """A factory class for creating and managing JUnitTestSuite."""

    test_suites = {}

    @classmethod
    def get(cls, name, reporter=None, **kwargs):
        """Returns a JUnitTestSuite instance for the given name."""

        test_suite = cls.test_suites.get(name)

        if not test_suite:
            test_suite = JUnitTestSuite(name, **kwargs)

            reporter = ReporterFactory.get(filename=reporter)
            reporter.add_test_suite(test_suite)

            cls.test_suites[name] = test_suite

        return test_suite

    @classmethod
    def clear(cls):
        cls.test_suites.clear()

    @classmethod
    def len(cls):
        return len(cls.test_suites)


def junit_test_case(*args, test_suite=None, **kwargs):
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
                test_case.add_failure(message=str(error), error_type=error.__class__.__name__)
                raise
            except Exception as error:
                test_case.add_error(message=str(error), error_type=error.__class__.__name__)
                raise
            finally:
                test_case.finish()

            return result
        return wrapper
    return decorator


def junit_test_suite(_func=None, *, name=None, reporter=None, **kwargs):
    """Create a new test suite.

    Args:
        name (:obj:`string`, optional): The name of the tests case. If not set will use the name of the decorated
            method/function.
        reporter: The filename of the reporter.

    """

    def decorator(func):
        test_suite_name = name or func.__name__
        TestSuiteFactory.get(test_suite_name, reporter=reporter, **kwargs)

        return func

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def junit_reporter(_func=None, *, filename=None, prettyprint=True):
    """Create a JunitReporter instance.

    Args:
        filename (:obj:`str`): The filename to write the JUnit report to.
        prettyprint (:obj:`bool`, optional): If set to true will generate a "pretty" version of the JUnit report.
            Defaults to ``True``.

    """

    ReporterFactory.get(filename, prettyprint=prettyprint)

    def decorator(func):
        return func

    if _func is None:
        return decorator
    else:
        return decorator(_func)
