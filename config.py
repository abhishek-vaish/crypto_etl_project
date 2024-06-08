from pathlib import Path
import os

from dotenv import load_dotenv


BASE_PATH = Path(os.path.dirname(__file__))

load_dotenv(BASE_PATH / ".env")

# folder path
ARCHIVE_PATH = BASE_PATH / 'Data' / 'Archive'
ETL_PATH = BASE_PATH / 'Data' / 'FilesForProcessing'
if not ETL_PATH.is_dir() or not ARCHIVE_PATH.is_dir():
    ETL_PATH.mkdir(exist_ok=True)
    ARCHIVE_PATH.mkdir(exist_ok=True)

# snowflake environment variables
SNOWFLAKE_USERNAME = os.getenv("SNOWFLAKE_USERNAME")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_IDENTIFIER = os.getenv("SNOWFLAKE_IDENTIFIER")
INTERNAL_STAGE = os.getenv("INTERNAL_STAGE")

# coin ranking environment
API_KEY = os.getenv("API_KEY")
COIN_RANKING_URI = os.getenv("CRYPTO_RANKING_URI")
COIN_RANKING_LIMIT = os.getenv("API_LIMIT")
