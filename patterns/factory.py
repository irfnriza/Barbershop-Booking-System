# ============================================================================
# FACTORY PATTERN - Service Factory
# ============================================================================

from typing import List
from services import (
    Service,
    BasicService,
    HairWashDecorator,
    HairSpaDecorator,
    MassageDecorator,
    HotTowelDecorator,
    PremiumProductDecorator
)

class ServiceFactory:
    """Factory pattern to create services with decorators"""
    
    BASE_SERVICES = {
        "Haircut": {"price": 50000, "duration": 30, "desc": "Professional haircut"},
        "Shave": {"price": 30000, "duration": 20, "desc": "Clean shave"},
        "Styling": {"price": 80000, "duration": 45, "desc": "Hair styling"},
        "Coloring": {"price": 150000, "duration": 90, "desc": "Hair coloring"},
    }
    
    DECORATORS = {
        "Hair Wash": HairWashDecorator,
        "Hair Spa": HairSpaDecorator,
        "Massage": MassageDecorator,
        "Hot Towel": HotTowelDecorator,
        "Premium Products": PremiumProductDecorator,
    }
    
    @staticmethod
    def create_service(base_service_name: str, addons: List[str]) -> Service:
        """Create a service with selected addons using Decorator Pattern"""
        if base_service_name not in ServiceFactory.BASE_SERVICES:
            raise ValueError(f"Unknown service: {base_service_name}")
        
        service_info = ServiceFactory.BASE_SERVICES[base_service_name]
        service = BasicService(
            base_service_name,
            service_info["price"],
            service_info["duration"],
            service_info["desc"]
        )
        
        # Apply decorators dynamically
        for addon in addons:
            if addon in ServiceFactory.DECORATORS:
                decorator_class = ServiceFactory.DECORATORS[addon]
                service = decorator_class(service)
        
        return service
