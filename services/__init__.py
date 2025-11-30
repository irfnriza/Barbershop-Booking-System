# Services package
from .service_interface import Service
from .basic_services import BasicService, BasicHaircut, BasicShave, BasicStyling, BasicColoring
from .service_decorators import (
    ServiceDecorator,
    HairWashDecorator,
    HairSpaDecorator,
    MassageDecorator,
    HotTowelDecorator,
    PremiumProductDecorator
)

__all__ = [
    'Service',
    'BasicService',
    'BasicHaircut',
    'BasicShave',
    'BasicStyling',
    'BasicColoring',
    'ServiceDecorator',
    'HairWashDecorator',
    'HairSpaDecorator',
    'MassageDecorator',
    'HotTowelDecorator',
    'PremiumProductDecorator'
]
