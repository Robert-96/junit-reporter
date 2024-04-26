"""This module includes low-level classes that can be used to create test results in the standard JUnit XML format,
making it compatible with Jenkins and other build integration servers.

"""

import datetime
import logging
import re
import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET
from collections import defaultdict

logger = logging.getLogger(__name__)


def xml_safe(value):
    """Replaces invalid `XML characters`_ with '?'.

    .. _XML characters:
       https://www.w3.org/TR/xml11/#charsets

    """

    # The characters defined in the following ranges are discouraged.
    # They are either control characters or permanently undefined Unicode characters:
    illegal_characters = [
        (0x00, 0x08),
        (0x0B, 0x1F),
        (0x7F, 0x84),
        (0x86, 0x9F),
        (0xD800, 0xDFFF),
        (0xFDD0, 0xFDDF),
        (0xFFFE, 0xFFFF),
        (0x1FFFE, 0x1FFFF),
        (0x2FFFE, 0x2FFFF),
        (0x3FFFE, 0x3FFFF),
        (0x4FFFE, 0x4FFFF),
        (0x5FFFE, 0x5FFFF),
        (0x6FFFE, 0x6FFFF),
        (0x7FFFE, 0x7FFFF),
        (0x8FFFE, 0x8FFFF),
        (0x9FFFE, 0x9FFFF),
        (0xAFFFE, 0xAFFFF),
        (0xBFFFE, 0xBFFFF),
        (0xCFFFE, 0xCFFFF),
        (0xDFFFE, 0xDFFFF),
        (0xEFFFE, 0xEFFFF),
        (0xFFFFE, 0xFFFFF),
        (0x10FFFE, 0x10FFFF),
    ]

    illegal_ranges = [
        "{}-{}".format(chr(low), chr(high)) for (low, high) in illegal_characters if low < sys.maxunicode
    ]

    illegal_regex = re.compile("[{}]".format("".join(illegal_ranges)))
    return illegal_regex.sub("?", value)


def generate_error_xml(message=None, output=None, type=None):
    """Generates the error XML."""

    attributes = {"type": "error"}

    if message:
        attributes["message"] = str(message)

    if type:
        attributes["type"] = str(type)

    error_element = ET.Element("error", attributes)

    if output:
        error_element.text = str(output)

    return error_element


def generate_failure_xml(message=None, output=None, type=None):
    """Generates the failure XML."""

    attributes = {"type": "failure"}

    if message:
        attributes["message"] = str(message)

    if type:
        attributes["type"] = str(type)

    failure_element = ET.Element("failure", attributes)

    if output:
        failure_element.text = str(output)

    return failure_element


def generate_skipped_xml(message=None, output=None):
    """Generates the skipped XML."""

    attributes = {"type": "skipped"}

    if message:
        attributes["message"] = str(message)

    skipped_element = ET.Element("skipped", attributes)

    if output:
        skipped_element.text = str(output)

    return skipped_element


def generate_properties_xml(properties):
    """Generates the properties XML."""

    properties_element = ET.Element("properties")

    for key, value in properties.items():
        attributes = {
            "name": str(key),
            "value": str(value)
        }

        ET.SubElement(properties_element, "property", attributes)

    return properties_element


def generate_stdout_xml(stdout):
    """Generates the stdout XML."""

    stdout_element = ET.Element("system-out")
    stdout_element.text = str(stdout)

    return stdout_element


def generate_stderr_xml(stderr):
    """Generates the stderr XML."""

    stderr_element = ET.Element("system-err")
    stderr_element.text = str(stderr)

    return stderr_element


class JUnitTestCase:
    """This class is designed to store and manage information related to the execution of a single test case.

    Args:
        name (:obj:`str`): The display name of the test case.
        classname (:obj:`str`): The full name of the class.
        status (:obj:`str`): The status of the test case.
        category (:obj:`str`): The category of the test case.
        stdout (:obj:`str`): The data written to ``stdout`` during the test execution.
        stderr (:obj:`str`): The data written to ``stderr`` during the test execution.
        assertions (:obj:`int`): The total number of asserts run in the test cases.
        timestamp (:obj:`str`): The time when the test case execution started.
        elapsed_seconds (:obj:`float`, :obj:`int`): The time, in fractional seconds, spent running the tests.
        filename (:obj:`str`): The full file name of the test case.
        line (:obj:`int`): The line number of the test case.
        log (:obj:`str`): The log of the test case.
        url (:obj:`str`): The url of the test case.
        enabled (:obj:`bool`): If set to ``False`` mark the test case as disabled.
        allow_multiple_subelements (:obj:`bool`): If set to ``True`` will allow a test cases to have multiple errors,
            failures or skips. Defaults to ``False``.

    """

    def __init__(self, name, classname=None, stdout=None, stderr=None, assertions=None, timestamp=None,
                 elapsed_seconds=None, status=None, category=None, filename=None, line=None, log=None, url=None,
                 enabled=True, allow_multiple_subelements=False):

        self.name = name
        self.classname = classname

        self.stdout = stdout
        self.stderr = stderr

        self.timestamp = timestamp
        self.elapsed_seconds = elapsed_seconds

        self.status = status
        self.category = category

        self.filename = filename
        self.line = line
        self.log = log
        self.url = url

        self.assertions = assertions

        self.enabled = enabled
        self._errors = []
        self._failures = []
        self._skipped = []

        self.allow_multiple_subelements = allow_multiple_subelements

    def __repr__(self):
        return ""

    @property
    def is_enabled(self):
        """Returns ``True`` if this test case is enabled."""

        return self.enabled

    @property
    def errors(self):
        """The total number of errors."""

        return sum(1 for error in self._errors if error["message"] or error["output"])

    @property
    def is_error(self):
        """Returns ``True`` if this test case is an error."""

        return self.errors > 0

    @property
    def failures(self):
        """The total number of failures."""

        return sum(1 for failure in self._failures if failure["message"] or failure["output"])

    @property
    def is_failure(self):
        """Returns ``True`` if this test case is a failure."""

        return self.failures > 0

    @property
    def skipped(self):
        """The total number of skips."""

        return len(self._skipped)

    @property
    def is_skipped(self):
        """Returns ``True`` if this test case has been skipped."""

        return self.skipped > 0

    @property
    def attributes(self):
        attributes = {
            "name": str(self.name)
        }

        if self.assertions:
            attributes["assertions"] = str(self.assertions)
        if self.elapsed_seconds:
            attributes["time"] = str(self.elapsed_seconds)
        if self.timestamp:
            attributes["timestamp"] = str(self.timestamp)
        if self.classname:
            attributes["classname"] = str(self.classname)
        if self.status:
            attributes["status"] = str(self.status)
        if self.category:
            attributes["class"] = str(self.category)
        if self.filename:
            attributes["file"] = str(self.filename)
        if self.line:
            attributes["line"] = str(self.line)
        if self.log:
            attributes["log"] = str(self.log)
        if self.url:
            attributes["url"] = str(self.url)

        return attributes

    def _xml(self):
        """Generates the test case XML."""

        xml_element = ET.Element("testcase", self.attributes)

        for error in self._errors:
            xml_element.append(generate_error_xml(**error))

        for failure in self._failures:
            xml_element.append(generate_failure_xml(**failure))

        for skipped in self._skipped:
            xml_element.append(generate_skipped_xml(**skipped))

        if self.stdout:
            xml_element.append(generate_stdout_xml(self.stdout))

        if self.stderr:
            xml_element.append(generate_stderr_xml(self.stderr))

        return xml_element

    def start(self):
        """Set the start timestamps."""

        self.timestamp = datetime.datetime.now()

    def finish(self):
        """Set the elapsed seconds based on the start timestamp."""

        if not self.timestamp:
            return

        delta = datetime.datetime.now() - self.timestamp
        self.elapsed_seconds = delta.total_seconds()

    def add_error(self, message=None, output=None, error_type=None):
        """Adds an error to the test case. Errors indicates that the test errored. An errored test had an unanticipated problem.
        For example an unchecked throwable (exception), crash or a problem with the implementation of the test.

        Args:
            message (:obj:`str`): The error message.
            output (:obj:`str`): The failure description, should contain relevant data for the error (e.g., a stack trace).
            error_type (:obj:`str`): The type of error that occurred. If an exception is thrown the full class name of the exception.

        """

        if message is None and output is None:
            return

        error = {
            "message": message,
            "output": output,
            "type": error_type
        }

        if self.allow_multiple_subelements:
            self._errors.append(error)
        else:
            self._errors = [error]

    def add_failure(self, message=None, output=None, failure_type=None):
        """Adds a failure to the test case. Failure indicates that the test failed.
        A failure is a condition which the code has explicitly failed by using the mechanisms for that purpose.
        For example via an ``AssertException``.

        Args:
            message (:obj:`str`): The message specified in the assert.
            output (:obj:`str`): The failure description, should contain relevant data for the failure (e.g., a stack trace).
            failure_type (:obj:`str`): The type of the assert.

        """

        if message is None and output is None:
            return

        failure = {
            "message": message,
            "output": output,
            "type": failure_type
        }

        if self.allow_multiple_subelements:
            self._failures.append(failure)
        else:
            self._failures = [failure]

    def add_skipped(self, message=None, output=None):
        """Adds a skipped to the test case. If the test was not executed.

        Args:
            message (:obj:`str`): The message/description string why the test case was skipped.
            output (:obj:`str`): The skip output.

        """

        skipped = {
            "message": message,
            "output": output
        }

        if self.allow_multiple_subelements:
            self._skipped.append(skipped)
        else:
            self._skipped = [skipped]


class JUnitTestSuite:
    """This class is responsible for managing information related to the execution of a single test suite, including
    any failures or errors associated with the test cases within the suite.

    Args:
        name: The name of the tests case.
        test_cases (:obj:`list`): A list of :class:`~JUnitTestCase`.
        id (:obj:`str`): The id of the test suite.
        stdout (:obj:`str`): The data written to ``stdout`` during the test execution.
        stderr (:obj:`str`): The data written to ``stderr`` during the test execution.
        package (:obj:`str`): The package name of the test suite.
        hostname (:obj:`str`): The hostname of the test suite.
        filename (:obj:`str`): The full file name of the test suite.
        log (:obj:`str`): The log of the test suite.
        url (:obj:`str`): The url of the test suite.
        timestamp (:obj:`str`): The time when the test suite execution started.
        properties (:obj:`dict`): The test suite properties.

    """

    def __init__(self, name, test_cases=None, id=None, stdout=None, stderr=None, package=None, hostname=None,
                 filename=None, log=None, url=None, timestamp=None, properties=None):

        self.name = name
        self.test_cases = test_cases or []

        self.id = id

        self.stdout = stdout
        self.stderr = stderr

        self.timestamp = timestamp

        self.package = package
        self.filename = filename
        self.log = log

        self.hostname = hostname
        self.url = url

        self.properties = properties

    @property
    def assertions(self):
        return sum(int(test_case.assertions) for test_case in self.test_cases if test_case.assertions)

    @property
    def disabled(self):
        return sum(1 for test_case in self.test_cases if not test_case.is_enabled)

    @property
    def errors(self):
        return sum(1 for test_case in self.test_cases if test_case.is_error)

    @property
    def failures(self):
        return sum(1 for test_case in self.test_cases if test_case.is_failure)

    @property
    def skipped(self):
        return sum(1 for test_case in self.test_cases if test_case.is_skipped)

    @property
    def tests(self):
        return len(self.test_cases)

    @property
    def time(self):
        return sum(test_case.elapsed_seconds for test_case in self.test_cases if test_case.elapsed_seconds)

    @property
    def attributes(self):
        attributes = dict()

        attributes["name"] = str(self.name)

        if self.hostname:
            attributes["hostname"] = str(self.hostname)
        if self.id:
            attributes["id"] = str(self.id)
        if self.package:
            attributes["package"] = str(self.package)
        if self.timestamp:
            attributes["timestamp"] = str(self.timestamp)
        if self.filename:
            attributes["file"] = str(self.filename)
        if self.log:
            attributes["log"] = str(self.log)
        if self.url:
            attributes["url"] = str(self.url)

        attributes["tests"] = str(len(self.test_cases))
        attributes["assertions"] = str(self.assertions)
        attributes["disabled"] = str(self.disabled)
        attributes["errors"] = str(self.errors)
        attributes["failures"] = str(self.failures)
        attributes["skipped"] = str(self.skipped)
        attributes["time"] = str(self.time)

        return attributes

    def _xml(self):
        xml_element = ET.Element("testsuite", self.attributes)

        if self.properties:
            xml_element.append(generate_properties_xml(self.properties))

        if self.stdout:
            xml_element.append(generate_stdout_xml(self.stdout))

        if self.stderr:
            xml_element.append(generate_stderr_xml(self.stderr))

        for test_case in self.test_cases:
            xml_element.append(test_case._xml())

        return xml_element

    def create_test_case(self, *args, **kwargs):
        """Create a new test cases and add it to the test suite.

        Arguments and optional keyword arguments correspond to the :class:`~JUnitTestCase` constructor arguments,
        documented above.

        Returns:
            JUnitTestCase: The new test case.

        """

        test_case = JUnitTestCase(*args, **kwargs)
        self.test_cases.append(test_case)

        return test_case

    def add_test_case(self, test_case):
        """Add a test case to the test suite."""

        self.test_cases.append(test_case)


class JUnitReporter:
    """This class is a test reporter that can produce JUnit XML reports to express test results.

    Args:
        test_suites (:obj:`list` of :class:`~JUnitTestSuite`, optional): A list of test suites to include in the report.

    """

    def __init__(self, test_suites=None):
        self.test_suites = test_suites or []

    def __repr__(self):
        return f"{self.__class__.__name__}(test_suites={self.test_suites!r})"

    def _xml(self):
        """Generate the JUnit XML report.

        Returns:
            :class:`~xml.etree.ElementTree.Element`: The root element of the JUnit XML report.

        """

        xml_element = ET.Element("testsuites")

        for test_suite in self.test_suites:
            xml_element.append(test_suite._xml())

        for key, value in self.attributes.items():
            xml_element.set(key, str(value))

        return xml_element

    @property
    def attributes(self):
        """Compute the summary attributes of the JUnit report.

        Returns:
            :obj:`defaultdict` of :obj:`int`: A dictionary of summary attributes of the JUnit report.

        """

        attributes = defaultdict(int)

        for test_suite in self.test_suites:
            for key in ["disabled", "errors", "failures", "tests", "time"]:
                attributes[key] += getattr(test_suite, key)

        return attributes

    def to_string(self, prettyprint=True):
        """Generate a string representation of the JUnit report.

        Args:
            prettyprint (:obj:`bool`, optional): Whether to pretty-print the XML output. Defaults to True.

        Returns:
            :obj:`str`: The string representation of the JUnit report.

        """

        xml_element = self._xml()
        xml_string = ET.tostring(xml_element, encoding="unicode")
        xml_string = xml_safe(xml_string)

        if prettyprint:
            xml_string = xml.dom.minidom.parseString(xml_string)
            xml_string = xml_string.toprettyxml()

        return xml_string

    def write(self, filename="report.xml", prettyprint=True):
        """Write the JUnit report to a file in XML format.

        Args:
            filename (:obj:`str`, optional): The name of the output file. Defaults to 'report.xml'.
            prettyprint (:obj:`bool`, optional): Whether to pretty-print the XML output. Defaults to True.

        """

        xml_string = self.to_string(prettyprint=prettyprint)

        with open(filename, "w") as fp:
            fp.write(xml_string)

    def add_test_suite(self, test_suite):
        """Add a test suite to the report.

        Args:
            test_suite (JUnitTestSuite): The test suite to add to the report.

        """

        self.test_suites.append(test_suite)

    def create_test_suite(self, *args, **kwargs):
        """Create a new test suite and add it to the report.

        Arguments and optional keyword arguments correspond to the :class:`~JUnitTestSuite` constructor arguments,
        documented above.

        Args:
            name (str, optional): The name of the test suite. Defaults to None.
            tests (int, optional): The total number of tests in the suite. Defaults to None.
            failures (int, optional): The total number of failed tests in the suite. Defaults to None.
            errors (int, optional): The total number of tests with errors in the suite. Defaults to None.
            time (float, optional): The total time taken to run the tests in the suite. Defaults to None.
            timestamp (str, optional): The timestamp when the tests were run. Defaults to None.
            hostname (str, optional): The hostname of the machine where the tests were run. Defaults to None.
            id (str, optional): The ID of the test suite. Defaults to None.

        Returns:
            JUnitTestSuite: The new test suite.

        """

        test_suite = JUnitTestSuite(*args, **kwargs)
        self.test_suites.append(test_suite)

        return test_suite

    @classmethod
    def report_to_string(cls, test_suites, prettyprint=True):
        """Generate a string representation of the JUnit report.

        Args:
            test_suites (:obj:`list` of :class:`~JUnitTestSuite`): A list of test suites to include in the report.
            prettyprint (:obj:`bool`, optional): Whether to pretty-print the XML output. Defaults to True.

        Returns:
            :obj:`str`: The string representation of the JUnit report.

        """

        junit_xml = cls(test_suites)
        return junit_xml.to_string(prettyprint=prettyprint)

    @classmethod
    def write_report(cls, test_suites, filename="report.xml", prettyprint=True):
        """Generate the JUnit report and write it to a file in XML format.

        Args:
            test_suites (:obj:`list` of :class:`~JUnitTestSuite`): A list of test suites to include in the report.
            filename (:obj:`str`, optional): The name of the output file. Defaults to 'report.xml'.
            prettyprint (:obj:`bool`, optional): Whether to pretty-print the XML output. Defaults to True.

        """

        junit_xml = cls(test_suites)
        return junit_xml.write(filename=filename, prettyprint=prettyprint)
