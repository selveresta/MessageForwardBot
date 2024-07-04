import os
from dotenv import load_dotenv

load_dotenv()

API_ID = str(os.environ.get("API_ID", 0))
API_HASH = str(os.environ.get("API_HASH", 0))
PHONE = str(os.environ.get("PHONE", 0))
