# ============================================================================
# OBSERVER PATTERN - Notification System
# ============================================================================

from abc import ABC, abstractmethod
from typing import List
import streamlit as st
from models.notification import Notification

class Observer(ABC):
    """Observer interface"""
    @abstractmethod
    def update(self, subject, event_type: str, data: dict):
        pass


class NotificationObserver(Observer):
    """Concrete Observer for notifications"""
    def update(self, subject, event_type: str, data: dict):
        notification = Notification(
            user_id=data.get('user_id'),
            notification_type=event_type,
            message=data.get('message'),
            channel='email'
        )
        st.success(f"📧 Notification: {notification.message}")


class Subject(ABC):
    """Subject interface"""
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(self, event_type, data)
