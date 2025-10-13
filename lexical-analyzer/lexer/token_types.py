class TokenType:
    """Enumeration of all token types"""
    
    # Operators
    PLUS = 'PLUS'           # +
    MINUS = 'MINUS'         # -
    MULTIPLY = 'MULTIPLY'   # *
    DIVIDE = 'DIVIDE'       # /
    MODULO = 'MODULO'       # %
    POWER = 'POWER'         # **
    
    # Comparison operators
    LT = 'LT'               # <
    GT = 'GT'               # >
    LE = 'LE'               # <=
    GE = 'GE'               # >=
    EQ = 'EQ'               # ==
    NE = 'NE'               # !=
    
    # Delimiters
    LPAREN = 'LPAREN'       # (
    RPAREN = 'RPAREN'       # )
    LBRACE = 'LBRACE'       # {
    RBRACE = 'RBRACE'       # }
    SEMICOLON = 'SEMICOLON' # ;
    COMMA = 'COMMA'         # ,
    
    # Assignment
    ASSIGN = 'ASSIGN'       # =
    
    # Keywords
    IF = 'IF'               # if
    ELSE = 'ELSE'           # else
    WHILE = 'WHILE'         # while
    FOR = 'FOR'             # for
    DEF = 'DEF'             # def
    RETURN = 'RETURN'       # return
    
    # Identifiers and Literals
    ID = 'ID'               # Variable names
    NUMBER = 'NUMBER'       # Numeric literals
    
    # Special
    EOF = 'EOF'             # End of file

class Token:
    """Represents a single token with type, value, and position"""
    
    def __init__(self, token_type, value, lexeme, line=1, column=0):
        self.type = token_type
        self.value = value
        self.lexeme = lexeme
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.lexeme}', line={self.line}, col={self.column})"
    
    def to_dict(self):
        """Convert token to dictionary for JSON serialization"""
        return {
            'type': self.type,
            'value': self.value,
            'lexeme': self.lexeme,
            'line': self.line,
            'column': self.column
        }

# Keywords mapping
KEYWORDS = {
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'def': TokenType.DEF,
    'return': TokenType.RETURN
}

# Operator precedence
PRECEDENCE = {
    '**': 3,  # Exponentiation (right associative)
    '*': 2, '/': 2, '%': 2,  # Multiplication, Division, Modulo
    '+': 1, '-': 1,  # Addition, Subtraction
    '<': 0, '>': 0, '<=': 0, '>=': 0, '==': 0, '!=': 0  # Comparison
}

def get_token_category(token_type):
    """Returns the category of a given token type"""
    operators = ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO', 'POWER',
                 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE']
    delimiters = ['LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA']
    keywords = ['IF', 'ELSE', 'WHILE', 'FOR', 'DEF', 'RETURN']
    
    if token_type in operators:
        return 'Operator'
    elif token_type in delimiters:
        return 'Delimiter'
    elif token_type in keywords:
        return 'Keyword'
    elif token_type == 'ID':
        return 'Identifier'
    elif token_type == 'NUMBER':
        return 'Literal'
    elif token_type == 'ASSIGN':
        return 'Assignment'
    else:
        return 'Unknown'

