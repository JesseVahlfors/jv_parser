from typing import Any, Dict, Union, List
from .scanner import Scanner, Token, TokenType

JSONValue = Union[str, int, float, bool, None, 'JSONObject', 'JSONArray']
JSONObject = Dict[str, JSONValue]
JSONArray = List[JSONValue]


def parse(json_string: str) -> JSONValue:
    if not isinstance(json_string, str):
        raise ValueError("Invalid JSON: Input must be a valid JSON string")
    
    scanner = Scanner(json_string)
    tokens = scanner.scan_tokens()
    def parse_object(scanner: Scanner) -> JSONObject:
        obj = {}
        consume(scanner, TokenType.LBRACE)
        if scanner.tokens[scanner.current_position].token_type == TokenType.RBRACE:
            consume(scanner, TokenType.RBRACE)
            return obj
        while scanner.tokens[scanner.current_position].token_type != TokenType.RBRACE:
            key = consume(scanner, TokenType.STRING).value
            consume(scanner, TokenType.COLON)
            value = parse_value(scanner)
            obj[key] = value
            if scanner.tokens[scanner.current_position].token_type == TokenType.COMMA:
                consume(scanner, TokenType.COMMA)

                if scanner.tokens[scanner.current_position].token_type == TokenType.RBRACE:
                    return error(scanner.tokens[scanner.current_position], "Unexpected trailing comma")
        consume(scanner, TokenType.RBRACE)
        return obj
    
    #def parse_array(scanner: Scanner) -> JSONArray:
    

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
            return f"Invalid JSON: Unexpected end of input."
        return f"Invalid JSON: {message} at line {scanner.line}, token type: {token.token_type}."

    def parse_value(scanner: Scanner) -> JSONValue:
        if scanner.current_position >= len(scanner.tokens):
            return error(None, "Unexpected end of input")
        token = scanner.tokens[scanner.current_position]
        match token.token_type:
            case TokenType.LBRACE:
                return parse_object(scanner)
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
            #case TokenType.LBRACKET:
            case _:
                return error(token, f"Unexpected input at line {scanner.line}.")
            
    result = parse_value(scanner)
    if isinstance(result, str) and result.startswith("Invalid JSON"):
        return result
            
    return result

    
    
