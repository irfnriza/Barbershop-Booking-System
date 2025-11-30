# Design Patterns package
from .singleton import DatabaseManager
from .observer import Observer, NotificationObserver, Subject
from .factory import ServiceFactory

__all__ = [
    'DatabaseManager',
    'Observer',
    'NotificationObserver',
    'Subject',
    'ServiceFactory'
]
