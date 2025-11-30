# ============================================================================
# USER MODELS
# ============================================================================

from dataclasses import dataclass, field
from datetime import datetime
from utils.enums import UserRole

@dataclass
class User:
    """Base user class"""
    user_id: str
    name: str
    email: str
    password: str
    phone: str
    role: UserRole
    created_at: datetime = field(default_factory=datetime.now)


class Customer(User):
    """Customer user type"""
    def __init__(self, user_id: str, name: str, email: str, password: str, phone: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.role = UserRole.CUSTOMER
        self.created_at = datetime.now()
        self.address = ""
        self.loyalty_points = 0


class Barber(User):
    """Barber user type"""
    def __init__(self, user_id: str, name: str, email: str, password: str, phone: str,
                 specialization: str = "", is_available: bool = True):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.role = UserRole.BARBER
        self.created_at = datetime.now()
        self.specialization = specialization
        self.is_available = is_available
        self.rating = 5.0


class Owner(User):
    """Owner/Admin user type"""
    def __init__(self, user_id: str, name: str, email: str, password: str, phone: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.role = UserRole.OWNER
        self.created_at = datetime.now()
