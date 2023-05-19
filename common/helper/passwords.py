from passlib.context import CryptContext


# password context using passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password verification function
def verify_password(plain_password, hashed_password):
    """
    To verify a hashed password with a plain password
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    """
    To hash the given password
    """
    return pwd_context.hash(password)