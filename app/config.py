from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL_ALEMBIC = os.environ.get("DATABASE_URL_ALEMBIC")
