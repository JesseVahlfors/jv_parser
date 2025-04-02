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
        # Check that the string starts with a object or array
        if not self.is_at_end(): 
            first_char = self.json_string[0]
            if first_char != '{' and first_char != '[':
                raise Exception("Invalid JSON: JSON must start with an object or array.")
            
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
            case '[':
                self.tokens.append(Token(TokenType.LBRACKET, char))
            case ']':
                self.tokens.append(Token(TokenType.RBRACKET, char))
            case ':':
                self.tokens.append(Token(TokenType.COLON, char))
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1
            case '"':
                self.add_string()
            case ',':
                self.tokens.append(Token(TokenType.COMMA, char))
            case ' ':
                pass
            case _:
                if char.isdigit() or char == '-':
                    self.add_number()
                elif char.isalpha():
                    self.add_keyword()
                else:
                    raise Exception(f"Unexpected character: {char} at line {self.line}.")

             
    def advance(self) -> str:
        char = self.json_string[self.current_position]
        self.current_position += 1
        return char
    
    def add_string(self):
        value = ""
        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == '\\':
                self.advance()
                if self.is_at_end():
                    raise Exception("Invalid JSON: Unexpected end of input in string.")
                escape_char = self.advance()
                if escape_char not in ('"', '\\', '/', 'b', 'f', 'n', 'r', 't'):
                    raise Exception(f"Invalid JSON: Illegal backslash escape {escape_char} at line {self.line}.")
                if escape_char == 'u':
                    hex_digits = ""
                    for _ in range(4):
                        if self.is_at_end() or not self.peek().isalnum():
                            raise Exception("Invalid JSON: Invalid unicode escape sequence.")
                        hex_digits += self.advance()
                    try:
                        value += chr(int(hex_digits, 16))
                    except ValueError:
                        raise Exception("Invalid JSON: Invalid unicode escape sequence.")
                else:
                    escape_map = {
                        '"': '"',
                        '\\': '\\',
                        '/': '/',
                        'b': '\b',
                        'f': '\f',
                        'n': '\n',
                        'r': '\r',
                        't': '\t'
                    }
                    value += escape_map[escape_char]
            else:
                char = self.advance()

                if ord(char) < 0x20:
                    raise Exception(f"Invalid JSON: Control character at line {self.line}.")
                
                value += char


        if self.is_at_end():
            raise Exception("Invalid JSON: Unexpected end of input in string.")
            
        self.advance() # consume closing quote
        self.tokens.append(Token(TokenType.STRING, value))
     
    def add_number(self):
        value = self.json_string[self.current_position - 1] # start with the first digit
        if value == '0' and not self.is_at_end() and self.peek().isdigit():
            raise Exception("Invalid JSON: Leading zeros in number.")
        
        if self.peek() == '-':
            value += self.advance()
            if self.peek() == '0':
                raise Exception("Invalid JSON: Leading zeros in number.")

        while not self.is_at_end() and self.peek().isdigit():
                value += self.advance()
        
        if not self.is_at_end() and self.peek() == '.':
            value += self.advance()
            while not self.is_at_end() and self.peek().isdigit():
                value += self.advance()

        if not self.is_at_end() and self.peek() in ('e', 'E'):
            value += self.advance()
            if not self.is_at_end() and self.peek() in ('+', '-'):
                value += self.advance()

        self.tokens.append(Token(TokenType.NUMBER, value))
       
    
    def add_keyword(self):
        value = self.json_string[self.current_position - 1] # start with the first character
        while not self.is_at_end() and self.peek().isalnum():
            value += self.advance()
        if value == "true" or value == "false":
            value = True if value == "true" else False
            self.tokens.append(Token(TokenType.BOOLEAN, value))
        elif value == "null":
            value = None
            self.tokens.append(Token(TokenType.NULL, value))
        else:
            raise Exception(f"Unexpected keyword: {value} at line {self.line}. Keywords must be 'true', 'false', or 'null'.")
        

    def peek(self) -> str:
        if self.is_at_end():
            return "\0" # return null character
        return self.json_string[self.current_position]
