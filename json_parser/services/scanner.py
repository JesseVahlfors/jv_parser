from enum import StrEnum, auto
from typing import Any, List

class TokenType(StrEnum): 
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    NULL = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    EOF = auto()

class Token:
    def __init__(self, token_type: TokenType, value: Any):
        self.token_type = token_type
        self.value = value
    
    def __str__(self):
        return f"{self.token_type}: {self.value}"
    
    def __repr__(self):
        return self.__str__()

class Scanner:
    def __init__(self, json_string: str):
        self.json_string = json_string
        self.start = 0
        self.current_position = 0
        self.tokens: List[Token] = []
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current_position
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, None))
        self.current_position = 0
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.json_string)
    
    def scan_token(self):
        char = self.advance()
        match char:
            case '{':
                self.tokens.append(Token(TokenType.LBRACE, char))
            case '}':
                self.tokens.append(Token(TokenType.RBRACE, char))
            case ':':
                self.tokens.append(Token(TokenType.COLON, char))
            case ' ' | '\n' | '\r' | '\t':
                pass
            case '"':
                self.add_string()
            case ',':
                self.tokens.append(Token(TokenType.COMMA, char))
            case ' ':
                pass
            case _:
                if char.isdigit():
                    self.add_number()
                elif char.isalpha():
                    self.add_keyword()
                else:
                    raise Exception(f"Unexpected character: {char}.")

             
    def advance(self) -> str:
        char = self.json_string[self.current_position]
        self.current_position += 1
        return char
    
    def add_string(self):
        value = ""
        while not self.is_at_end() and self.peek() != '"':
            value += self.advance()
        self.advance() # consume closing quote
        self.tokens.append(Token(TokenType.STRING, value))
     

    def add_number(self):
        value = self.json_string[self.start]
        while not self.is_at_end() and self.peek().isdigit():
            value += self.advance()
        self.tokens.append(Token(TokenType.NUMBER, value))
       
    
    def add_keyword(self):
        value = self.json_string[self.start]
        while not self.is_at_end() and self.peek().isalnum():
            value += self.advance()
        if value == "true" or value == "false":
            value = True if value == "true" else False
            self.tokens.append(Token(TokenType.BOOLEAN, value))
        elif value == "null":
            value = None
            self.tokens.append(Token(TokenType.NULL, value))
        else:
            raise Exception(f"Unexpected keyword: {value}.")
        

    def peek(self) -> str:
        if self.is_at_end():
            return "\0" # return null character
        return self.json_string[self.current_position]
