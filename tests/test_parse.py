import pytest
import xml.etree.cElementTree as ET

from line_to_xml import LineToXml


@pytest.fixture
def ltx():
    return LineToXml()


def test_parse_record(ltx: LineToXml):
    # Correct number of arguments
    with pytest.raises(Exception):
        ltx.parse_record("P|000")

    # Trims whitespace
    assert isinstance(ltx.parse_record(" P|000|111 ")[1], ET.Element)

    # Correct type returned
    assert ltx.parse_record("P|111|222")[0] == "P"

    # Allowed type
    with pytest.raises(Exception):
        ltx.parse_record("G|abc")


def test_parse_person(ltx: LineToXml):
    input = "P|Carl Gustaf|Bernadotte"

    person = ltx.parse_person(input.split("|")[1:])
    assert person.tag == "person"

    firstname = person.find("firstname")
    lastname = person.find("lastname")
    assert firstname is not None
    assert lastname is not None
    assert firstname.text == "Carl Gustaf"
    assert lastname.text == "Bernadotte"


def test_parse_phone(ltx: LineToXml):
    input = "T|0768-101801|08-101801"

    phone = ltx.parse_phone(input.split("|")[1:])
    assert phone.tag == "phone"

    mobile = phone.find("mobile")
    home = phone.find("home")
    assert mobile is not None
    assert home is not None
    assert mobile.text == "0768-101801"
    assert home.text == "08-101801"


def test_parse_address(ltx: LineToXml):
    input = "A|Drottningholms slott|Stockholm|10001"

    address = ltx.parse_address(input.split("|")[1:])
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

    family = ltx.parse_family(input.split("|")[1:])
    assert family.tag == "family"

    name = family.find("name")
    born = family.find("born")
    assert name is not None
    assert born is not None
    assert name.text == "Victoria"
    assert born.text == "1977"


def test_append_to_person_or_family(ltx: LineToXml):
    person = ET.Element("person")
    address = ET.Element("address")

    ltx.append_to_person_or_family(person, None, address)
    address = person.find("./address")
    assert address is not None
    assert address.tag == "address"

    person = ET.Element("person")
    family = ET.Element("family")
    address = ET.Element("address")

    ltx.append_to_person_or_family(person, family, address)
    address = family.find("./address")
    assert address is not None
    assert address.tag == "address"

    with pytest.raises(Exception):
        ltx.append_to_person_or_family(None, None, None)


def test_parse(ltx: LineToXml):
    input = None
    with open("example/input.txt") as file:
        input = file.readlines()

    people = ltx.parse(input)
    assert people is not None
    assert people.tag == "people"

    assert len(people.findall("./person")) == 2

    assert len(people.findall("./person[firstname='Carl Gustaf']/family")) == 2
    assert people.find("./person[firstname='Carl Gustaf']/phone/mobile").text == "0768-101801"
    assert people.find("./person[firstname='Carl Gustaf']/family[name='Victoria']/address/street").text == "Haga Slott"
    assert people.find("./person[firstname='Carl Gustaf']/family[name='Carl Philip']/phone/home").text == "08-101802"

    assert len(people.findall("./person[firstname='Barack']/family")) == 0
    assert people.find("./person[firstname='Barack']/address/street").text == "1600 Pennsylvania Avenue"
