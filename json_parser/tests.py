from django.test import TestCase
from json_parser.services.json_parser import json_parser

# Create your tests here.
class JsonParserTestCase(TestCase):

    def test_output(self):
        print(json_parser("{}"))

    def test_json_parser_step1_invalid(self):
        file = "json_parser/tests/step1/invalid.json"
        self.assertEqual(json_parser(file), "Invalid JSON")

    def test_json_parser_step1_valid(self):
        file = "json_parser/tests/step1/valid.json"
        self.assertEqual(json_parser(file), {})

    """ def test_json_parser_step2_invalid(self):
        file = "json_parser/tests/step2/invalid.json"
        self.assertEqual(json_parser(file), "Invalid JSON")

    def test_json_parser_step2_valid(self):
        file = "json_parser/tests/step2/valid.json"
        self.assertEqual(json_parser(file), {"key": "value"})
    
    def test_json_parser_step2_invalid2(self):
        file = "json_parser/tests/step2/invalid2.json"
        self.assertEqual(json_parser(file), "Invalid JSON")

    def test_json_parser_step2_valid2(self):
        file = "json_parser/tests/step2/valid2.json"
        self.assertEqual(json_parser(file), {"key": "value", "key2": "value"}) """