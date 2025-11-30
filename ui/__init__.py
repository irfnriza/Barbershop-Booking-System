# UI package
from .auth import login_page, register_page
from .customer_dashboard import customer_dashboard
from .barber_dashboard import barber_dashboard
from .owner_dashboard import owner_dashboard

__all__ = [
    'login_page',
    'register_page',
    'customer_dashboard',
    'barber_dashboard',
    'owner_dashboard'
]
