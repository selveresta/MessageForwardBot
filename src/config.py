import os
from dotenv import load_dotenv

load_dotenv()

API_ID = str(os.environ.get("API_ID", 0))
API_HASH = str(os.environ.get("API_HASH", 0))
PHONE = str(os.environ.get("PHONE", 0))

API_ID_PREMIUM = str(os.environ.get("API_ID_PREMIUM", 0))
API_HASH_PREMIUM = str(os.environ.get("API_HASH_PREMIUM", 0))
PHONE_PREMIUM = str(os.environ.get("PHONE_PREMIUM", 0))
