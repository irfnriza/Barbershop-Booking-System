# ============================================================================
# SERVICE DECORATORS - Decorator Pattern Implementation
# ============================================================================

from .service_interface import Service

class ServiceDecorator(Service):
    """Base Decorator - Abstract decorator for services"""
    
    def __init__(self, wrapped_service: Service):
        self.wrapped_service = wrapped_service
    
    def get_price(self) -> float:
        return self.wrapped_service.get_price()
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description()
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration()


class HairWashDecorator(ServiceDecorator):
    """Concrete Decorator - Adds Hair Wash to service"""
    
    def get_price(self) -> float:
        return self.wrapped_service.get_price() + 15000
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description() + " + Hair Wash"
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration() + 10


class HairSpaDecorator(ServiceDecorator):
    """Concrete Decorator - Adds Hair Spa to service"""
    
    def get_price(self) -> float:
        return self.wrapped_service.get_price() + 30000
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description() + " + Hair Spa"
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration() + 20


class MassageDecorator(ServiceDecorator):
    """Concrete Decorator - Adds Head Massage to service"""
    
    def get_price(self) -> float:
        return self.wrapped_service.get_price() + 15000
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description() + " + Massage"
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration() + 10


class HotTowelDecorator(ServiceDecorator):
    """Concrete Decorator - Adds Hot Towel to service"""
    
    def get_price(self) -> float:
        return self.wrapped_service.get_price() + 10000
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description() + " + Hot Towel"
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration() + 5


class PremiumProductDecorator(ServiceDecorator):
    """Concrete Decorator - Adds Premium Products to service"""
    
    def get_price(self) -> float:
        return self.wrapped_service.get_price() + 25000
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description() + " + Premium Products"
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration()
