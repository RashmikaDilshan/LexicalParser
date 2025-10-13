from lexer.tokenizer import Tokenizer
from parser.recursive_descent import RecursiveDescentParser
from parser.parse_tree import visualize_tree_ascii

def test_expression(description, input_string, should_pass=True):
    """Test a single expression"""
    print("\n" + "="*70)
    print(f"TEST: {description}")
    print("="*70)
    print(f"Input: {input_string}")
    print("-"*70)
    
    try:
        # Tokenize
        tokenizer = Tokenizer(input_string)
        tokens = tokenizer.tokenize()
        
        print(f"✓ Tokenization successful: {len(tokens)-1} tokens")
        for token in tokens:
            if token.type != 'EOF':
                print(f"  {token}")
        
        # Parse
        parser = RecursiveDescentParser(tokens)
        parse_tree, success, errors = parser.parse()
        
        if success and should_pass:
            print(f"\n✓ Parsing successful!")
            print("\nParse Tree:")
            print(visualize_tree_ascii(parse_tree))
            print(f"\n✓ TEST PASSED: {description}")
        elif not success and not should_pass:
            print(f"\n✓ Parsing failed as expected")
            for error in errors:
                print(f"  Error: {error}")
            print(f"\n✓ TEST PASSED: {description}")
        elif success and not should_pass:
            print(f"\n✗ TEST FAILED: Expected to fail but passed")
        else:
            print(f"\n✗ TEST FAILED: Parsing failed unexpectedly")
            for error in errors:
                print(f"  Error: {error}")
                
    except Exception as e:
        if not should_pass:
            print(f"\n✓ Exception raised as expected: {e}")
            print(f"✓ TEST PASSED: {description}")
        else:
            print(f"\n✗ TEST FAILED: Unexpected exception: {e}")

def run_all_tests():
    """Run comprehensive test suite"""
    print("\n" + "="*70)
    print("ENHANCED PROGRAMMING LANGUAGE ANALYZER - TEST SUITE")
    print("="*70)
    
    # Test 1: Simple Assignment
    test_expression(
        "Simple Assignment",
        "x = 5;",
        should_pass=True
    )
    
    # Test 2: Arithmetic Expression Assignment
    test_expression(
        "Arithmetic Expression Assignment",
        "result = a + b * c;",
        should_pass=True
    )
    
    # Test 3: If Statement
    test_expression(
        "If Statement",
        "if (x > 0) { y = 1; }",
        should_pass=True
    )
    
    # Test 4: If-Else Statement
    test_expression(
        "If-Else Statement",
        "if (x > 0) { y = 1; } else { y = 0; }",
        should_pass=True
    )
    
    # Test 5: While Loop
    test_expression(
        "While Loop",
        "while (i < 10) { i = i + 1; }",
        should_pass=True
    )
    
    # Test 6: For Loop
    test_expression(
        "For Loop",
        "for (i = 0; i < 10; i = i + 1) { sum = sum + i; }",
        should_pass=True
    )
    
    # Test 7: Function Definition
    test_expression(
        "Function Definition",
        "def add(a, b) { return a + b; }",
        should_pass=True
    )
    
    # Test 8: Function Call
    test_expression(
        "Function Call in Assignment",
        "result = add(3, 5);",
        should_pass=True
    )
    
    # Test 9: Nested Function Calls
    test_expression(
        "Nested Function Calls",
        "result = add(multiply(2, 3), 4);",
        should_pass=True
    )
    
    # Test 10: Multiple Statements
    test_expression(
        "Multiple Statements",
        "x = 5; y = 10; z = x + y;",
        should_pass=True
    )
    
    # Test 11: Nested Blocks
    test_expression(
        "Nested If Statements",
        "if (x > 0) { if (y > 0) { z = 1; } }",
        should_pass=True
    )
    
    # Test 12: Complex Function
    test_expression(
        "Recursive Function",
        """def factorial(n) {
            if (n <= 1) {
                return 1;
            } else {
                return n * factorial(n - 1);
            }
        }""",
        should_pass=True
    )
    
    # Test 13: Power Operator
    test_expression(
        "Power Operator",
        "result = base ** exponent;",
        should_pass=True
    )
    
    # Test 14: All Comparison Operators
    test_expression(
        "Multiple Comparison Operators",
        """if (a < b) { x = 1; }
        if (a > b) { x = 2; }
        if (a <= b) { x = 3; }
        if (a >= b) { x = 4; }
        if (a == b) { x = 5; }
        if (a != b) { x = 6; }""",
        should_pass=True
    )
    
    # Test 15: Empty Return
    test_expression(
        "Return Without Value",
        "def doSomething() { x = 1; return; }",
        should_pass=True
    )
    
    # Test 16: Function with No Parameters
    test_expression(
        "Function with No Parameters",
        "def getConstant() { return 42; }",
        should_pass=True
    )
    
    # Test 17: Function with Multiple Parameters
    test_expression(
        "Function with Multiple Parameters",
        "def calculate(a, b, c, d) { return a + b * c - d; }",
        should_pass=True
    )
    
    # ERROR CASES
    
    # Test 18: Missing Semicolon
    test_expression(
        "Missing Semicolon (Should Fail)",
        "x = 5",
        should_pass=False
    )
    
    # Test 19: Unbalanced Parentheses
    test_expression(
        "Unbalanced Parentheses (Should Fail)",
        "if (x > 0 { y = 1; }",
        should_pass=False
    )
    
    # Test 20: Unbalanced Braces
    test_expression(
        "Unbalanced Braces (Should Fail)",
        "if (x > 0) { y = 1;",
        should_pass=False
    )