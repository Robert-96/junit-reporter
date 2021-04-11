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

# ...
```

Produces the following output:

.. code-block:: xml

    <test></test>

## Running the tests

```
$ pytest tests
```

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
