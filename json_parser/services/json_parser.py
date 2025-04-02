from typing import Any, Dict, Union, List
from .scanner import Scanner, Token, TokenType

JSONValue = Union[str, int, float, bool, None, 'JSONObject', 'JSONArray']
JSONObject = Dict[str, JSONValue]
JSONArray = List[JSONValue]


def parse(json_string: str) -> JSONValue:
    if not isinstance(json_string, str):
        raise Exception("Invalid JSON: Input must be a valid JSON string")
    if not json_string:
        raise Exception("Invalid JSON: Input must be a valid JSON string")
    
    scanner = Scanner(json_string)
    tokens = scanner.scan_tokens()


    def parse_object(scanner: Scanner, depth=0) -> JSONObject:
        obj = {}
        consume(scanner, TokenType.LBRACE)
        if scanner.tokens[scanner.current_position].token_type == TokenType.RBRACE:
            consume(scanner, TokenType.RBRACE)
            return obj
        while scanner.tokens[scanner.current_position].token_type != TokenType.RBRACE:
            key = consume(scanner, TokenType.STRING).value
            consume(scanner, TokenType.COLON)
            value = parse_value(scanner, depth + 1)
            obj[key] = value

            next_token = scanner.tokens[scanner.current_position].token_type

            if next_token == TokenType.COMMA:
                consume(scanner, TokenType.COMMA)
                if scanner.tokens[scanner.current_position].token_type == TokenType.RBRACE:
                    return error(scanner.tokens[scanner.current_position], "Unexpected trailing comma")
            elif next_token == TokenType.RBRACE:
                break
            else:
                return error(scanner.tokens[scanner.current_position], "Expected ',' or '}', but found something else.")
           
        consume(scanner, TokenType.RBRACE)
        return obj
    
    def parse_array(scanner: Scanner, depth=0) -> JSONArray:
        arr = []
        consume(scanner, TokenType.LBRACKET)
        if scanner.tokens[scanner.current_position].token_type == TokenType.RBRACKET:
            consume(scanner, TokenType.RBRACKET)
            return arr
        while scanner.tokens[scanner.current_position].token_type != TokenType.RBRACKET:
            value = parse_value(scanner, depth + 1)
            arr.append(value)
            if scanner.tokens[scanner.current_position].token_type == TokenType.COMMA:
                consume(scanner, TokenType.COMMA)
                if scanner.tokens[scanner.current_position].token_type == TokenType.RBRACKET:
                    return error(scanner.tokens[scanner.current_position], "Unexpected trailing comma")
        consume(scanner, TokenType.RBRACKET)
        return arr

    def consume(scanner: Scanner, token_type: TokenType) -> Token:
        if scanner.current_position >= len(scanner.tokens):
            return error(None, "Unexpected end of input")
        if scanner.tokens[scanner.current_position].token_type == token_type:
            token = scanner.tokens[scanner.current_position]
            scanner.current_position += 1
            return token
        else:
            return error(scanner.tokens[scanner.current_position], f"Expected {token_type}")

    def error(token: Token, message: str) -> None:
        if token is None or token.token_type == TokenType.EOF:
            raise Exception("Invalid JSON: Unexpected end of input.")
        raise Exception(f"Invalid JSON: {message} at line {scanner.line} and index {scanner.current_position}, token type: {token.token_type}.")
    
    MAX_DEPTH = 20  # Maximum depth for nested structures

    def parse_value(scanner: Scanner, depth=0) -> JSONValue:
        if scanner.current_position >= len(scanner.tokens):
            return error(None, "Unexpected end of input")
        if scanner.tokens[scanner.current_position].token_type in {TokenType.LBRACKET, TokenType.LBRACE}:
            if depth > MAX_DEPTH:
                return error(scanner.tokens[scanner.current_position], "Maximum depth exceeded. Maximum depth is 20.")
               
        token = scanner.tokens[scanner.current_position]
        match token.token_type:
            case TokenType.LBRACE:
                return parse_object(scanner, depth + 1)
            case TokenType.LBRACKET:
                return parse_array(scanner, depth + 1)
            case TokenType.STRING:
                return consume(scanner, TokenType.STRING).value
            case TokenType.NUMBER:
                num = consume(scanner, TokenType.NUMBER).value
                if "." not in num and "e" not in num:
                    return int(num)
                else:
                    return float(num)
            case TokenType.BOOLEAN:
                return consume(scanner, TokenType.BOOLEAN).value
            case TokenType.NULL:
                return consume(scanner, TokenType.NULL).value
            case _:
                return error(token, f"Unexpected input at line {scanner.line}.")
            
    result = parse_value(scanner)

    if scanner.current_position < len(scanner.tokens) - 1: #check for extra tokens after main object/array closed
        extra_token = scanner.tokens[scanner.current_position]
        raise Exception(f"Invalid JSON: Extra value after close at line {scanner.line}, token type: {extra_token.token_type}.")
    
    if isinstance(result, str) and result.startswith("Invalid JSON"):
        return result
            
    return result

    
    
