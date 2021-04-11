# junit-reporter

A Python3 package that generates test results in the standard JUnit XML format for use with Jenkins and other build integration servers.

## Installation

Use the following command to install ``junit-reporter``:

```
$ pip install junit-reporter
```

## Quickstart

Create a test report:

```python
from junit_reporter import TestCase, TestSuite, TestReporter

test_case = TestCase('Test #1', classname='some.class.name', stdout='I am stdout!', stderr='I am stderr!')
test_suite = TestSuite('Test Suite #1', [test_case])

xml = TestReporter.report_to_string([test_suite])
```

It produces the following output:

```xml
<?xml version="1.0" ?>
<testsuites disabled="0" errors="0" failures="0" tests="1" time="0">
    <testsuite name="Test Suite #1" tests="1" assertions="0" disabled="0" errors="0" failures="0" skipped="0" time="0">
        <testcase name="Test #1" classname="some.class.name">
            <system-out>I am stdout!</system-out>
            <system-err>I am stderr!</system-err>
        </testcase>
    </testsuite>
</testsuites>
```

## Running the tests

```
$ pytest tests
```

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
