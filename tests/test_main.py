import random
from datetime import datetime

from junit_reporter import TestCase, TestSuite, TestReporter


def generate_test_case(index):
    test_case = TestCase(
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
        test_case.add_skipped(
            message="Skiped.",
        )

    return test_case


def generate_test_cases():
    return [generate_test_case(x) for x in range(10)]


def generate_test_suites():
    return [
        TestSuite("Test Suite #{}".format(x), test_cases=generate_test_cases()) for x in range(10)
    ]


def test_happy_flow(tmpdir):
    test_case = TestCase("Test Case #1", elapsed_seconds=10)
    test_suite = TestSuite("Test Suite #1", test_cases=[test_case])
    junit_xml = TestReporter([test_suite])

    assert junit_xml.to_string() != ""


def test_xml(tmpdir):
    junit_xml = TestReporter(generate_test_suites())

    junit_xml.write()
    assert junit_xml.to_string() != ""
