# ============================================================================
# SERVICE INTERFACE - Decorator Pattern Component
# ============================================================================

from abc import ABC, abstractmethod

class Service(ABC):
    """Component - Base service interface for Decorator Pattern"""
    
    @abstractmethod
    def get_price(self) -> float:
        """Get the total price of the service"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get the description of the service"""
        pass
    
    @abstractmethod
    def get_duration(self) -> int:
        """Get the duration in minutes"""
        pass
