==========
Quickstart
==========

Create a test report:

.. code-block:: python

    from junit_reporter import TestCase, TestSuite, TestReporter

    test_case = TestCase('Test #1', classname='some.class.name', stdout='I am stdout!', stderr='I am stderr!')
    test_suite = TestSuite('Test Suite #1', [test_case])

    xml = TestReporter.report_to_string([test_suite])


It produces the following output:

.. code-block:: xml

    <?xml version="1.0" ?>
    <testsuites disabled="0" errors="0" failures="0" tests="1" time="0">
        <testsuite name="Test Suite #1" tests="1" assertions="0" disabled="0" errors="0" failures="0" skipped="0" time="0">
            <testcase name="Test #1" classname="some.class.name">
                <system-out>I am stdout!</system-out>
                <system-err>I am stderr!</system-err>
            </testcase>
        </testsuite>
    </testsuites>

If you want to write the Junit XML to file:

.. code-block:: python

    from junit_reporter import TestCase, TestSuite, TestReporter

    test_case = TestCase('Test #1', classname='some.class.name', stdout='I am stdout!', stderr='I am stderr!')
    test_suite = TestSuite('Test Suite #1', [test_case])

    xml = TestReporter.write_report([test_suite], filename="report.xml")

This will write the report to ``report.xml``. By default ``prettyprint`` is set
to ``True`` but can be disabled using the ``prettyprint`` keyword argument.

.. code-block:: python

    xml = TestReporter.write_report([test_suite], filename="report.xml", prettyprint=False)


.. note::

    Unicode characters identified as "illegal or discouraged" are automatically replaced with ``?`` in the XML string or file.

    You can se the full list of illegal characters `here <https://www.w3.org/TR/xml11/#charsets>`_.
