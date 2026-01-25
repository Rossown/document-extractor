import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Create formatter with detailed information
# Includes: timestamp, level, filename:line number, function name, message
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_CONN_STRING')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # External API Configuration
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 10))  # Default 10 seconds
    API_RETRIES = int(os.getenv('API_RETRIES', 3))  # Default 3 retries
    API_DEFAULT_HEADERS = {
        'User-Agent': 'DocumentExtractor/1.0',
        'Content-Type': 'application/json',
    }
        
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', 2000))
    
    # Document Configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB
    
    STORE_ALLOWED_FIELDS = {
        "name",
        "address_type",
        "address_line1",
        "address_line2",
        "city",
        "state_province",
        "postal_code",
        "country_region"
    }