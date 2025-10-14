import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lexical-parser-dev-key-2024'
    
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # Application settings
    MAX_INPUT_LENGTH = 1000
    ENABLE_DETAILED_ERRORS = True
    
    # Parse tree settings
    MAX_TREE_DEPTH = 100
    ENABLE_SVG_GENERATION = True
    
    # Lexer settings
    CASE_SENSITIVE = True
    ALLOW_UNDERSCORE_IN_ID = True
    
    # Parser settings
    ENABLE_ERROR_RECOVERY = False
    MAX_PARSE_ERRORS = 10


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MAX_INPUT_LENGTH = 500


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name='default'):
    """Get configuration based on environment"""
    return config.get(config_name, config['default'])