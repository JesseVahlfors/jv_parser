from typing import Any, Dict, Union, List
from scanner import Scanner, Token, TokenType

JSONValue = Union[str, int, float, bool, None, 'JSONObject', 'JSONArray']
JSONObject = Dict[str, JSONValue]
JSONArray = List[JSONValue]


def parse(json_string: str) -> JSONValue:
    scanner = Scanner(json_string)
    tokens = scanner.scan_tokens()

    #def parse_object(scanner: Scanner) -> JSONObject:

    #def consume(scanner: Scanner, token_type: TokenType) -> Token:

    #def error(token: Token, message: str) -> None:

    def parse_value(scanner: Scanner) -> JSONValue:
        token = scanner.tokens[scanner.current_position]
        match token.token_type:
            case TokenType.LBRACE:
                return parse_object(scanner)

    return parse_value(scanner)

    
    
