from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json

# Import our modules
from lexer.tokenizer import Tokenizer, LexicalError
from lexer.token_types import TokenType, get_token_category
from parser.recursive_descent import RecursiveDescentParser
from parser.grammar import get_grammar_rules, get_grammar_explanation
from utils.errors import ErrorHandler, CompilerError, ErrorType, detect_common_errors
from utils.visualizer import (generate_html_tree, generate_json_tree, 
                               generate_svg_tree, generate_tree_statistics,
                               format_tree_ascii)


app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Configuration
app.config['SECRET_KEY'] = 'lexical-parser-secret-key'
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/grammar')
def grammar_page():
    """Grammar documentation page"""
    grammar_rules = get_grammar_rules()
    explanation = get_grammar_explanation()
    return render_template('grammar.html', 
                         grammar_rules=grammar_rules,
                         explanation=explanation)


@app.route('/tokens')
def tokens_page():
    """Token types page"""
    token_categories = {
        'Operators': ['+', '-', '*', '/', '%', '**'],
        'Delimiters': ['(', ')'],
        'Assignment': ['='],
        'Identifiers': 'letter (letter | digit | _)*',
        'Literals': 'Integer or Float numbers'
    }
    
    test_cases = {
        'valid': ['a+b', 'a*b+c', '(a+b)*c', 'a**b', '2+3*4', 
                  '(1+2)*(3+4)', 'x+y-z', 'a/b%c', 'x123', '_var'],
        'invalid': ['a++b', '(a+b', 'a+', '*a', '+', '()', 
                    'a b', 'a+*b', '123abc', '@var']
    }
    
    return render_template('tokens.html',
                         token_categories=token_categories,
                         test_cases=test_cases)


@app.route('/testcases')
def test_cases_page():
    """Standalone Test Cases page"""
    # Reuse the same test cases defined for tokens page
    test_cases = {
        'valid': ['a+b', 'a*b+c', '(a+b)*c', 'a**b', '2+3*4', 
                  '(1+2)*(3+4)', 'x+y-z', 'a/b%c', 'x123', '_var'],
        'invalid': ['a++b', '(a+b', 'a+', '*a', '+', '()', 
                    'a b', 'a+*b', '123abc', '@var']
    }

    return render_template('test_cases.html', test_cases=test_cases)


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    API endpoint to analyze input string
    Returns: JSON with tokens, parse tree, and errors
    """
    data = request.get_json()
    input_string = data.get('input', '').strip()
    
    if not input_string:
        return jsonify({
            'success': False,
            'error': 'Input string is empty',
            'tokens': [],
            'parse_tree': None,
            'errors': ['Input string cannot be empty']
        })
    
    error_handler = ErrorHandler()
    result = {
        'success': False,
        'input': input_string,
        'tokens': [],
        'parse_tree': None,
        'errors': [],
        'warnings': [],
        'statistics': {}
    }
    
    try:
        # Step 1: Lexical Analysis
        tokenizer = Tokenizer(input_string)
        tokens = tokenizer.tokenize()
        
        # Convert tokens to dict format
        result['tokens'] = [
            {
                'type': token.type,
                'value': str(token.value),
                'lexeme': token.lexeme,
                'category': get_token_category(token.type),
                'line': token.line,
                'column': token.column
            }
            for token in tokens if token.type != TokenType.EOF
        ]
        
        # Detect common errors
        common_errors = detect_common_errors(input_string, tokens)
        for error in common_errors:
            error_handler.add_error(error)
        
        # Step 2: Syntax Analysis (Parsing)
        parser = RecursiveDescentParser(tokens)
        parse_tree, parse_success, parse_errors = parser.parse()
        
        # Add parse errors
        for error_msg in parse_errors:
            error_handler.add_error(CompilerError(ErrorType.SYNTAX, error_msg))
        
        # Convert parse tree to dict
        if parse_tree:
            result['parse_tree'] = parse_tree.to_dict()
            result['tree_ascii'] = format_tree_ascii(parse_tree)
            result['tree_svg'] = generate_svg_tree(parse_tree)
            result['statistics'] = generate_tree_statistics(parse_tree)
        
        # Determine overall success
        result['success'] = not error_handler.has_errors()
        result['errors'] = error_handler.get_errors_as_dict()
        result['accepted'] = result['success']
        
    except LexicalError as e:
        result['errors'] = [{
            'type': ErrorType.LEXICAL,
            'message': str(e),
            'line': e.line,
            'column': e.column
        }]
        result['success'] = False
        result['accepted'] = False
        
    except Exception as e:
        result['errors'] = [{
            'type': 'System Error',
            'message': f"Unexpected error: {str(e)}"
        }]
        result['success'] = False
        result['accepted'] = False
    
    return jsonify(result)


@app.route('/api/grammar', methods=['GET'])
def get_grammar():
    """API endpoint to get grammar rules"""
    return jsonify({
        'rules': get_grammar_rules(),
        'explanation': get_grammar_explanation()
    })


@app.route('/api/validate', methods=['POST'])
def validate():
    """
    Quick validation endpoint
    Just returns if input is valid or not
    """
    data = request.get_json()
    input_string = data.get('input', '').strip()
    
    try:
        tokenizer = Tokenizer(input_string)
        tokens = tokenizer.tokenize()
        
        parser = RecursiveDescentParser(tokens)
        parse_tree, success, errors = parser.parse()
        
        return jsonify({
            'valid': success,
            'error_count': len(errors)
        })
    except:
        return jsonify({
            'valid': False,
            'error_count': 1
        })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Lexical Analyzer & Parser Web Application")
    print("=" * 60)
    print("Starting Flask server...")
    print("Access the application at: http://localhost:3000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=3000)