from typing import Any, Dict, Union, List

JSONValue = Union[str, int, float, bool, None, 'JSONObject', 'JSONArray']
JSONObject = Dict[str, JSONValue]
JSONArray = List[JSONValue]


def json_parser(token: str) -> JSONValue:
    
    if token == 'null':
        return None
    elif token == 'true':
        return True
    elif token == 'false':
        return False
    elif token.isdigit():
        return int(token)
    elif token.replace('.', '', 1).isdigit():
        return float(token)
    elif token.startswith('{') and token.endswith('}'):
        return {}
    elif token.startswith('[') and token.endswith(']'):
        return []
    else:
        return token
    
    
