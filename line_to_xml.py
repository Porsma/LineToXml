import xml.etree.cElementTree as ET


class LineToXml():
    def parse_record(self, record: str) -> ET.Element:
        """
        Check that a record is of correct format and convert it to an XML-object

        :param record: The input string to parse
        :raises Exception: raises exception on errors, e.g. faulty type, num arguments etc.
        :return (str, ET.Element) : A tuple with the type as a string in the first field and an XML-object as the second
        """
        types = {
            "A": {"num_args": (2, 3), "parser": self.parse_address},
            "F": {"num_args": (2, ), "parser": self.parse_family},
            "P": {"num_args": (2, ), "parser": self.parse_person},
            "T": {"num_args": (2, ), "parser": self.parse_phone}
        }

        if len(record) == 0:
            raise Exception("No empty lines allowed")

        record = record.strip()
        arguments = record.split("|")[1:]
        type = record[0]

        num_args = types[type]["num_args"]
        if len(arguments) not in num_args:
            raise Exception(f"Number of arguments for a '{type}' record is not fullfilled: {record}")

        if type not in types.keys():
            raise Exception(f"Only {types.keys()} is allowed as first argument: {record}")

        element = types[type]["parser"](arguments)

        return (type, element)

    def parse_person(self, components: list) -> ET.Element:
        """
        Parse a person record. A record consist of a first name and
        a last name

        :param record: a list or arguments to create the XML-object from
        :return: ET.Element containing the xml representation
        """
        person = ET.Element("person")

        ET.SubElement(person, "firstname").text = components[0]
        ET.SubElement(person, "lastname").text = components[1]

        return person

    def parse_phone(self, components: list) -> ET.Element:
        """
        Parse a phone record. A record consist of a mobile phone number
        and home phone number

        :param record: a list or arguments to create the XML-object from
        :return: ET.Element containing the xml representation
        """
        phone = ET.Element("phone")

        ET.SubElement(phone, "mobile").text = components[0]
        ET.SubElement(phone, "home").text = components[1]

        return phone

    def parse_address(self, components: list) -> ET.Element:
        """
        Parse an address record. A record consist of street, city and zip code

        :param record: a list or arguments to create the XML-object from
        :return: ET.Element containing the xml representation
        """
        address = ET.Element("address")

        ET.SubElement(address, "street").text = components[0]
        ET.SubElement(address, "city").text = components[1]
        if len(components) >= 3:
            ET.SubElement(address, "zip").text = components[2]

        return address

    def parse_family(self, components: list) -> ET.Element:
        """
        Parse a family record. A record consist of name and year of birth

        :param record: a list or arguments to create the XML-object from
        :return: ET.Element containing the xml representation
        """
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
            (type, element) = self.parse_record(record)

            if type in ("A", "T"):
                self.append_to_person_or_family(person, family, element)

            elif type == "F":
                family = element
                if person is None:
                    raise Exception(f"Unexpected family record {record}. No person to add record to")
                person.append(family)

            elif type == "P":
                person = element
                people.append(person)
                family = None

            else:
                raise Exception(f"Unsupported record type {type}: {record}")

        return people
