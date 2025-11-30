# ============================================================================
# ENUMS - All enumeration types for the system
# ============================================================================

from enum import Enum

class BookingStatus(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    CANCELED = "canceled"

class PaymentMethod(Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    E_WALLET = "e-wallet"

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class UserRole(Enum):
    CUSTOMER = "customer"
    BARBER = "barber"
    STAFF = "staff"
    OWNER = "owner"
