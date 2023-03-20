import unittest

from junit_reporter import junit_reporter, test_suite, test_case


@junit_reporter(filename="report.xml", prettyprint=True)
@test_suite(name="TestStringMethods", reporter="report.xml")
class TestStringMethods(unittest.TestCase):
    @test_case(test_suite="TestStringMethods")
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    @test_case(test_suite="TestStringMethods")
    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    @test_case(test_suite="TestStringMethods")
    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


@test_suite(reporter="report.xml")
class MyTestCase(unittest.TestCase):
    @test_case(test_suite="MyTestCase")
    def test_nothing(self):
        pass

    @test_case(test_suite="MyTestCase")
    def test_format(self):
        pass

    @test_case(test_suite="MyTestCase")
    def test_maybe_skipped(self):
        pass


if __name__ == "__main__":
    unittest.main()
