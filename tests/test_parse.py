import pytest

from line_to_xml import LineToXml


@pytest.fixture
def ltx():
    return LineToXml()


def test_parse_record(ltx: LineToXml):
    # Correct number of arguments
    with pytest.raises(Exception):
        ltx.parse_record("P|000", "P", 3)

    # Starts with "type"
    with pytest.raises(Exception):
        ltx.parse_record("T|000|111", "P", 2)

    # Trims whitespace
    assert isinstance(ltx.parse_record(" P|000|111 ", "P", 2), list)

    # Allowed type
    with pytest.raises(Exception):
        ltx.parse_record("G|abc", "G", 1)


def test_parse_person(ltx: LineToXml):
    input = "P|Carl Gustaf|Bernadotte"

    person = ltx.parse_person(input)
    assert person.tag == "person"

    firstname = person.find("firstname")
    lastname = person.find("lastname")
    assert firstname is not None
    assert lastname is not None
    assert firstname.text == "Carl Gustaf"
    assert lastname.text == "Bernadotte"


def test_parse_phone(ltx: LineToXml):
    input = "T|0768-101801|08-101801"

    phone = ltx.parse_phone(input)
    assert phone.tag == "phone"

    mobile = phone.find("mobile")
    home = phone.find("home")
    assert mobile is not None
    assert home is not None
    assert mobile.text == "0768-101801"
    assert home.text == "08-101801"


def test_parse_address(ltx: LineToXml):
    input = "A|Drottningholms slott|Stockholm|10001"

    address = ltx.parse_address(input)
    assert address.tag == "address"

    street = address.find("street")
    city = address.find("city")
    zip = address.find("zip")
    assert street is not None
    assert city is not None
    assert zip is not None
    assert street.text == "Drottningholms slott"
    assert city.text == "Stockholm"
    assert zip.text == "10001"


def test_parse_family(ltx: LineToXml):
    input = "F|Victoria|1977"

    family = ltx.parse_family(input)
    assert family.tag == "family"

    name = family.find("name")
    born = family.find("born")
    assert name is not None
    assert born is not None
    assert name.text == "Victoria"
    assert born.text == "1977"
