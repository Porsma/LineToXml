import xml.etree.cElementTree as ET


class LineToXml():
    def parse_record(self, record: str, type: str, num_components: int) -> list:
        """
        Check that a record is of correct format.

        :param record: The input string to parse
        :param type: The type of the record, e.g. 'P'
        :raises Exception: raises exception on errors, e.g. faulty type, num arguments etc.
        :return: list with all arguments, except the type
        """
        components = record.strip().split("|")

        if len(components) != num_components + 1:
            raise Exception(f"{type} need {num_components} arguments")

        allowed_types = ('A', 'F', 'P', 'T')
        if components[0] not in allowed_types:
            raise Exception(f"Only {allowed_types} is allowed as first argument")

        if components[0] != type:
            raise Exception(f"{type}-line does not start with '{type}'")

        return components[1:]

    def parse_person(self, record: str) -> ET.Element:
        """
        Parse a person record. A record consist of a first name and
        a last name

        :param record: The input string to parse
        :return: ET.Element containing the xml representation
        """
        components = self.parse_record(record, "P", 2)

        person = ET.Element("person")

        ET.SubElement(person, "firstname").text = components[0]
        ET.SubElement(person, "lastname").text = components[1]

        return person

    def parse_phone(self, record: str) -> ET.Element:
        """
        Parse a phone record. A record consist of a mobile phone number
        and home phone number

        :param record: The input string to parse
        :return: ET.Element containing the xml representation
        """
        components = self.parse_record(record, "T", 2)

        phone = ET.Element("phone")

        ET.SubElement(phone, "mobile").text = components[0]
        ET.SubElement(phone, "home").text = components[1]

        return phone

    def parse_address(self, record: str) -> ET.Element:
        """
        Parse an address record. A record consist of street, city and zip code

        :param record: The input string to parse
        :return: ET.Element containing the xml representation
        """
        components = self.parse_record(record, "A", 3)

        address = ET.Element("address")

        ET.SubElement(address, "street").text = components[0]
        ET.SubElement(address, "city").text = components[1]
        ET.SubElement(address, "zip").text = components[2]

        return address

    def parse_family(self, record: str) -> ET.Element:
        """
        Parse a family record. A record consist of name and year of birth

        :param record: The input string to parse
        :return: ET.Element containing the xml representation
        """
        components = self.parse_record(record, "F", 2)

        family = ET.Element("family")

        ET.SubElement(family, "name").text = components[0]
        ET.SubElement(family, "born").text = components[1]

        return family
