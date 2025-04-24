import unittest

from junit_reporter import junit_reporter, junit_test_case, junit_test_suite


@junit_test_suite(name="TestStringMethods", reporter="report.xml")
@junit_reporter(filename="report.xml", prettyprint=False)
class TestStringMethods(unittest.TestCase):
    """Test suite for string method behaviors."""

    @junit_test_case()
    def test_upper(self):
        """Test that the upper() method converts strings to uppercase."""

        self.assertEqual("hello".upper(), "HELLO")

    @junit_test_case()
    def test_isupper(self):
        """Test that isupper() correctly identifies uppercase strings."""

        self.assertTrue("HELLO".isupper())
        self.assertFalse("Hello".isupper())

    @junit_test_case()
    def test_fail(self):
        """Example of a failing test case to demonstrate reporting."""

        self.assertTrue(False, "This test is designed to fail.")

    @junit_test_case()
    def test_upper_edge_case(self):
        """Test upper() with an empty string."""

        self.assertEqual("".upper(), "")

    @junit_test_case()
    def test_isupper_edge_case(self):
        """Test isupper() with a string containing numbers and symbols."""

        self.assertFalse("123!".isupper())


@junit_test_suite(reporter="report-autodetect.xml", prettyprint=True, auto_discover=True)
class TestAutoDetect(unittest.TestCase):
    """Test suite for auto-detected string behaviors."""

    def setUp(self):
        """Set up a common test fixture."""

        self.foo = "FOO"
        self.assertEqual(self.foo, "FOO", "Fixture setup failed.")

    def test_lower(self):
        """Test that the lower() method converts strings to lowercase."""

        print("Running test_lower...") # The stdout and stderr will be captured by the reporter
        self.assertEqual("FOO".lower(), "foo")

    def test_islower(self):
        """Test that islower() correctly identifies lowercase strings."""

        self.assertTrue("foo".islower())
        self.assertFalse("Foo".islower())

    def tearDown(self):
        """Clean up after tests."""

        self.foo = None


if __name__ == "__main__":
    unittest.main()
