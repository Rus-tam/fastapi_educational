from jose import JWTError, jwt
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


# Algorithm

# Expiration time
