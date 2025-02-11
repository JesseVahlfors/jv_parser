from enum import StrEnum, auto
from typing import Any

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

class Scanner:
    def __init__(self, json_string: str):
        self.json_string = json_string
        self.start = 0
        self.current_position = 0
        self.tokens = []
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current_position
            self.scan_token()
            self.tokens.append(Token(TokenType.EOF))
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
            case ' ':
                pass

             
    def advance(self) -> str:
        char = self.json_string[self.current_position]
        self.current_position += 1
        return char
    
    #def add_string(self):
     

    #def add_number(self):
       
    
    #def add_keyword(self):
        

    #def get_char(self) -> str:
       

    #def get_next_char(self) -> str:
