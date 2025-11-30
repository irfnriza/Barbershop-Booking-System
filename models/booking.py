# ============================================================================
# BOOKING MODEL
# ============================================================================

from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional
import streamlit as st
from utils.enums import BookingStatus
from patterns.observer import Subject
from services import Service

@dataclass
class Booking(Subject):
    """Booking model with Observer pattern"""
    booking_id: str
    customer_id: str
    service: Service
    barber_id: Optional[str]
    booking_date: date
    booking_time: time
    status: BookingStatus
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        Subject.__init__(self)
    
    def cancel(self) -> bool:
        """Cancel booking with validation"""
        if self.status in [BookingStatus.CANCELED, BookingStatus.COMPLETED]:
            return False
        
        booking_datetime = datetime.combine(self.booking_date, self.booking_time)
        hours_until = (booking_datetime - datetime.now()).total_seconds() / 3600
        
        if hours_until < 2:
            st.error("Cannot cancel less than 2 hours before appointment")
            return False
        
        self.status = BookingStatus.CANCELED
        self.notify('cancellation', {
            'user_id': self.customer_id,
            'message': f'Booking {self.booking_id} has been canceled'
        })
        return True
    
    def complete(self):
        """Mark booking as completed"""
        self.status = BookingStatus.COMPLETED
        self.notify('completion', {
            'user_id': self.customer_id,
            'message': f'Booking {self.booking_id} is completed. Please provide feedback!'
        })
