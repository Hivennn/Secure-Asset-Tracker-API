from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

# Secret signature key (In a production app, this would stay inside a .env file)
SECRET_KEY = "SUPER_SECRET_PORTFOLIO_KEY_KEEP_THIS_SECURE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Securely hashes a raw plain text password natively using bcrypt
def get_password_hash(password: str) -> str:

    # Convert password string into bytes, generate salt, and has it
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")


# Verifies incoming password against the stored database hash string
def verify_password(plain_password: str, hashed_password: str) -> bool:

    try:
        # Convert both strings to bytes explicitly before checking signatures
        plain_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(plain_bytes, hashed_bytes)

    except Exception as e:
        print(f"Bcrypt verification crash log: {e}")
        return False


# Encrypt and encodes a signed session token that expires in 30 minutes
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
