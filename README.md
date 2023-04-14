# junit-reporter

This is a Python 3 package that creates test results using the standard JUnit XML format, which can be utilized with Jenkins and other build integration servers.

Documentation: <https://junit-reporter.readthedocs.io/>

## Installation

Use the following command to install ``junit-reporter``:

```console
pip install junit-reporter
```

### Living on the edge

If you want to work with the latest code before it’s released, install or
update the code from the `main` branch:

```console
pip install -U https://github.com/Robert-96/junit-reporter
```

## Quickstart

### Using the decorators

Create a JUnit report for a `unittest` project:

```python
import unittest

from junit_reporter import report


class TestFoo(unittest.TestCase):
    pass

```

### Using classes

Create a JUnit report:

```python
from junit_reporter import TestCase, JUnitTestSuite, JUnitReporter

test_case = TestCase('Test #1', classname='some.class.name', stdout='I am stdout!', stderr='I am stderr!')
test_suite = JUnitTestSuite('Test Suite #1', [test_case])

reporter = JUnitReporter([test_suite])

# Generate a string containing the XML report
xml = reporter.to_string(prettyprint=True)

# Write the XML report in a file
reporter.write(filename="report.xml", prettyprint=True)
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

Check out the [API documentation](https://junit-reporter.readthedocs.io/en/latest/api.html) for more details.

## Development

### Running the tests

```console
pytest tests
```

### Building the documentation

```console
cd docs
make docs
```

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
