# Lexical Parser 

Python project providing a lexical analyzer and recursive-descent parser for a custom grammar. This repository contains the backend code used by a simple web UI for visualizing tokens and parse trees.

## Features

- Tokenizer / lexer
- Recursive descent parser
- Web frontend (Flask) serving static HTML/CSS/JS to interact with the parser
- Utilities for error handling and visualization

## Repository Structure

- `app.py` - Flask application entrypoint
- `config.py` - Application configuration
- `lexer/` - Tokenizer and token type definitions
- `parser/` - Grammar, recursive descent parser, and parse tree utilities
- `templates/` - Jinja2 HTML templates for the web UI
- `static/` - CSS and JS for the front end
- `utils/` - Helper utilities (errors, visualizer)
- `requirements.txt` - Python dependencies
- `text_analyzer.py` - (Top-level script, likely for CLI/testing)

## Quick Start

Prerequisites
- Python 3.10+ recommended
- pip
# 1. first clone the repo

# 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
```
# OR
```
venv\Scripts\activate     # Windows
```
# 3. Install dependencies
```
pip install -r requirements.txt
```
# 7. Run the application
```
python app.py
```
# OR
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

# 8. Open browser & Navigate to http://localhost:3000


## Tests

There are no automated tests included in this repo currently. Adding unit tests for the tokenizer and parser is highly recommended.

## Notes & Next Steps

- Add unit tests for `lexer/tokenizer.py` and the parser in `parser/`.
- Add CI (GitHub Actions) to run tests and linters on push.
- Consider packaging the parser as a library with a `setup.cfg`/`pyproject.toml`.
