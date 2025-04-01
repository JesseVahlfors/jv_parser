from django.test import TestCase
from json_parser.services.json_parser import parse
import os
import json
from pathlib import Path

# Create your tests here.
class JsonParserTestCase(TestCase):

    #def test_output(self):
        #print("This is the output: ", parse('{"name": "John", "sex": "male", "boolean": true, "null": null, "age": 30, "height": 1.75, "array": [1, 2, 3], "object": {"key": "value"}}'))

    def test_empty_input(self):
        with self.assertRaises(ValueError) as context:
            parse("")
        self.assertEqual(str(context.exception), "Invalid JSON: Input must be a valid JSON string")

    def test_only_string_input(self):
        print("Testing only string input", parse("string"))
        with self.assertRaises(Exception) as context:
            parse("string")
        self.assertTrue("Invalid JSON:" in str(context.exception))

    def test_whitespace_only_input(self):
        with self.assertRaises(Exception) as context:
            parse("   ")
        self.assertTrue("Unexpected end of input" in str(context.exception))

    def test_nested_objects(self):
        json_string = '{"a": {"b": {"c": {"d": {"e": "value"}}}}}'
        self.assertEqual(parse(json_string), {"a": {"b": {"c": {"d": {"e": "value"}}}}})

    def test_nested_arrays(self):
        json_string = '[1, [2, [3, [4, [5]]]]]'
        self.assertEqual(parse(json_string), [1, [2, [3, [4, [5]]]]])

    def test_mixed_nested_structures(self):
        json_string = '{"a": [1, {"b": [2, {"c": 3}]}]}'
        self.assertEqual(parse(json_string), {"a": [1, {"b": [2, {"c": 3}]}]})

    def test_missing_comma(self):
        json_string = '{"key1": "value1" "key2": "value2"}'
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Expected ',' or '}', but found something else. at line 1, token type: string." in str(context.exception))

    # Test cases for Coding challenges test json
    def read_file(self, file):
        with open(file, "r") as f:
            return f.read()
        
    def test_json_parser_step1_invalid(self):
        file = "json_parser/tests/step1/invalid.json"
        json_string = self.read_file(file)
        with self.assertRaises(ValueError) as context:
            parse(json_string)
        self.assertEqual(str(context.exception), "Invalid JSON: Input must be a valid JSON string")

    def test_json_parser_step1_valid(self):
        file = "json_parser/tests/step1/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {})

    def test_json_parser_step2_invalid(self):
        file = "json_parser/tests/step2/invalid.json"
        json_string = self.read_file(file)
        with self.assertRaises(Exception) as context:
            parse(json_string)
            print("This is the output: ", parse(json_string))
        self.assertTrue("Invalid JSON: Unexpected trailing comma" in str(context.exception))

    def test_json_parser_step2_valid(self):
        file = "json_parser/tests/step2/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {"key": "value"})
    
    def test_json_parser_step2_invalid2(self):
        file = "json_parser/tests/step2/invalid2.json"
        json_string = self.read_file(file)
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Unexpected keyword: key2." in str(context.exception))

    def test_json_parser_step2_valid2(self):
        file = "json_parser/tests/step2/valid2.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {"key": "value", "key2": "value"})

    def test_json_parser_step3_invalid(self):
        file = "json_parser/tests/step3/invalid.json"
        json_string = self.read_file(file)
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Unexpected keyword: False." in str(context.exception))

    def test_json_parser_step3_valid(self):
        file = "json_parser/tests/step3/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), { 
                                            "key1": True,
                                            "key2": False,
                                            "key3": None,
                                            "key4": "value",
                                            "key5": 101
                                            })
        
    def test_json_parser_step4_invalid(self):
        file = "json_parser/tests/step4/invalid.json"
        json_string = self.read_file(file)
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Unexpected character: '." in str(context.exception))

    def test_json_parser_step4_valid(self):
        file = "json_parser/tests/step4/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {
                                            "key": "value",
                                            "key-n": 101,
                                            "key-o": {},
                                            "key-l": []
                                            })

    def test_json_parser_step4_valid2(self):
        file = "json_parser/tests/step4/valid2.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {
                                            "key": "value",
                                            "key-n": 101,
                                            "key-o": {
                                                "inner key": "inner value"
                                            },
                                            "key-l": ["list value"]
                                            })

    #json.org test cases
    def test_json_parser_json_org_test_cases(self):
        TEST_DIR = Path("json_parser/tests/json.org_tests/test").resolve()
        print(f"Test directory: {TEST_DIR}")

        for filename in os.listdir(TEST_DIR):
            if filename.endswith(".json"):
                file_path = TEST_DIR / filename
                with open(file_path, 'r', encoding="utf-8") as file:
                    json_string = file.read()

                print(f"Testing {filename}...")
                    
                if "fail" in filename:
                    with self.assertRaises(Exception):
                        parse(json_string)
                else:
                    expected = json.loads(json_string)
                    result = parse(json_string)
                    self.assertEqual(result, expected)
                   

 