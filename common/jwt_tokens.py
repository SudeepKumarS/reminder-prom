from datetime import datetime, timedelta

import jwt

from common.settings import JWT_SECRET_KEY


# Payload encoder helper
def encode_payload(payload: dict):
    """
    This method is used to encode the payload passed as a parameter
    """
    try:
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    except:
        raise


# Decode credential helper
def decode_credentials(credentials: str):
    """
    This method is used to decode the credentials passed as a parameter
    """
    try:
        return jwt.decode(credentials, JWT_SECRET_KEY, algorithms=["HS256"])
    except:
        raise


# Helper function to generate JWT token
def generate_token(username: str, role: str, password: str) -> str:
    try:
        payload = {
            "username": username,
            "role": role,
            "password": password,
            "exp": datetime.utcnow() + timedelta(hours=2),
        }
        return encode_payload(payload)
    except:
        raise
