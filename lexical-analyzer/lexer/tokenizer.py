import re
from .token_types import Token, TokenType, KEYWORDS

class LexicalError(Exception):
    """Custom exception for lexical errors"""
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.message)

class Tokenizer:
    """Enhanced Lexical Analyzer"""
    
    def __init__(self, input_string):
        self.input = input_string
        self.pos = 0
        self.line = 1
        self.column = 0
        self.tokens = []
        self.errors = []
    
    def current_char(self):
        """Returns the current character or None if at end"""
        if self.pos < len(self.input):
            return self.input[self.pos]
        return None
    
    def peek_char(self, offset=1):
        """Look ahead at character without consuming it"""
        pos = self.pos + offset
        if pos < len(self.input):
            return self.input[pos]
        return None
    
    def advance(self):
        """Move to the next character"""
        if self.pos < len(self.input):
            if self.input[self.pos] == '\n':
                self.line += 1
                self.column = 0
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        """Skip over whitespace characters"""
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def read_number(self):
        """Read a numeric literal"""
        start_column = self.column
        num_str = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    self.errors.append(f"Invalid number format at line {self.line}, column {self.column}")
                    break
                has_dot = True
            num_str += self.current_char()
            self.advance()
        
        if num_str.endswith('.'):
            self.errors.append(f"Invalid number format '{num_str}' at line {self.line}, column {start_column}")
        
        return Token(TokenType.NUMBER, float(num_str) if has_dot else int(num_str),
                    num_str, self.line, start_column)
    
    def read_identifier_or_keyword(self):
        """Read an identifier or keyword"""
        start_column = self.column
        id_str = ''
        
        # First character must be letter or underscore
        if self.current_char() and (self.current_char().isalpha() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        # Subsequent characters can be letters, digits, or underscores
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = KEYWORDS.get(id_str, TokenType.ID)
        return Token(token_type, id_str, id_str, self.line, start_column)
    
    def tokenize(self):
        """Main tokenization method"""
        self.tokens = []
        self.errors = []
        
        while self.pos < len(self.input):
            self.skip_whitespace()
            
            if self.pos >= len(self.input):
                break
            
            char = self.current_char()
            start_column = self.column
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identifiers and Keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier_or_keyword())
                continue
            
            # Two-character operators
            if char == '*' and self.peek_char() == '*':
                self.tokens.append(Token(TokenType.POWER, '**', '**', self.line, start_column))
                self.advance()
                self.advance()
            elif char == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LE, '<=', '<=', self.line, start_column))
                self.advance()
                self.advance()
            elif char == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GE, '>=', '>=', self.line, start_column))
                self.advance()
                self.advance()
            elif char == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQ, '==', '==', self.line, start_column))
                self.advance()
                self.advance()
            elif char == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NE, '!=', '!=', self.line, start_column))
                self.advance()
                self.advance()
            # Single-character operators and delimiters
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', '+', self.line, start_column))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', '-', self.line, start_column))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', '*', self.line, start_column))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', '/', self.line, start_column))
                self.advance()
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, '%', '%', self.line, start_column))
                self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.LT, '<', '<', self.line, start_column))
                self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.GT, '>', '>', self.line, start_column))
                self.advance()
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', '=', self.line, start_column))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', '(', self.line, start_column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', ')', self.line, start_column))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', '{', self.line, start_column))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', '}', self.line, start_column))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', ';', self.line, start_column))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', ',', self.line, start_column))
                self.advance()
            else:
                error_msg = f"Unexpected character '{char}' at line {self.line}, column {start_column}"
                self.errors.append(error_msg)
                raise LexicalError(error_msg, self.line, start_column)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, 'EOF', '', self.line, self.column))
        return self.tokens
    
    def get_tokens_as_dict(self):
        """Return tokens as list of dictionaries"""
        return [token.to_dict() for token in self.tokens]

def tokenize_input(input_string):
    """Convenience function to tokenize an input string"""
    tokenizer = Tokenizer(input_string)
    try:
        tokens = tokenizer.tokenize()
        return tokens, []
    except LexicalError as e:
        return [], [str(e)]