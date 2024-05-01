"""This module provides high-level decorators to generate test results in the standard JUnit XML format."""

import atexit
import fnmatch
import functools
import inspect
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
    def count(cls):
        return len(cls.reporters)


class TestSuiteFactory:
    """A factory class for creating and managing JUnitTestSuite."""

    test_suites = {}

    @classmethod
    def get(cls, name, reporter=None, prettyprint=True, **kwargs):
        """Returns a JUnitTestSuite instance for the given name."""

        test_suite = cls.test_suites.get(name)

        if not test_suite:
            test_suite = JUnitTestSuite(name, **kwargs)

            reporter = ReporterFactory.get(filename=reporter, prettyprint=prettyprint)
            reporter.add_test_suite(test_suite)

            cls.test_suites[name] = test_suite

        return test_suite

    @classmethod
    def clear(cls):
        cls.test_suites.clear()

    @classmethod
    def count(cls):
        return len(cls.test_suites)


def is_test_method(name, value, pattern=None):
    """Check if a given method is a test method based on its name and value.

    Args:
        name (str): The name of the method.
        value (callable): The value of the method.
        pattern (str, optional): A wildcard pattern to match against the method name.
            Defaults to ``"test*"``. Note that matches are always performed using
            ``fnmatch.fnmatchcase()``.

    Returns:
        bool: ``True`` if the method is a test method, ``False`` otherwise.

    Examples:
        >>> is_test_method("test_example", lambda: None)
        True
        >>> is_test_method("not_a_test", lambda: None)
        False
        >>> is_test_method("t_another_example", lambda: None, pattern="t_*")
        True

    """

    if pattern is None:
        pattern = "test*"

    return inspect.isfunction(value) and fnmatch.fnmatchcase(name, pattern)


def discover(cls, test_suite_name=None, pattern=None):
    """Discover and convert test methods within a test class to JUnit test cases.

    This function iterates over the attributes of the given test class ``cls``, identifies test methods based on the
    provided ``pattern``, and converts them into JUnit test cases by wrapping them with the ``junit_test_case`` decorator.

    Args:
        cls (class): The test class containing test methods to be discovered and converted.
        test_suite_name (str, optional): The name of the test suite to which the discovered test cases belong.
            Defaults to ``None``.
        pattern (str, optional): A wildcard pattern to match against the names of test methods.
            Defaults to None, which implies matching against the default pattern ``"test*"``.

    Returns:
        None: This function modifies the test class ``cls`` in-place by replacing test methods with JUnit test cases.

    Examples:
        Consider the following test class:

        >>> class MyTestClass(unittest.TestCase):
        ...     def test_example(self):
        ...         pass
        ...     def other_method(self):
        ...         pass

        To discover and convert test methods within ``MyTestClass`` into JUnit test cases:

        >>> discover(MyTestClass, test_suite_name="MyTestSuite", pattern="test_*")

        The ``test_example`` method will be converted into a JUnit test case with the specified test suite name.
        The ``other_method`` will remain unchanged as it does not match the provided pattern.

    """

    attrs = ((attr_name, getattr(cls, attr_name)) for attr_name in dir(cls))

    for method_name, method in attrs:
        if is_test_method(method_name, method, pattern=pattern):
            setattr(cls, method_name, junit_test_case(method, test_suite=test_suite_name))


def junit_test_case(_func=None, *, test_suite=None, **kwargs):
    """Decorator to create a new JUnit test case.

    This decorator is used to wrap test methods within a test class, converting them into JUnit test cases.
    Each JUnit test case is associated with a specific test suite, which is used to categorize and organize
    test cases in test reports.

    Args:
        _func (callable, optional): The function to be decorated. Defaults to ``None``.
        test_suite (str, optional): The name of the test suite to which the test case belongs.
            If not provided, the test suite name is derived from the enclosing class name.
        **kwargs: Additional keyword arguments are ignored.

    Returns:
        callable: The decorated function.

    Examples:
        Usage as a decorator:
        >>> @junit_test_case(test_suite="MyTestSuite")
        ... def test_example():
        ...     assert True

        Usage without arguments:
        >>> @junit_test_case
        ... def test_example():
        ...     assert True

        In both cases, the ``test_example`` function will be converted into a JUnit test case associated with the
        specified test suite ``"MyTestSuite"`` or derived from the enclosing class name.

    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            suite = TestSuiteFactory.get(test_suite or func.__qualname__.rpartition(".")[0])
            test_case = suite.create_test_case(func.__name__)
            test_case.start()

            try:
                result = func(*args, **kwargs)
            except AssertionError as error:
                test_case.add_failure(message=str(error), failure_type=error.__class__.__name__)
                raise
            except Exception as error:
                test_case.add_error(message=str(error), error_type=error.__class__.__name__)
                raise
            finally:
                test_case.finish()

            return result
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def junit_test_suite(_func=None, *, name=None, reporter=None, auto_discover=False, pattern=None, **kwargs):
    """Decorator to create a new JUnit test suite.

    This decorator is used to create a new JUnit test suite, which can be associated with one or more test cases.
    The test suite may include custom settings such as the name, reporter filename, and auto-discovery of test cases.

    Args:
        _func (callable, optional): The function to be decorated. Defaults to ``None``.
        name (str, optional): The name of the test suite. If not provided, the name will default to the name of
            the decorated function.
        reporter (str, optional): The filename of the reporter to be associated with the test suite.
        auto_discover (bool, optional): If set to ``True`` and the decorated function is a class, the test suite will
            automatically discover and include test cases within the class. Defaults to ``False``.
        pattern (str, optional): A wildcard pattern to match against the names of test methods for auto-discovery.
        **kwargs: Additional keyword arguments are passed to the ``JUnitTestSuite`` to customize the test suite.

    Returns:
        callable: The decorated function.

    Examples:
        Usage as a decorator:
        >>> @junit_test_suite(name="MyTestSuite", reporter="report.xml", auto_discover=True, pattern="test_*")
        ... def my_test_suite():
        ...     pass

        In this example, a test suite named ``"MyTestSuite"`` is created with a custom reporter filename ``"report.xml"``.
        Auto-discovery is enabled, and test methods within the decorated function will be discovered based on the
        specified pattern ``"test_*"``.

    """

    def decorator(func):
        test_suite_name = name or func.__name__
        TestSuiteFactory.get(test_suite_name, reporter=reporter, **kwargs)

        if auto_discover and inspect.isclass(func):
            discover(func, test_suite_name=test_suite_name, pattern=pattern)

        return func

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def junit_reporter(_func=None, *, filename=None, prettyprint=True):
    """Decorator to create a JUnit reporter instance.

    This decorator is used to create a JUnit reporter instance, which is responsible for generating a JUnit report
    and writing it to a specified filename. The generated report can be customized with options such as pretty-printing.

    Args:
        _func (callable, optional): The function to be decorated. Defaults to ``None``.
        filename (str): The filename to write the JUnit report to.
        prettyprint (bool, optional): If set to ``True``, the generated JUnit report will be formatted for human readability
            (pretty-printed). Defaults to ``True``.

    Returns:
        callable: The decorated function.

    Examples:
        Usage as a decorator:
        >>> @junit_reporter(filename="test_report.xml", prettyprint=True)
        ... def my_test_function():
        ...     pass

        In this example, a JUnit reporter instance is created with the specified filename ``"test_report.xml"``,
        and pretty-printing is enabled. The decorated function remains unchanged.

    """

    ReporterFactory.get(filename, prettyprint=prettyprint)

    def decorator(func):
        return func

    if _func is None:
        return decorator
    else:
        return decorator(_func)
