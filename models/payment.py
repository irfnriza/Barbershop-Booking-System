# ============================================================================
# PAYMENT MODEL
# ============================================================================

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid
from utils.enums import PaymentMethod, PaymentStatus

@dataclass
class Payment:
    """Payment model"""
    payment_id: str
    booking_id: str
    amount: float
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    transaction_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    
    def process_payment(self) -> bool:
        """Process payment"""
        self.payment_status = PaymentStatus.PAID
        self.payment_date = datetime.now()
        self.transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        return True
