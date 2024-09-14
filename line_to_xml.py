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
        allowed_types = ('A', 'F', 'P', 'T')

        if len(components) != num_components + 1:
            raise Exception(f"A record of type {type} requires {num_components} arguments: {record}")

        if components[0] not in allowed_types:
            raise Exception(f"Only {allowed_types} is allowed as first argument: {record}")

        if type not in allowed_types:
            raise Exception(f"Unknown type {type}. Only {allowed_types} is allowed")

        if components[0] != type:
            raise Exception(f"{type}-line does not start with '{type}': {record}")

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

    def append_to_person_or_family(self, person: ET.Element, family: ET.Element, info: ET.Element) -> None:
        """
        Append an xml element to the person or family element. If family element is not None,
        the info element is appended to the family element, otherwise it is added to the person element

        :param person: XML element to add info to if family parameter is None
        :param family: XML element to add info to if it is not None. Then the info is addde to the person element
        :param info: XML element to add to either person or family
        :raises Exception: If both person and family is None
        """
        if family is not None:
            family.append(info)
        elif person is not None:
            person.append(info)
        else:
            raise Exception(f"No person or family to add record {ET.tostring(info)} to")

    def parse(self, input_records: list[str]) -> ET.Element:
        """
        Parse records and return an XML-tree containing data from the records

        :param input_records: A list of strings to be parsed and added to the XML tree
        :raises Exception: If a record cannot be addded of if a record cannot be parsed
        :returns ET.Element: An XML representation of the input records
        """
        people = ET.Element("people")
        person: ET.Element = None
        family: ET.Element = None

        for record in input_records:
            record = record.strip()

            if len(record) == 0:
                raise Exception("No empty lines accepted")

            type = record[0]

            if type == "A":
                address = self.parse_address(record)
                self.append_to_person_or_family(person, family, address)

            elif type == "F":
                family = self.parse_family(record)
                if person is None:
                    raise Exception(f"Unexpected family record {record}. No person to add record to")
                person.append(family)

            elif type == "P":
                person = self.parse_person(record)
                people.append(person)
                family = None

            elif type == "T":
                phone = self.parse_phone(record)
                self.append_to_person_or_family(person, family, phone)

            else:
                raise Exception(f"Unsupported record type {type}: {record}")

        return people
