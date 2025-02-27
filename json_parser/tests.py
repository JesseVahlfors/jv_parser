from django.test import TestCase
from json_parser.services.json_parser import parse

# Create your tests here.
class JsonParserTestCase(TestCase):

    def test_output(self):
        print("This is the output: ", parse('{"key": "value", "key2": "value"}'))

    def read_file(self, file):
        with open(file, "r") as f:
            return f.read()

    def test_json_parser_step1_invalid(self):
        file = "json_parser/tests/step1/invalid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), "Invalid JSON: Unexpected end of input.")

    def test_json_parser_step1_valid(self):
        file = "json_parser/tests/step1/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {})

    def test_json_parser_step2_invalid(self):
        file = "json_parser/tests/step2/invalid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), "Invalid JSON")

    def test_json_parser_step2_valid(self):
        file = "json_parser/tests/step2/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {"key": "value"})
    
    def test_json_parser_step2_invalid2(self):
        file = "json_parser/tests/step2/invalid2.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), "Invalid JSON")

    def test_json_parser_step2_valid2(self):
        file = "json_parser/tests/step2/valid2.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {"key": "value", "key2": "value"})