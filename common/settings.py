import os

from dotenv import load_dotenv

# Loading environment file
load_dotenv()

# Getting the MongoDB connection string
try:
    CONNECTION_STRING = os.environ["CONNECTION_STRING"]
except KeyError:
    raise ("Connection string is not set")

try:
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
except KeyError:
    raise ("JWT secret key is not set")

USERS_DB_NAME = "users_db"
USERS_COLLECTION_NAME = "users"
