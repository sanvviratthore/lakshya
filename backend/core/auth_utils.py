import jwt
from datetime import datetime, timedelta, timezone
import os

# Use an environment variable for the secret, but keep a fallback for local development
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-lakshya-key-2026")
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Standard 24-hour expiration for a seamless user experience during the hackathon
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        # Decodes the token and checks if it's expired automatically
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.PyJWTError as e:
        print(f"Token verification failed: {str(e)}")
        return None