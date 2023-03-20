from junit_reporter import JUnitReporter, TestCase, TestSuite

test_case = TestCase("Test #1", classname="some.class.name", stdout="I am stdout!", stderr="I am stderr!")
test_suite = TestSuite("Test Suite #1", [test_case])

reporter = JUnitReporter([test_suite])

# Generate a string containing the XML report
xml = reporter.to_string(prettyprint=True)

# Write the XML report in a file
reporter.write(filename="report.xml", prettyprint=True)
