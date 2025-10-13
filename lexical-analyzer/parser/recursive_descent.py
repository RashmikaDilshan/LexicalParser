from lexer.token_types import TokenType
from .parse_tree import ParseTreeNode

class SyntaxError(Exception):
    """Custom exception for syntax errors"""
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(self.message)

class RecursiveDescentParser:
    """Enhanced Recursive Descent Parser"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self.parse_tree = None
    
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]
    
    def peek_token(self, offset=1):
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def eat(self, token_type):
        current = self.current_token()
        if current.type == token_type:
            self.pos += 1
            return current
        else:
            error_msg = f"Expected {token_type} but got {current.type} at line {current.line}, column {current.column}"
            self.errors.append(error_msg)
            return None
    
    def parse(self):
        try:
            self.parse_tree = self.parse_Program()
            if self.current_token().type != TokenType.EOF:
                self.errors.append(f"Unexpected token '{self.current_token().lexeme}' after program")
            success = len(self.errors) == 0
            return self.parse_tree, success, self.errors
        except Exception as e:
            self.errors.append(f"Parser Error: {str(e)}")
            return self.parse_tree, False, self.errors

    
    
    # Grammar production methods
    def parse_Program(self):
        node = ParseTreeNode('Program')
        stmt_list = self.parse_StatementList()
        if stmt_list:
            node.add_child(stmt_list)
        return node
    
    def parse_StatementList(self):
        node = ParseTreeNode('StatementList')
        if self.current_token().type in [TokenType.ID, TokenType.IF, TokenType.WHILE, 
                                         TokenType.FOR, TokenType.DEF, TokenType.RETURN, 
                                         TokenType.LBRACE]:
            stmt = self.parse_Statement()
            if stmt:
                node.add_child(stmt)
            stmt_list = self.parse_StatementList()
            if stmt_list:
                node.add_child(stmt_list)
        else:
            node.add_child(ParseTreeNode('ε'))
        return node
    
    def parse_Statement(self):
        node = ParseTreeNode('Statement')
        token = self.current_token()
        if token.type == TokenType.IF:
            node.add_child(self.parse_IfStatement())
        elif token.type == TokenType.WHILE:
            node.add_child(self.parse_WhileStatement())
        elif token.type == TokenType.FOR:
            node.add_child(self.parse_ForStatement())
        elif token.type == TokenType.DEF:
            node.add_child(self.parse_FunctionDef())
        elif token.type == TokenType.RETURN:
            node.add_child(self.parse_ReturnStatement())
        elif token.type == TokenType.LBRACE:
            node.add_child(self.parse_Block())
        elif token.type == TokenType.ID:
            node.add_child(self.parse_Assignment())
        else:
            self.errors.append(f"Unexpected token {token.type} at line {token.line}")
        return node
    
    def parse_Assignment(self):
        node = ParseTreeNode('Assignment')
        id_token = self.eat(TokenType.ID)
        if id_token:
            node.add_child(ParseTreeNode(f"id({id_token.value})"))
        self.eat(TokenType.ASSIGN)
        node.add_child(ParseTreeNode('='))
        expr = self.parse_E()
        if expr:
            node.add_child(expr)
        self.eat(TokenType.SEMICOLON)
        node.add_child(ParseTreeNode(';'))
        return node
    
    def parse_Block(self):
        node = ParseTreeNode('Block')
        self.eat(TokenType.LBRACE)
        node.add_child(ParseTreeNode('{'))
        stmt_list = self.parse_StatementList()
        if stmt_list:
            node.add_child(stmt_list)
        self.eat(TokenType.RBRACE)
        node.add_child(ParseTreeNode('}'))
        return node
    
    def parse_IfStatement(self):
        node = ParseTreeNode('IfStatement')
        self.eat(TokenType.IF)
        node.add_child(ParseTreeNode('if'))
        self.eat(TokenType.LPAREN)
        node.add_child(ParseTreeNode('('))
        cond = self.parse_Condition()
        if cond:
            node.add_child(cond)
        self.eat(TokenType.RPAREN)
        node.add_child(ParseTreeNode(')'))
        stmt = self.parse_Statement()
        if stmt:
            node.add_child(stmt)
        else_part = self.parse_ElsePart()
        if else_part:
            node.add_child(else_part)
        return node
    
    def parse_ElsePart(self):
        node = ParseTreeNode('ElsePart')
        if self.current_token().type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            node.add_child(ParseTreeNode('else'))
            stmt = self.parse_Statement()
            if stmt:
                node.add_child(stmt)
        else:
            node.add_child(ParseTreeNode('ε'))
        return node
    
    def parse_WhileStatement(self):
        node = ParseTreeNode('WhileStatement')
        self.eat(TokenType.WHILE)
        node.add_child(ParseTreeNode('while'))
        self.eat(TokenType.LPAREN)
        node.add_child(ParseTreeNode('('))
        cond = self.parse_Condition()
        if cond:
            node.add_child(cond)
        self.eat(TokenType.RPAREN)
        node.add_child(ParseTreeNode(')'))
        stmt = self.parse_Statement()
        if stmt:
            node.add_child(stmt)
        return node
    
    def parse_ForStatement(self):
        node = ParseTreeNode('ForStatement')
        self.eat(TokenType.FOR)
        node.add_child(ParseTreeNode('for'))
        self.eat(TokenType.LPAREN)
        node.add_child(ParseTreeNode('('))
        # init part: optional assignment
        if self.current_token().type == TokenType.ID:
            init = self.parse_Assignment()
            if init:
                node.add_child(init)
        else:
            # allow empty init (epsilon)
            node.add_child(ParseTreeNode('ε'))

        # expect first semicolon
        self.eat(TokenType.SEMICOLON)
        node.add_child(ParseTreeNode(';'))

        # condition part: optional condition
        if self.current_token().type != TokenType.SEMICOLON:
            cond = self.parse_Condition()
            if cond:
                node.add_child(cond)
        else:
            node.add_child(ParseTreeNode('ε'))

        # expect second semicolon
        self.eat(TokenType.SEMICOLON)
        node.add_child(ParseTreeNode(';'))

        # increment part: optional assignment/expression
        if self.current_token().type == TokenType.ID:
            incr = self.parse_Assignment()
            if incr:
                node.add_child(incr)
        else:
            node.add_child(ParseTreeNode('ε'))
        self.eat(TokenType.RPAREN)
        node.add_child(ParseTreeNode(')'))
        stmt = self.parse_Statement()
        if stmt:
            node.add_child(stmt)
        return node
    
    def parse_FunctionDef(self):
        """FunctionDef → def id ( ParamList ) Block"""
        node = ParseTreeNode('FunctionDef')
        self.eat(TokenType.DEF)
        node.add_child(ParseTreeNode('def'))
        id_token = self.eat(TokenType.ID)
        if id_token:
            node.add_child(ParseTreeNode(f"id({id_token.value})"))
        self.eat(TokenType.LPAREN)
        node.add_child(ParseTreeNode('('))
        param_list = self.parse_ParamList()
        if param_list:
            node.add_child(param_list)
        self.eat(TokenType.RPAREN)
        node.add_child(ParseTreeNode(')'))
        block = self.parse_Block()
        if block:
            node.add_child(block)
        return node
    
    def parse_ParamList(self):
        """ParamList → id , ParamList | id | ε"""
        node = ParseTreeNode('ParamList')
        if self.current_token().type == TokenType.ID:
            id_token = self.eat(TokenType.ID)
            node.add_child(ParseTreeNode(f"id({id_token.value})"))
            if self.current_token().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                node.add_child(ParseTreeNode(','))
                rest = self.parse_ParamList()
                if rest:
                    node.add_child(rest)
        else:
            node.add_child(ParseTreeNode('ε'))
        return node
    
    def parse_ReturnStatement(self):
        """ReturnStatement → return E ;"""
        node = ParseTreeNode('ReturnStatement')
        self.eat(TokenType.RETURN)
        node.add_child(ParseTreeNode('return'))
        # Support both `return;` and `return E;`
        if self.current_token().type == TokenType.SEMICOLON:
            # empty return
            node.add_child(ParseTreeNode('ε'))
        else:
            expr = self.parse_E()
            if expr:
                node.add_child(expr)

        # require terminating semicolon
        self.eat(TokenType.SEMICOLON)
        node.add_child(ParseTreeNode(';'))
        return node
    
    def parse_Assignment(self, require_semicolon=True):
        """Parse Assignment. When used inside for(...), semicolon shouldn't be consumed.
        Assignment -> id = E ;
        If require_semicolon is False the trailing semicolon is not eaten.
        """
        node = ParseTreeNode('Assignment')
        id_token = self.eat(TokenType.ID)
        if id_token:
            node.add_child(ParseTreeNode(f"id({id_token.value})"))
        self.eat(TokenType.ASSIGN)
        node.add_child(ParseTreeNode('='))
        expr = self.parse_E()
        if expr:
            node.add_child(expr)
        if require_semicolon:
            self.eat(TokenType.SEMICOLON)
            node.add_child(ParseTreeNode(';'))
        return node

    # Expression parsing (implements grammar from parser/grammar.py)
    def parse_E(self):
        """E -> T ((+|-) T)*"""
        node = ParseTreeNode('E')
        left = self.parse_T()
        if left:
            node.add_child(left)

        # handle + and - (left associative)
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token()
            self.pos += 1
            op_node = ParseTreeNode(f"op({op.lexeme})")
            right = self.parse_T()
            bin_node = ParseTreeNode('AddSub')
            bin_node.add_child(op_node)
            if right:
                bin_node.add_child(right)
            node.add_child(bin_node)

        return node

    def parse_T(self):
        """T -> F ((*|/|%) F)*"""
        node = ParseTreeNode('T')
        left = self.parse_F()
        if left:
            node.add_child(left)

        while self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.current_token()
            self.pos += 1
            op_node = ParseTreeNode(f"op({op.lexeme})")
            right = self.parse_F()
            bin_node = ParseTreeNode('MulDiv')
            bin_node.add_child(op_node)
            if right:
                bin_node.add_child(right)
            node.add_child(bin_node)

        return node

    def parse_F(self):
        """F -> P (** F)?"""
        node = ParseTreeNode('F')
        primary = self.parse_P()
        if primary:
            node.add_child(primary)

        # right-associative power operator
        if self.current_token().type == TokenType.POWER:
            op = self.eat(TokenType.POWER)
            node.add_child(ParseTreeNode(f"op({op.lexeme})"))
            right = self.parse_F()
            if right:
                node.add_child(right)

        return node

    def parse_P(self):
        """P -> (E) | id FunctionCall | number"""
        node = ParseTreeNode('P')
        tok = self.current_token()
        if tok.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node.add_child(ParseTreeNode('('))
            expr = self.parse_E()
            if expr:
                node.add_child(expr)
            self.eat(TokenType.RPAREN)
            node.add_child(ParseTreeNode(')'))
        elif tok.type == TokenType.ID:
            id_token = self.eat(TokenType.ID)
            node.add_child(ParseTreeNode(f"id({id_token.value})"))
            # possible function call
            if self.current_token().type == TokenType.LPAREN:
                call = self.parse_FunctionCall()
                if call:
                    node.add_child(call)
        elif tok.type == TokenType.NUMBER:
            num_token = self.eat(TokenType.NUMBER)
            node.add_child(ParseTreeNode(f"number({num_token.value})"))
        else:
            # unexpected primary, create error but advance to avoid infinite loop
            self.errors.append(f"Unexpected token in primary: {tok.type} at line {tok.line}")
            self.pos += 1
        return node

    def parse_FunctionCall(self):
        """Parse function call arguments: assumes current token is LPAREN"""
        node = ParseTreeNode('FunctionCall')
        self.eat(TokenType.LPAREN)
        node.add_child(ParseTreeNode('('))
        # arg list: E (, E)* | ε
        if self.current_token().type != TokenType.RPAREN:
            arg = self.parse_E()
            if arg:
                node.add_child(arg)
            while self.current_token().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                node.add_child(ParseTreeNode(','))
                arg = self.parse_E()
                if arg:
                    node.add_child(arg)
        self.eat(TokenType.RPAREN)
        node.add_child(ParseTreeNode(')'))
        return node

    def parse_Condition(self):
        """Condition -> E RelOp E (RelOp is one of <, >, <=, >=, ==, !=)"""
        node = ParseTreeNode('Condition')
        left = self.parse_E()
        if left:
            node.add_child(left)

        if self.current_token().type in (TokenType.LT, TokenType.GT, TokenType.LE,
                                         TokenType.GE, TokenType.EQ, TokenType.NE):
            op = self.current_token()
            self.pos += 1
            node.add_child(ParseTreeNode(f"relop({op.lexeme})"))
            right = self.parse_E()
            if right:
                node.add_child(right)
        else:
            # no relational op; treat condition as truthiness of expression
            pass

        return node

"""
Parse a list of tokens and return (parse_tree, success, errors)
"""
def parse_tokens(tokens):
    
    parser = RecursiveDescentParser(tokens)
    parse_tree, success, errors = parser.parse()
    return parse_tree, success, errors
