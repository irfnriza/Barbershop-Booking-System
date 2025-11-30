# ============================================================================
# BASIC SERVICES - Concrete Components for Decorator Pattern
# ============================================================================

from .service_interface import Service

class BasicService(Service):
    """Base implementation for basic services"""
    
    def __init__(self, name: str, base_price: float, base_duration: int, description: str = ""):
        self.name = name
        self.base_price = base_price
        self.base_duration = base_duration
        self.description = description
    
    def get_price(self) -> float:
        return self.base_price
    
    def get_description(self) -> str:
        return self.name
    
    def get_duration(self) -> int:
        return self.base_duration


class BasicHaircut(Service):
    """Concrete Component - Basic Haircut Service"""
    
    def __init__(self):
        self.base_price = 50000
        self.base_duration = 30
        self.name = "Haircut"
    
    def get_price(self) -> float:
        return self.base_price
    
    def get_description(self) -> str:
        return self.name
    
    def get_duration(self) -> int:
        return self.base_duration


class BasicShave(Service):
    """Concrete Component - Basic Shave Service"""
    
    def __init__(self):
        self.base_price = 30000
        self.base_duration = 20
        self.name = "Shave"
    
    def get_price(self) -> float:
        return self.base_price
    
    def get_description(self) -> str:
        return self.name
    
    def get_duration(self) -> int:
        return self.base_duration


class BasicStyling(Service):
    """Concrete Component - Basic Styling Service"""
    
    def __init__(self):
        self.base_price = 80000
        self.base_duration = 45
        self.name = "Styling"
    
    def get_price(self) -> float:
        return self.base_price
    
    def get_description(self) -> str:
        return self.name
    
    def get_duration(self) -> int:
        return self.base_duration


class BasicColoring(Service):
    """Concrete Component - Basic Coloring Service"""
    
    def __init__(self):
        self.base_price = 150000
        self.base_duration = 90
        self.name = "Coloring"
    
    def get_price(self) -> float:
        return self.base_price
    
    def get_description(self) -> str:
        return self.name
    
    def get_duration(self) -> int:
        return self.base_duration
