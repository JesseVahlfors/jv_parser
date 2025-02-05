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
            case '[':
                self.tokens.append(Token(TokenType.LBRACKET, char))
            case ']':
                self.tokens.append(Token(TokenType.RBRACKET, char))
            case ',':
                self.tokens.append(Token(TokenType.COMMA, char))
            case ':':
                self.tokens.append(Token(TokenType.COLON, char))
            case '\n':
                self.line += 1
            case ' ':
                pass
            case '"':
                self.add_string()
            case '-':
                if self.get_char().isDigit():
                    self.advance()
                    self.add_number()
                else:
                    raise ValueError(f"Invalid character {char} at line {self.line}")
            case _:
                if char.isdigit():
                    self.add_number()
                elif char.isalpha():
                    self.add_keyword()
                else:
                    raise ValueError(f"Invalid character {char} at line {self.line}")
             
    def advance(self) -> str:
        char = self.json_string[self.current_position]
        self.current_position += 1
        return char
    
    def add_string(self):
        while self.get_char() != '"' and not self.is_at_end():
            if self.get_char() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            raise ValueError(f"Unterminated string at line {self.line}")
        self.advance()
        self.tokens.append(Token(TokenType.STRING, self.json_string[self.start+1:self.current_position-1]))

    def add_number(self):
        while self.get_char().isdigit():
            self.advance()
        if self.get_char() == '.':
            if not self.get_next_char().isdigit():
                raise ValueError(f"Expected digit after . (trying to parse float()) at line {self.line}")
            #Skip the . character
            self.advance()

            while self.get_char().isDigit():
                self.advance()
            self.tokens.append(
                Token(TokenType.NUMBER, float(self.json_string[self.start:self.current_position]))
                )
        else:
            self.tokens.append(
                Token(TokenType.NUMBER, int(self.json_string[self.start:self.current_position]))
                )
    
    def add_keyword(self):
        while self.get_char().isAlpha():
            self.advance()
        keyword = self.json_string[self.start:self.current_position]
        match keyword:
            case 'true':
                self.tokens.append(Token(TokenType.BOOLEAN, True))
            case 'false':
                self.tokens.append(Token(TokenType.BOOLEAN, False))
            case 'null':
                self.tokens.append(Token(TokenType.NULL, None))
            case _:
                raise ValueError(f"Invalid keyword {keyword} at line {self.line}")

    def get_char(self) -> str:
        if self.is_at_end():
            return ''
        return self.json_string[self.current_position]

    def get_next_char(self) -> str:
        if self.current_position + 1 >= len(self.json_string):
            return ''
        return self.json_string[self.current_position + 1]