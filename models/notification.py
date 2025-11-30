# ============================================================================
# NOTIFICATION MODEL
# ============================================================================

from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Notification:
    """Notification model"""
    notification_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    notification_type: str = ""
    message: str = ""
    channel: str = "email"
    is_sent: bool = True
    sent_at: datetime = field(default_factory=datetime.now)
