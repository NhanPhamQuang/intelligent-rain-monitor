import hashlib
import secrets
from datetime import datetime

from services.weather_service import get_db

# Pages each role can access
ROLE_PAGES = {
    "admin":          ["Weather Dashboard", "Rain Prediction", "Model Performance", "Farmer App", "Weather Monitoring"],
    "data_scientist": ["Weather Dashboard", "Rain Prediction", "Model Performance"],
    "farmer":         ["Farmer App"],
    "weather_agency": ["Weather Monitoring"],
}

ROLE_LABELS = {
    "data_scientist": "Data Scientist",
    "farmer":         "Farmer",
    "weather_agency": "Weather Agency",
}


def _hash(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{digest}"


def _verify(password: str, stored: str) -> bool:
    try:
        salt, digest = stored.split(":", 1)
        return hashlib.sha256((salt + password).encode()).hexdigest() == digest
    except Exception:
        return False


def ensure_admin():
    """Create admin / 1111 on first run."""
    db = get_db()
    if db is None:
        return
    if not db["users"].find_one({"username": "admin"}):
        db["users"].insert_one({
            "username": "admin",
            "email": "admin@rainmonitor.local",
            "password_hash": _hash("1111"),
            "role": "admin",
            "created_at": datetime.utcnow(),
            "is_active": True,
        })
        db["users"].create_index("username", unique=True)


def register_user(username: str, email: str, password: str, role: str) -> tuple:
    db = get_db()
    if db is None:
        return False, "Database connection failed."
    if db["users"].find_one({"$or": [{"username": username}, {"email": email}]}):
        return False, "Username or email already taken."
    db["users"].insert_one({
        "username": username,
        "email": email,
        "password_hash": _hash(password),
        "role": role,
        "created_at": datetime.utcnow(),
        "is_active": True,
    })
    return True, "Account created successfully."


def login_user(username: str, password: str) -> dict:
    """Returns user dict on success, None on failure."""
    db = get_db()
    if db is None:
        return None
    doc = db["users"].find_one({"username": username, "is_active": True})
    if doc and _verify(password, doc["password_hash"]):
        return {
            "username": doc["username"],
            "email": doc.get("email", ""),
            "role": doc["role"],
        }
    return None


def get_allowed_pages(role: str) -> list:
    return ROLE_PAGES.get(role, [])
