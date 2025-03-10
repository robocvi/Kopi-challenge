from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
MONGO_DB_CONNECTION_STRING = os.environ["MONGO_DB_CONNECTION_STRING"]
