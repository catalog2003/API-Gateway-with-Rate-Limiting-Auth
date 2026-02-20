from datetime import datetime


def user_entity(email: str, password_hash: bytes, role="free"):
    return {
        "email": email,
        "password_hash": password_hash,
        "role": role,
        "created_at": datetime.utcnow()
    }


