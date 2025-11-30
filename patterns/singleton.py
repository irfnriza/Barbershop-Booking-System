# ============================================================================
# SINGLETON PATTERN - Database Manager with JSON Persistence
# ============================================================================

import json
import os
from typing import Dict
from datetime import datetime, date, time
from models.user import User, Customer, Barber, Owner
from models.booking import Booking
from models.payment import Payment
from models.feedback import Feedback
from utils.enums import UserRole, BookingStatus, PaymentStatus, PaymentMethod
from patterns.factory import ServiceFactory

class DatabaseManager:
    """Singleton pattern to manage all data storage with JSON persistence"""
    _instance = None
    DATA_FILE = "barbershop_data.json"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.users: Dict[str, User] = {}
        self.bookings: Dict[str, Booking] = {}
        self.services: Dict[str, 'Service'] = {}
        self.payments: Dict[str, Payment] = {}
        self.feedbacks: Dict[str, 'Feedback'] = {}
        self.schedules: Dict[str, 'Schedule'] = {}
        
        # Load data from JSON or initialize demo data
        if os.path.exists(self.DATA_FILE):
            self._load_from_json()
        else:
            self._initialize_demo_data()
            self._save_to_json()
    
    def _serialize_user(self, user: User) -> dict:
        """Serialize user object to dict"""
        data = {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'password': user.password,
            'phone': user.phone,
            'role': user.role.value,
            'created_at': user.created_at.isoformat() if hasattr(user.created_at, 'isoformat') else str(user.created_at)
        }
        
        if isinstance(user, Customer):
            data['type'] = 'customer'
            data['address'] = user.address
            data['loyalty_points'] = user.loyalty_points
        elif isinstance(user, Barber):
            data['type'] = 'barber'
            data['specialization'] = user.specialization
            data['is_available'] = user.is_available
            data['rating'] = user.rating
        elif isinstance(user, Owner):
            data['type'] = 'owner'
        
        return data
    
    def _deserialize_user(self, data: dict) -> User:
        """Deserialize dict to user object"""
        user_type = data.get('type', 'customer')
        
        if user_type == 'customer':
            user = Customer(data['user_id'], data['name'], data['email'], 
                          data['password'], data['phone'])
            user.address = data.get('address', '')
            user.loyalty_points = data.get('loyalty_points', 0)
        elif user_type == 'barber':
            user = Barber(data['user_id'], data['name'], data['email'],
                         data['password'], data['phone'],
                         data.get('specialization', ''),
                         data.get('is_available', True))
            user.rating = data.get('rating', 5.0)
        elif user_type == 'owner':
            user = Owner(data['user_id'], data['name'], data['email'],
                        data['password'], data['phone'])
        else:
            # Fallback to customer
            user = Customer(data['user_id'], data['name'], data['email'],
                          data['password'], data['phone'])
        
        return user
    
    def _serialize_booking(self, booking: Booking) -> dict:
        """Serialize booking object to dict"""
        return {
            'booking_id': booking.booking_id,
            'customer_id': booking.customer_id,
            'barber_id': booking.barber_id,
            'booking_date': booking.booking_date.isoformat(),
            'booking_time': booking.booking_time.isoformat(),
            'status': booking.status.value,
            'created_at': booking.created_at.isoformat(),
            'service_description': booking.service.get_description(),
            'service_price': booking.service.get_price(),
            'service_duration': booking.service.get_duration()
        }
    
    def _deserialize_booking(self, data: dict) -> Booking:
        """Deserialize dict to booking object - simplified version"""
        # Parse service info to recreate service
        service_desc = data.get('service_description', 'Haircut')
        
        # Try to extract base service and addons from description
        base_service = 'Haircut'
        addons = []
        
        for service_name in ServiceFactory.BASE_SERVICES.keys():
            if service_name in service_desc:
                base_service = service_name
                break
        
        for addon_name in ServiceFactory.DECORATORS.keys():
            if addon_name in service_desc:
                addons.append(addon_name)
        
        service = ServiceFactory.create_service(base_service, addons)
        
        booking = Booking(
            booking_id=data['booking_id'],
            customer_id=data['customer_id'],
            service=service,
            barber_id=data.get('barber_id'),
            booking_date=date.fromisoformat(data['booking_date']),
            booking_time=time.fromisoformat(data['booking_time']),
            status=BookingStatus(data['status']),
            created_at=datetime.fromisoformat(data['created_at'])
        )
        
        return booking
    
    def _serialize_payment(self, payment: Payment) -> dict:
        """Serialize payment object to dict"""
        return {
            'payment_id': payment.payment_id,
            'booking_id': payment.booking_id,
            'amount': payment.amount,
            'payment_method': payment.payment_method.value,
            'payment_status': payment.payment_status.value,
            'transaction_id': payment.transaction_id,
            'payment_date': payment.payment_date.isoformat() if payment.payment_date else None
        }
    
    def _deserialize_payment(self, data: dict) -> Payment:
        """Deserialize dict to payment object"""
        payment = Payment(
            payment_id=data['payment_id'],
            booking_id=data['booking_id'],
            amount=data['amount'],
            payment_method=PaymentMethod(data['payment_method']),
            payment_status=PaymentStatus(data['payment_status']),
            transaction_id=data.get('transaction_id'),
            payment_date=datetime.fromisoformat(data['payment_date']) if data.get('payment_date') else None
        )
        return payment
    
    def _serialize_feedback(self, feedback) -> dict:
        """Serialize feedback object to dict"""
        return {
            'feedback_id': feedback.feedback_id,
            'booking_id': feedback.booking_id,
            'customer_id': feedback.customer_id,
            'barber_id': feedback.barber_id,
            'rating': feedback.rating,
            'comment': feedback.comment,
            'created_at': feedback.created_at.isoformat()
        }
    
    def _deserialize_feedback(self, data: dict):
        """Deserialize dict to feedback object"""
        from models.feedback import Feedback
        return Feedback(
            feedback_id=data['feedback_id'],
            booking_id=data['booking_id'],
            customer_id=data['customer_id'],
            barber_id=data['barber_id'],
            rating=data['rating'],
            comment=data['comment'],
            created_at=datetime.fromisoformat(data['created_at'])
        )
    
    def _save_to_json(self):
        """Save all data to JSON file"""
        try:
            data = {
                'users': {uid: self._serialize_user(user) for uid, user in self.users.items()},
                'bookings': {bid: self._serialize_booking(booking) for bid, booking in self.bookings.items()},
                'payments': {pid: self._serialize_payment(payment) for pid, payment in self.payments.items()},
                'feedbacks': {fid: self._serialize_feedback(feedback) for fid, feedback in self.feedbacks.items()}
            }
            
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def _load_from_json(self):
        """Load all data from JSON file"""
        try:
            with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load users
            self.users = {uid: self._deserialize_user(user_data) 
                         for uid, user_data in data.get('users', {}).items()}
            
            # Load bookings
            self.bookings = {bid: self._deserialize_booking(booking_data)
                           for bid, booking_data in data.get('bookings', {}).items()}
            
            # Load payments
            self.payments = {pid: self._deserialize_payment(payment_data)
                           for pid, payment_data in data.get('payments', {}).items()}
            
            # Load feedbacks
            self.feedbacks = {fid: self._deserialize_feedback(feedback_data)
                            for fid, feedback_data in data.get('feedbacks', {}).items()}
            
            print(f"✅ Data loaded from {self.DATA_FILE}")
        except Exception as e:
            print(f"Error loading from JSON: {e}")
            self._initialize_demo_data()
    
    def save(self):
        """Public method to save data"""
        self._save_to_json()
    
    def _initialize_demo_data(self):
        """Initialize with demo data"""
        # Create demo barbers
        barber1 = Barber("B001", "John Doe", "john@barber.com", "1234", "081234567890", 
                        "Hair Specialist", True)
        barber2 = Barber("B002", "Jane Smith", "jane@barber.com", "1234", "081234567891",
                        "Beard Expert", True)
        
        self.users[barber1.user_id] = barber1
        self.users[barber2.user_id] = barber2
        
        # Create demo owner
        owner = Owner("O001", "Admin Boss", "admin@barber.com", "admin", "081234567892")
        self.users[owner.user_id] = owner
