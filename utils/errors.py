class ErrorType:
    """Enumeration of error types"""
    LEXICAL = "Lexical Error"
    SYNTAX = "Syntax Error"
    SEMANTIC = "Semantic Error"

class CompilerError:
    """Represents a compilation error with details"""
    
    def __init__(self, error_type, message, line=None, column=None, suggestion=None):
        self.type = error_type
        self.message = message
        self.line = line
        self.column = column
        self.suggestion = suggestion
    
    def __repr__(self):
        location = ""
        if self.line is not None:
            location = f" at line {self.line}"
            if self.column is not None:
                location += f", column {self.column}"
        return f"{self.type}{location}: {self.message}"
    
    def to_dict(self):
        """Convert error to dictionary"""
        return {
            'type': self.type,
            'message': self.message,
            'line': self.line,
            'column': self.column,
            'suggestion': self.suggestion
        }

class ErrorHandler:
    """Manages and formats compilation errors"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def add_error(self, error):
        """Add a compilation error"""
        self.errors.append(error)
    
    def add_warning(self, message):
        """Add a warning"""
        self.warnings.append(message)
    
    def has_errors(self):
        """Check if any errors were recorded"""
        return len(self.errors) > 0
    
    def get_error_count(self):
        """Get total number of errors"""
        return len(self.errors)
    
    def get_errors_as_dict(self):
        """Get all errors as list of dictionaries"""
        return [error.to_dict() for error in self.errors]
    
    def format_errors(self):
        """Format all errors as readable string"""
        if not self.errors:
            return "No errors found."
        
        lines = [f"Found {len(self.errors)} error(s):"]
        for i, error in enumerate(self.errors, 1):
            lines.append(f"{i}. {str(error)}")
            if error.suggestion:
                lines.append(f"   Suggestion: {error.suggestion}")
        
        return "\n".join(lines)
    
    def clear(self):
        """Clear all errors and warnings"""
        self.errors.clear()
        self.warnings.clear()

def detect_common_errors(input_string, tokens=None):
    """
    Detect common programming errors and provide suggestions
    """
    errors = []
    
    # Check for unbalanced braces
    open_brace = input_string.count('{')
    close_brace = input_string.count('}')
    if open_brace != close_brace:
        if open_brace > close_brace:
            errors.append(CompilerError(
                ErrorType.SYNTAX,
                f"Missing {open_brace - close_brace} closing brace(s)",
                suggestion="Add '}' to match opening braces"
            ))
        else:
            errors.append(CompilerError(
                ErrorType.SYNTAX,
                f"Extra {close_brace - open_brace} closing brace(s)",
                suggestion="Remove extra '}' or add matching '{'"
            ))
    
    # Check for unbalanced parentheses
    open_paren = input_string.count('(')
    close_paren = input_string.count(')')
    if open_paren != close_paren:
        if open_paren > close_paren:
            errors.append(CompilerError(
                ErrorType.SYNTAX,
                f"Missing {open_paren - close_paren} closing parenthesis/parentheses",
                suggestion="Add ')' to match opening parentheses"
            ))
        else:
            errors.append(CompilerError(
                ErrorType.SYNTAX,
                f"Extra {close_paren - open_paren} closing parenthesis/parentheses",
                suggestion="Remove extra ')' or add matching '('"
            ))
    
    # Check for statements without semicolons
    if tokens:
        for i, token in enumerate(tokens):
            # Check if assignment is followed by semicolon
            if token.type == 'ASSIGN':
                # Find the end of the expression
                j = i + 1
                depth = 0
                while j < len(tokens):
                    if tokens[j].type in ['LPAREN', 'LBRACE']:
                        depth += 1
                    elif tokens[j].type in ['RPAREN', 'RBRACE']:
                        depth -= 1
                    elif tokens[j].type == 'SEMICOLON' and depth == 0:
                        break
                    elif tokens[j].type in ['IF', 'WHILE', 'FOR', 'DEF'] and depth == 0:
                        errors.append(CompilerError(
                            ErrorType.SYNTAX,
                            "Missing semicolon after assignment",
                            line=token.line,
                            column=token.column,
                            suggestion="Add ';' at the end of the assignment"
                        ))
                        break
                    j += 1
        
        # Check for division by zero
        for i, token in enumerate(tokens):
            if token.type == 'DIVIDE' and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token.type == 'NUMBER' and next_token.value == 0:
                    errors.append(CompilerError(
                        ErrorType.SEMANTIC,
                        "Division by zero",
                        line=token.line,
                        column=token.column,
                        suggestion="Avoid dividing by zero"
                    ))
    
    # Check for empty blocks
    if '{}' in input_string:
        errors.append(CompilerError(
            ErrorType.SYNTAX,
            "Empty block detected",
            suggestion="Add statements inside braces or remove the block"
        ))
    
    # Check for empty parentheses in conditions
    if '()' in input_string and 'def' not in input_string:
        errors.append(CompilerError(
            ErrorType.SYNTAX,
            "Empty parentheses in condition or expression",
            suggestion="Add an expression inside parentheses"
        ))
    
    return errors

def get_error_suggestions(error_message):
    """
    Provide helpful suggestions based on error message
    """
    suggestions = {
        'Unexpected character': "Check for invalid symbols or special characters",
        'Expected': "Verify the syntax matches the grammar rules",
        'Missing closing': "Add the appropriate closing delimiter",
        'Unexpected token': "Check statement structure and syntax",
        'Missing semicolon': "Add ';' at the end of the statement",
    }
    
    for key, suggestion in suggestions.items():
        if key in error_message:
            return suggestion
    
    return "Review the grammar rules and syntax"