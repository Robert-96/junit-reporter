import os
import random
from datetime import datetime

from junit_reporter import JUnitReporter, JUnitTestCase, JUnitTestSuite


def generate_test_case(index):
    test_case = JUnitTestCase(
        "Test Case #{}".format(index),
        assertions=random.randint(0, index),
        stdout="Output: {}.".format(index),
        stderr="Error: {}.".format(index),
        timestamp=datetime.now().strftime("%H:%M:%S.%f - %b %d %Y"),
        elapsed_seconds=index,
    )

    test_case_type = random.choice(["PASS", "ERROR", "FAIL", "SKIP"])

    if test_case_type == "ERROR":
        test_case.add_error(
            message="ValueError: Invalid arguments.",
            error_type="ValueError"
        )

    if test_case_type == "FAIL":
        test_case.add_failure(
            message="AssertError: Invalid arguments.",
            failure_type="AssertError"
        )

    if test_case_type == "SKIP":
        test_case.skip(
            message="Skipped.",
        )

    return test_case


def generate_test_cases():
    return [generate_test_case(x) for x in range(10)]


def generate_test_suites():
    return [
        JUnitTestSuite("Test Suite #{}".format(x), test_cases=generate_test_cases()) for x in range(10)
    ]


def test_repr():
    test_case = JUnitTestCase("Test Case #1", elapsed_seconds=10)
    test_suite = JUnitTestSuite("Test Suite #1", test_cases=[test_case])
    junit_xml = JUnitReporter([test_suite])

    assert eval(repr(junit_xml)).attributes == junit_xml.attributes


def test_happy_flow():
    test_case = JUnitTestCase("Test Case #1", elapsed_seconds=10)
    test_suite = JUnitTestSuite("Test Suite #1", test_cases=[test_case])
    junit_xml = JUnitReporter([test_suite])

    assert junit_xml.to_string() != ""
    assert junit_xml.to_string(prettyprint=False) != ""
    assert len(junit_xml.to_string()) > len(junit_xml.to_string(prettyprint=False))


def test_report_to_string():
    test_case = JUnitTestCase("Test Case #1", elapsed_seconds=10)
    test_suite = JUnitTestSuite("Test Suite #1", test_cases=[test_case])

    report = JUnitReporter.report_to_string([test_suite])
    report_min = JUnitReporter.report_to_string([test_suite], prettyprint=False)

    assert report != ""
    assert report_min != ""
    assert len(report) > len(report_min)


def test_crete_test_suite():
    junit_xml = JUnitReporter()

    assert junit_xml.suites == 0

    junit_xml.create_test_suite("TestSuite #1")

    assert junit_xml.suites == 1


def test_write(tmpdir):
    junit_xml = JUnitReporter(generate_test_suites())

    xml_file = os.path.join(tmpdir, "report.xml")
    junit_xml.write(filename=xml_file)

    with open(xml_file) as fp:
        xml = fp.read()

    assert xml != ""


def test_write_report(tmpdir):
    xml_file = os.path.join(tmpdir, "report.xml")
    JUnitReporter.write_report(generate_test_suites(), filename=xml_file)

    with open(xml_file) as fp:
        xml = fp.read()

    assert xml != ""
