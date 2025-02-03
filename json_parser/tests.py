from django.test import TestCase
from json_parser.services.json_parser import json_parser

# Create your tests here.
class JsonParserTestCase(TestCase):

    def test_json_parser_step1_invalid(self):
        file = "json_parser/tests/step1/invalid.json"
        self.assertEqual(json_parser(file), "")

    def test_json_parser_step1_valid(self):
        file = "json_parser/tests/step1/valid.json"
        self.assertEqual(json_parser(file), "{}")