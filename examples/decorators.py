import unittest

from junit_reporter import junit_reporter, junit_test_case, junit_test_suite


@junit_test_suite(name="TestStringMethods", reporter="report.xml")
@junit_reporter(filename="report.xml", prettyprint=True)
class TestStringMethods(unittest.TestCase):

    @junit_test_case()
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    @junit_test_case()
    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    @junit_test_case()
    def test_fail(self):
        self.assertTrue(False)


@junit_test_suite(reporter="report-autodetect.xml", prettyprint=True, auto_discover=True)
class TestAutoDetect(unittest.TestCase):

    def setUp(self):
        self.foo = "FOO"

    def test_lower(self):
        self.assertEqual("FOO".lower(), "foo")

    def test_islower(self):
        self.assertTrue("foo".islower())
        self.assertFalse("Foo".islower())


if __name__ == "__main__":
    unittest.main()
