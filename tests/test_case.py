import datetime
import xml.etree.ElementTree as ET

import pytest

from junit_reporter import JUnitTestCase

from .conftest import FAKE_NOW


def test_repr():
    test_case = JUnitTestCase("Test Case #1")

    assert eval(repr(test_case)).attributes == test_case.attributes


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

    assert not test_case.is_error

    for error in errors:
        test_case.add_error(**error)

    assert test_case.is_error == expected


@pytest.mark.parametrize(
    "error, allow_multiple_subelements", [
        ({"message": "Error Message."}, True),
        ({"message": "Error Message."}, False),
        ({"output": "Error Output."}, True),
        ({"output": "Error Output."}, False),
        ({"message": "Error Message.", "output": "Error Output."}, True),
        ({"message": "Error Message.", "output": "Error Output."}, False),
    ]
)
def test_error_xml(error, allow_multiple_subelements):
    test_case = JUnitTestCase("Test Case #1", allow_multiple_subelements=allow_multiple_subelements)
    test_case.add_error(**error)

    xml_element = test_case._xml()
    error_elements = xml_element.findall("error")

    assert len(error_elements) == 1

    error_element = error_elements[0]
    assert error_element.text == error.get("output")

    if error.get("message"):
        assert error_element.attrib == {"message": error.get("message"), "type": error.get("error_type", "error")}
    else:
        assert error_element.attrib == {"type": error.get("error_type", "error")}


@pytest.mark.parametrize("allow_multiple_subelements", [True, False])
def test_error_xml_with_no_error(allow_multiple_subelements):
    test_case = JUnitTestCase("Test Case #1", allow_multiple_subelements=allow_multiple_subelements)
    test_case.add_error()

    xml_element = test_case._xml()
    error_elements = xml_element.findall("error")

    assert len(error_elements) == 0


@pytest.mark.parametrize(
    "errors, allow_multiple_subelements", [
        ([{"message": "Error Message."}], True),
        ([{"message": "Error Message."}], False),
        ([{"output": "Error Output."}], True),
        ([{"output": "Error Output."}], False),
        ([{"message": "Error Message."}, {"output": "Error Output."}], True),
        ([{"message": "Error Message."}, {"output": "Error Output."}], False),
    ]
)
def test_error_xml_with_multiple_errors(errors, allow_multiple_subelements):
    test_case = JUnitTestCase("Test Case #1", allow_multiple_subelements=allow_multiple_subelements)

    for error in errors:
        test_case.add_error(*error)

    xml_element = test_case._xml()
    error_elements = xml_element.findall("error")

    assert len(error_elements) == len(errors) if allow_multiple_subelements else 1


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

    assert not test_case.is_failure

    for failure in failures:
        test_case.add_failure(**failure)

    assert test_case.is_failure == expected


@pytest.mark.parametrize(
    "failure, allow_multiple_subelements", [
        ({"message": "Failure Message."}, True),
        ({"message": "Failure Message."}, False),
        ({"output": "Failure Output."}, True),
        ({"output": "Failure Output."}, False),
        ({"message": "Failure Message.", "output": "Failure Output."}, True),
        ({"message": "Failure Message.", "output": "Failure Output."}, False),
    ]
)
def test_failure_xml(failure, allow_multiple_subelements):
    test_case = JUnitTestCase("Test Case #1", allow_multiple_subelements=allow_multiple_subelements)
    test_case.add_failure(**failure)

    xml_element = test_case._xml()
    failures_element = xml_element.findall("failure")

    assert len(failures_element) == 1

    failure_element = failures_element[0]
    assert failure_element.text == failure.get("output")

    if failure.get("message"):
        assert failure_element.attrib == {"message": failure.get("message"), "type": failure.get("failure_type", "failure")}
    else:
        assert failure_element.attrib == {"type": failure.get("failure_type", "failure")}


@pytest.mark.parametrize(
    "skip, expected", [
        (None, False),
        ({"message": "Skip."}, True),
        ({"output": "Skip."}, True),
        ({"message": "Skip."}, True),
    ]
)
def test_is_skipped(skip, expected):
    test_case = JUnitTestCase("Test Case #1")

    assert not test_case.is_skipped

    if skip:
        test_case.skip(**skip)

    assert test_case.is_skipped == expected


@pytest.mark.parametrize(
    "skip", [
        {"message": "Skip message."},
        {"output": "Skip output."},
        {"message": "Skip message.", "output": "Skip output."},
    ]
)
def test_skip_xml(skip):
    test_case = JUnitTestCase("Test Case #1")

    assert not test_case.is_skipped

    test_case.skip(**skip)

    xml_element = test_case._xml()
    skipped_element = xml_element.find("skipped")

    assert skipped_element is not None
    if skip.get("message"):
        assert skipped_element.attrib == {"message": skip.get("message"), "type": "skipped"}
    else:
        assert skipped_element.attrib == {"type": "skipped"}

    assert skipped_element.text == skip.get("output")


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
        log="file.log",
        url="localhost:2424",
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
        "log": "file.log",
        "url": "localhost:2424",
        "timestamp": "2020-08-24 00:00:00"
    }

    assert test_case.attributes == expected


def test_start(mock_datetime_now):
    test_case = JUnitTestCase("Test Case #1")

    assert test_case.timestamp is None
    test_case.start()
    assert test_case.timestamp == FAKE_NOW


def test_finish(mock_datetime_now):
    test_case = JUnitTestCase("Test Case #1")

    assert test_case.elapsed_seconds is None

    test_case.start()
    test_case.finish()

    assert test_case.elapsed_seconds == 7


def test_finish_without_start():
    test_case = JUnitTestCase("Test Case #1")

    assert test_case.elapsed_seconds is None
    test_case.finish()
    assert test_case.elapsed_seconds is None


def test_xml():
    test_case = JUnitTestCase("Test Case #1")
    xml_element = test_case._xml()

    assert xml_element.tag == "testcase"
    assert xml_element.attrib == test_case.attributes
