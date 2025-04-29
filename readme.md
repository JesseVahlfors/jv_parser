# JV Parser

A robust and efficient JSON parser built from scratch in Python, designed to handle JSON parsing with strict compliance to the JSON standard (RFC 8259). This project includes comprehensive error handling, depth limit enforcement, and support for various JSON structures.

This parser was inspired by the coding challenge "Build your own JSON Parser" from Coding Challenges by John Crickett.
You can find the challenges at https://codingchallenges.fyi/


---

## Features

- **Full JSON Compliance**: Adheres to the JSON standard, supporting objects, arrays, strings, numbers, booleans, and `null`.
- **Error Handling**: Provides detailed error messages for invalid JSON, including line and column numbers.
- **Depth Limit Enforcement**: Prevents stack overflow by enforcing a configurable depth limit for nested structures.
- **Performance Optimizations**: Efficient handling of large JSON inputs with optimized string and number parsing.
- **Test Coverage**: Includes extensive test cases, including the official [json.org test suite](https://www.json.org/).

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Testing](#testing)
- [License](#license)

---

## Installation

1. Clone the repository:
   git clone https://github.com/your-username/json-parser.git
   cd json-parser

2. Install dependencies (if any):
    pip install -r requirements.txt

3. Run the tests to ensure everything is working:
    python manage.py test

## Usage

The parse function is the main entry point for parsing JSON strings. It returns the parsed JSON object or raises an exception for invalid JSON.

### Example

    from json_parser.services.json_parser import parse

    # Valid JSON
    json_string = '{"name": "John", "age": 30, "isStudent": false, "grades": [90, 85, 88]}'
    result = parse(json_string)
    print(result)
    # Output: {'name': 'John', 'age': 30, 'isStudent': False, 'grades': [90, 85, 88]}

    # Invalid JSON
    try:
        invalid_json = '{"name": "John", "age": 30, "isStudent": false,}'
        parse(invalid_json)
    except Exception as e:
        print(e)
    # Output: Invalid JSON: Unexpected trailing comma at line 1.

## Examples

### Parsing Nested Structures

    json_string = '{"a": {"b": {"c": {"d": "value"}}}}'
    result = parse(json_string)
    print(result)
    # Output: {'a': {'b': {'c': {'d': 'value'}}}}

### Handling Arrays

    json_string = '[1, 2, 3, {"key": "value"}]'
    result = parse(json_string)
    print(result)
    # Output: [1, 2, 3, {'key': 'value'}]

### Error Handling

    try:
    invalid_json = '{"key": "value",}'
    parse(invalid_json)
    except Exception as e:
        print(e)
    # Output: Invalid JSON: Unexpected trailing comma at line 1.

## Testing

This project includes extensive test cases to ensure correctness and robustness. The tests cover:

Valid and invalid JSON inputs.
Edge cases like deeply nested structures and large inputs.
Compliance with the json.org test suite.

### Run Tests

    python manage.py test

### License

This project is licensed under the GNU General Public License v3.0.

### Acknowledgments

- Official json.org test suite for providing comprehensive test cases.
- John Crickett's Coding Challenges for the inspiration to build this. 