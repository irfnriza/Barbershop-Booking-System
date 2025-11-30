# ============================================================================
# FEEDBACK MODEL
# ============================================================================

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Feedback:
    """Feedback model"""
    feedback_id: str
    booking_id: str
    customer_id: str
    barber_id: str
    rating: int
    comment: str
    created_at: datetime = field(default_factory=datetime.now)
