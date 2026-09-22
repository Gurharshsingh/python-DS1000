import bcrypt
import hashlib

def hash_password(password: str) -> bytes:
    # 1. Pre-hash the password with SHA-256 to get a fixed-length 64-character hex string
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    # 2. Pass that fixed-length string into bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(hashed_password.encode('utf-8'), salt)

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    # Must also pre-hash the plain password during verification
    pre_hashed = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return bcrypt.checkpw(pre_hashed.encode('utf-8'), hashed_password)