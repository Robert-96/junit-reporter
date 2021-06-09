import pytest

from junit_reporter.xml import xml_safe


VALID_CHARS = [0x9, 0xA, 0x20]
INVALID_CHARS = [0x1, 0xB, 0xC, 0xE, 0x00, 0x19, 0xD800, 0xDFFF, 0xFFFE, 0x0FFFF]


@pytest.mark.parametrize(
    "string, expected", [
        *[(chr(x), chr(x)) for x in VALID_CHARS],
        *[(chr(x), "?") for x in INVALID_CHARS]
    ]
)
def test_xml_save(string, expected):
    assert xml_safe(string) == expected
