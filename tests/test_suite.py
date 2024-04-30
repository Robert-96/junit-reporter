import datetime
import random

from junit_reporter import JUnitTestCase, JUnitTestSuite

from .conftest import FAKE_NOW


def test_repr():
    test_suite = JUnitTestSuite("Test Suite #1")

    assert eval(repr(test_suite)).attributes == test_suite.attributes


def test_tests():
    test_suite = JUnitTestSuite("Test Suite #1")
    expected = random.randint(2, 5)

    assert test_suite.tests == 0

    for i in range(expected):
        test_case = JUnitTestCase(f"Test Case #{i}")
        test_suite.add_test_case(test_case)

        assert test_suite.tests == i + 1

    assert test_suite.tests == expected


def test_disable():
    test_suite = JUnitTestSuite("Test Suite #1")
    expected = random.randint(2, 5)

    assert test_suite.disabled == 0

    for i in range(expected):
        test_case = JUnitTestCase(f"Test Case #{i}", enabled=False)
        test_suite.add_test_case(test_case)

        assert test_suite.disabled == i + 1

    assert test_suite.disabled == expected


def test_errors():
    test_suite = JUnitTestSuite("Test Suite #1")
    expected = random.randint(2, 5)

    assert test_suite.errors == 0

    for i in range(expected):
        test_case = JUnitTestCase(f"Test Case #{i}")
        test_case.add_error(message=f"Error message #{i}")
        test_suite.add_test_case(test_case)

        assert test_suite.errors == i + 1

    assert test_suite.errors == expected


def test_failures():
    test_suite = JUnitTestSuite("Test Suite #1")
    expected = random.randint(2, 5)

    assert test_suite.failures == 0

    for i in range(expected):
        test_case = JUnitTestCase(f"Test Case #{i}")
        test_case.add_failure(message=f"Failure message #{i}")
        test_suite.add_test_case(test_case)

        assert test_suite.failures == i + 1

    assert test_suite.failures == expected


def test_skipped():
    test_suite = JUnitTestSuite("Test Suite #1")
    expected = random.randint(2, 5)

    assert test_suite.skipped == 0

    for i in range(expected):
        test_case = JUnitTestCase(f"Test Case #{i}")
        test_case.skip(message=f"Skip reason #{i}")
        test_suite.add_test_case(test_case)

        assert test_suite.skipped == i + 1

    assert test_suite.skipped == expected


def test_properties_xml():
    properties = {"version": "1.0.0", "browser": "Firefox"}
    test_suite = JUnitTestSuite("Test Suite #1", properties=properties)

    test_suite_xml = test_suite._xml()
    properties_xml = test_suite_xml.findall("properties")
    assert len(properties_xml) == 1
    assert len(properties_xml[0].findall("property")) == len(properties)

    for property_xml in properties_xml[0].findall("property"):
        name = property_xml.attrib["name"]
        value = property_xml.attrib["value"]

        assert properties[name] == value


def test_stdout_xml():
    stdout = "Test stdout."
    test_suite = JUnitTestSuite("Test Suite #1", stdout=stdout)
    test_suite_xml = test_suite._xml()
    stdout_xml = test_suite_xml.find("system-out")

    assert stdout_xml.text == stdout


def test_stderr_xml():
    stderr = "Test stderr."
    test_suite = JUnitTestSuite("Test Suite #1", stderr=stderr)
    test_suite_xml = test_suite._xml()
    stderr_xml = test_suite_xml.find("system-err")

    assert stderr_xml.text == stderr


def test_attributes(mock_datetime_now):
    test_suite = JUnitTestSuite(
        "Test Suite #1",
        id=1,
        package="tests",
        hostname="localhost",
        filename="tests.py",
        timestamp=datetime.datetime.now(),
        log="tests.log",
        url="localhost:2424"
    )

    expected = {
        "name": "Test Suite #1",
        "hostname": "localhost",
        "id": "1",
        "package": "tests",
        "file": "tests.py",
        "log": "tests.log",
        "url": "localhost:2424",
        "timestamp": str(FAKE_NOW),
        "tests": "0",
        "assertions": "0",
        "disabled": "0",
        "errors": "0",
        "failures": "0",
        "skipped": "0",
        "time": "0"
    }

    assert test_suite.attributes == expected


def test_create_junit_test_case():
    test_suite = JUnitTestSuite("Test Suite #1")
    expected = random.randint(2, 5)

    assert test_suite.tests == 0

    for i in range(expected):
        test_suite.create_test_case(f"Test Case #{i}")

        assert test_suite.tests == i + 1

    assert test_suite.tests == expected
