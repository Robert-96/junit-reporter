import unittest

from junit_reporter import JUnitReporter
from junit_reporter.decorator import junit_reporter, test_suite, test_case


reporter = JUnitReporter("report.xml", prettyprint=True)


@test_suite(reporter=reporter)
class TestStringMethods(unittest.TestCase):

    @test_case()
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    @test_case()
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    @test_case()
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # Check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
