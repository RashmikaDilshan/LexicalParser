class GrammarRule:
    """Represents a single production rule in the grammar"""
    
    def __init__(self, lhs, rhs, description=""):
        self.lhs = lhs  # Left-hand side (non-terminal)
        self.rhs = rhs  # Right-hand side (can be list of alternatives)
        self.description = description
    
    def __repr__(self):
        return f"{self.lhs} → {self.rhs}"
    
    def to_dict(self):
        return {
            'lhs': self.lhs,
            'rhs': self.rhs,
            'description': self.description
        }

# Grammar Productions for Programming Language
GRAMMAR_RULES = [
    # Program structure
    GrammarRule('Program', "StatementList", "Program: Sequence of statements"),
    GrammarRule('StatementList', "Statement StatementList | ε", "Statement List: Zero or more statements"),
    
    # Statements
    GrammarRule('Statement', "Assignment | IfStatement | WhileStatement | ForStatement | FunctionDef | ReturnStatement | Block", 
                "Statement: Various statement types"),
    GrammarRule('Assignment', "id = E ;", "Assignment: Variable assignment"),
    GrammarRule('Block', "{ StatementList }", "Block: Group of statements in braces"),
    
    # Control flow - If statement
    GrammarRule('IfStatement', "if ( Condition ) Statement ElsePart", 
                "If Statement: Conditional execution"),
    GrammarRule('ElsePart', "else Statement | ε", "Else Part: Optional else clause"),
    
    # Control flow - While loop
    GrammarRule('WhileStatement', "while ( Condition ) Statement", 
                "While Statement: Loop with condition"),
    
    # Control flow - For loop
    GrammarRule('ForStatement', "for ( Assignment Condition ; Assignment ) Statement", 
                "For Statement: Traditional for loop"),
    
    # Function definition
    GrammarRule('FunctionDef', "def id ( ParamList ) Block", 
                "Function Definition: Named function with parameters"),
    GrammarRule('ParamList', "id ParamListTail | ε", "Parameter List: Function parameters"),
    GrammarRule('ParamListTail', ", id ParamListTail | ε", "Parameter List Tail: Additional parameters"),
    
    # Return statement
    GrammarRule('ReturnStatement', "return E ; | return ;", 
                "Return Statement: Return value from function"),
    
    # Conditions (Comparison expressions)
    GrammarRule('Condition', "E RelOp E", "Condition: Comparison between expressions"),
    GrammarRule('RelOp', "< | > | <= | >= | == | !=", 
                "Relational Operator: Comparison operators"),
    
    # Arithmetic Expressions (Left-factored and left-recursion eliminated)
    GrammarRule('E', "TE'", "Expression: Term followed by Expression Prime"),
    GrammarRule("E'", "+TE' | -TE' | ε", 
                "Expression Prime: Add/Sub operations or epsilon"),
    
    GrammarRule('T', "FT'", "Term: Factor followed by Term Prime"),
    GrammarRule("T'", "*FT' | /FT' | %FT' | ε", 
                "Term Prime: Mul/Div/Mod operations or epsilon"),
    
    GrammarRule('F', "P**F | P", "Factor: Power operation (right-associative) or Primary"),
    
    GrammarRule('P', "(E) | id FunctionCall | number", 
                "Primary: Parenthesized expr, function call, identifier, or number"),
    
    # Function calls
    GrammarRule('FunctionCall', "( ArgList ) | ε", 
                "Function Call: Optional function invocation"),
    GrammarRule('ArgList', "E ArgListTail | ε", "Argument List: Function arguments"),
    GrammarRule('ArgListTail', ", E ArgListTail | ε", 
                "Argument List Tail: Additional arguments"),
    
    # Lexical rules
    GrammarRule('id', "letter (letter | digit | _)*", 
                "Identifier: Starts with letter/underscore"),
    GrammarRule('number', "digit+ | digit+.digit+", 
                "Number: Integer or floating-point"),
    GrammarRule('letter', "a-z | A-Z | _", "Letter: Alphabetic character or underscore"),
    GrammarRule('digit', "0-9", "Digit: Numeric character"),
]

# Non-terminals in the grammar
NON_TERMINALS = [
    'Program', 'StatementList', 'Statement', 'Assignment', 'Block',
    'IfStatement', 'ElsePart', 'WhileStatement', 'ForStatement',
    'FunctionDef', 'ParamList', 'ParamListTail', 'ReturnStatement',
    'Condition', 'RelOp', 'E', "E'", 'T', "T'", 'F', 'P',
    'FunctionCall', 'ArgList', 'ArgListTail'
]

# Terminals in the grammar
TERMINALS = [
    '+', '-', '*', '/', '%', '**', '(', ')', '{', '}', ';', ',', '=',
    '<', '>', '<=', '>=', '==', '!=',
    'if', 'else', 'while', 'for', 'def', 'return',
    'id', 'number', 'ε'
]

def get_grammar_rules():
    """Returns all grammar rules as a list of dictionaries"""
    return [rule.to_dict() for rule in GRAMMAR_RULES]

def get_grammar_as_string():
    """Returns grammar as formatted string"""
    lines = []
    for rule in GRAMMAR_RULES:
        lines.append(f"{rule.lhs} → {rule.rhs}")
    return '\n'.join(lines)

def is_terminal(symbol):
    """Check if a symbol is a terminal"""
    return symbol in TERMINALS or symbol not in NON_TERMINALS

def is_non_terminal(symbol):
    """Check if a symbol is a non-terminal"""
    return symbol in NON_TERMINALS

# Grammar explanation for documentation
GRAMMAR_EXPLANATION = """
This grammar defines a complete programming language with:

1. Program Structure:
   - Program consists of a list of statements
   - Statements can be assignments, control flow, functions, or blocks

2. Control Flow:
   - If statements with optional else clause
   - While loops
   - For loops with initialization, condition, and increment

3. Functions:
   - Function definitions with parameters
   - Function calls with arguments
   - Return statements

4. Expressions:
   - Arithmetic expressions with proper precedence
   - Comparison operators for conditions
   - Function calls within expressions

5. Operator Precedence (from highest to lowest):
   - ** (exponentiation) - right associative
   - *, /, % (multiplication, division, modulo) - left associative
   - +, - (addition, subtraction) - left associative
   - <, >, <=, >=, ==, != (comparison) - non-associative

Example Programs:
1. Simple assignment:
   x = 5;

2. If statement:
   if (x > 0) {
       y = x * 2;
   } else {
       y = 0;
   }

3. Function definition:
   def factorial(n) {
       if (n <= 1) {
           return 1;
       } else {
           return n * factorial(n - 1);
       }
   }

4. For loop:
   for (i = 0; i < 10; i = i + 1) {
       sum = sum + i;
   }
"""

def get_grammar_explanation():
    """Returns detailed explanation of the grammar"""
    return GRAMMAR_EXPLANATION