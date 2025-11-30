# Design Patterns Architecture Guide

## Overview

Barbershop Booking System dibangun dengan 4 design patterns utama yang bekerja sama untuk menciptakan sistem yang robust, scalable, dan maintainable. Dokumen ini menjelaskan implementasi detail dari setiap pattern.

## Pattern Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                       │
│                   (Streamlit UI - ui/)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Business Logic Layer                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Factory    │  │   Observer   │  │  Decorator   │     │
│  │   Pattern    │  │   Pattern    │  │   Pattern    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    Data Layer                                │
│              Singleton Pattern (Database)                    │
│                  (JSON Persistence)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Decorator Pattern - Dynamic Service Enhancement

### 📋 Purpose
Memungkinkan penambahan fitur (add-ons) ke layanan dasar secara dinamis tanpa mengubah class aslinya.

### 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Service Interface                         │
│         + get_price(): float                                 │
│         + get_description(): str                             │
│         + get_duration(): int                                │
└───────────────┬─────────────────────────────────────────────┘
                │
                │ implements
                │
    ┌───────────┴──────────┬──────────────────────┐
    │                      │                      │
┌───▼────────────┐  ┌─────▼──────────┐  ┌───────▼──────────┐
│ BasicHaircut   │  │  BasicShave    │  │  BasicStyling    │
│ Price: 50k     │  │  Price: 30k    │  │  Price: 80k      │
│ Duration: 30m  │  │  Duration: 20m │  │  Duration: 45m   │
└────────────────┘  └────────────────┘  └──────────────────┘
                │
                │ wraps
                │
    ┌───────────┴──────────────────────────────────────┐
    │          ServiceDecorator (Base)                 │
    │          - wrappedService: Service               │
    └───────────┬──────────────────────────────────────┘
                │
                │ extends
                │
    ┌───────────┴───────┬─────────────┬──────────────┐
┌───▼─────────────┐ ┌───▼──────────┐ ┌▼─────────────┐
│ HairWashDecorator│ │HairSpaDecorat│ │MassageDecorat│
│ +15k, +10m      │ │+30k, +20m    │ │+15k, +10m    │
└─────────────────┘ └──────────────┘ └──────────────┘
```

### 💻 Implementation

**Component Interface** (`services/service_interface.py`):
```python
from abc import ABC, abstractmethod

class Service(ABC):
    """Base interface untuk semua services"""
    
    @abstractmethod
    def get_price(self) -> float:
        """Return total price"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return service description"""
        pass
    
    @abstractmethod
    def get_duration(self) -> int:
        """Return duration in minutes"""
        pass
```

**Concrete Component** (`services/basic_services.py`):
```python
class BasicHaircut(Service):
    """Concrete Component - Base Haircut Service"""
    
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
```

**Base Decorator** (`services/service_decorators.py`):
```python
class ServiceDecorator(Service):
    """Base Decorator - Wraps another service"""
    
    def __init__(self, wrapped_service: Service):
        self.wrapped_service = wrapped_service
    
    def get_price(self) -> float:
        return self.wrapped_service.get_price()
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description()
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration()
```

**Concrete Decorator** (`services/service_decorators.py`):
```python
class HairWashDecorator(ServiceDecorator):
    """Adds Hair Wash feature to service"""
    
    def get_price(self) -> float:
        return self.wrapped_service.get_price() + 15000
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description() + " + Hair Wash"
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration() + 10
```

### 🎯 Usage Example

```python
# Manual wrapping
service = BasicHaircut()                    # Haircut: Rp 50,000
service = HairWashDecorator(service)        # + Hair Wash: Rp 65,000
service = MassageDecorator(service)         # + Massage: Rp 80,000

print(service.get_description())  # "Haircut + Hair Wash + Massage"
print(service.get_price())        # 80000
print(service.get_duration())     # 50 minutes

# Using Factory Pattern (recommended)
from patterns.factory import ServiceFactory

service = ServiceFactory.create_service(
    "Haircut",
    ["Hair Wash", "Massage", "Hot Towel"]
)
```

### ✨ Benefits

✅ **Open/Closed Principle** - Extend functionality without modifying existing code  
✅ **Single Responsibility** - Each decorator has one specific enhancement  
✅ **Flexible Combinations** - Mix and match any decorators  
✅ **Runtime Configuration** - Add features dynamically  

---

## 2. Singleton Pattern - Database Manager

### 📋 Purpose
Memastikan hanya ada satu instance database di seluruh aplikasi untuk menjaga konsistensi data.

### 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│              DatabaseManager (Singleton)             │
│                                                      │
│  - _instance: DatabaseManager (static)              │
│  - users: Dict[str, User]                           │
│  - bookings: Dict[str, Booking]                     │
│  - payments: Dict[str, Payment]                     │
│  - feedbacks: Dict[str, Feedback]                   │
│                                                      │
│  + __new__(cls)                                     │
│  + __init__()                                       │
│  + save()                                           │
│  + _load_from_json()                                │
│  + _save_to_json()                                  │
└──────────────────────────────────────────────────────┘
         │                                    │
         │ Only one instance                 │
         │                                    │
    ┌────▼─────┐    ┌────────┐    ┌─────────▼──┐
    │ UI Layer │    │ Models │    │ Controllers│
    └──────────┘    └────────┘    └────────────┘
         All access same instance
```

### 💻 Implementation

**Singleton Pattern** (`patterns/singleton.py`):
```python
class DatabaseManager:
    """Singleton - Only one instance exists"""
    
    _instance = None
    DATA_FILE = "barbershop_data.json"
    
    def __new__(cls):
        # Create instance only once
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # Initialize only once
        if self._initialized:
            return
            
        self._initialized = True
        self.users = {}
        self.bookings = {}
        self.payments = {}
        self.feedbacks = {}
        
        # Load from JSON or create demo data
        if os.path.exists(self.DATA_FILE):
            self._load_from_json()
        else:
            self._initialize_demo_data()
            self._save_to_json()
    
    def save(self):
        """Persist data to JSON"""
        self._save_to_json()
```

### 🎯 Usage Example

```python
# First access - creates instance
db1 = DatabaseManager()
db1.users['user1'] = Customer(...)

# Second access - returns same instance
db2 = DatabaseManager()
print(db2.users)  # Contains 'user1'

# Proof of singleton
print(db1 is db2)  # True - same object

# From anywhere in the application
db = DatabaseManager()  # Always returns the same instance
db.save()  # Save to JSON
```

### ✨ Benefits

✅ **Single Source of Truth** - All data in one place  
✅ **Consistent State** - No data duplication  
✅ **Global Access** - Easy to access from anywhere  
✅ **Resource Efficiency** - Only one database instance  
✅ **Automatic Persistence** - Auto-save to JSON  

---

## 3. Observer Pattern - Notification System

### 📋 Purpose
Notifikasi otomatis ketika terjadi perubahan status booking tanpa tight coupling.

### 🏗️ Architecture

```
┌────────────────────────────────────────────────┐
│              Subject (Observable)              │
│                                                │
│  - _observers: List[Observer]                 │
│  + attach(observer: Observer)                 │
│  + detach(observer: Observer)                 │
│  + notify(event: str, data: dict)             │
└────────────────┬───────────────────────────────┘
                 │ extends
                 │
┌────────────────▼───────────────────────────────┐
│                  Booking                       │
│                                                │
│  + cancel()                                    │
│  + complete()                                  │
│  + notify('cancellation', {...})              │
└────────────────┬───────────────────────────────┘
                 │ notifies
                 │
    ┌────────────▼────────────┬─────────────┐
    │                         │             │
┌───▼────────────────┐  ┌────▼──────┐  ┌──▼─────┐
│NotificationObserver│  │EmailObserv│  │SMSObser│
│ (Streamlit UI)     │  │  (Future) │  │(Future)│
└────────────────────┘  └───────────┘  └────────┘
```

### 💻 Implementation

**Observer Interface** (`patterns/observer.py`):
```python
from abc import ABC, abstractmethod

class Observer(ABC):
    """Observer interface"""
    
    @abstractmethod
    def update(self, subject, event_type: str, data: dict):
        """Called when subject changes"""
        pass

class Subject(ABC):
    """Subject that observers watch"""
    
    def __init__(self):
        self._observers = []
    
    def attach(self, observer: Observer):
        """Add observer"""
        self._observers.append(observer)
    
    def notify(self, event_type: str, data: dict):
        """Notify all observers"""
        for observer in self._observers:
            observer.update(self, event_type, data)
```

**Concrete Observer** (`patterns/observer.py`):
```python
class NotificationObserver(Observer):
    """Displays notifications in Streamlit UI"""
    
    def update(self, subject, event_type: str, data: dict):
        notification = Notification(
            user_id=data.get('user_id'),
            notification_type=event_type,
            message=data.get('message'),
            channel='email'
        )
        st.success(f"📧 {notification.message}")
```

**Concrete Subject** (`models/booking.py`):
```python
class Booking(Subject):
    """Booking that notifies observers on changes"""
    
    def __init__(self, ...):
        Subject.__init__(self)
        # ... other initialization
    
    def cancel(self):
        """Cancel booking and notify observers"""
        self.status = BookingStatus.CANCELED
        
        # Notify all observers
        self.notify('cancellation', {
            'user_id': self.customer_id,
            'message': f'Booking {self.booking_id} has been canceled'
        })
    
    def complete(self):
        """Complete booking and notify observers"""
        self.status = BookingStatus.COMPLETED
        
        # Notify all observers
        self.notify('completion', {
            'user_id': self.customer_id,
            'message': f'Booking {self.booking_id} completed!'
        })
```

### 🎯 Usage Example

```python
# Setup observer
notification_observer = NotificationObserver()

# Create booking
booking = Booking(...)

# Attach observer to booking
booking.attach(notification_observer)

# When booking changes, observer is automatically notified
booking.cancel()     # → Observer shows cancellation notification
booking.complete()   # → Observer shows completion notification

# Easy to add more observers
email_observer = EmailObserver()
sms_observer = SMSObserver()
booking.attach(email_observer)
booking.attach(sms_observer)
```

### ✨ Benefits

✅ **Loose Coupling** - Booking doesn't know about observers  
✅ **Automatic Updates** - No manual notification calls  
✅ **Multiple Observers** - Easy to add more notification channels  
✅ **Event-Driven** - React to state changes automatically  

---

## 4. Factory Pattern - Service Creation

### 📋 Purpose
Membuat service dengan kombinasi decorators secara otomatis, menyembunyikan kompleksitas wrapping.

### 🏗️ Architecture

```
┌──────────────────────────────────────────────────┐
│            ServiceFactory (Factory)              │
│                                                  │
│  + BASE_SERVICES: Dict                          │
│  + DECORATORS: Dict                             │
│  + create_service(name, addons): Service        │
└────────────────┬─────────────────────────────────┘
                 │ creates
                 │
    ┌────────────▼───────────────┐
    │                            │
┌───▼──────────┐    ┌───────────▼──────────┐
│ BasicService │    │ Decorated Service    │
│              │ ───│ (with add-ons)       │
└──────────────┘    └──────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    │                    │
          ┌─────────▼────────┐  ┌───────▼────────┐
          │ HairWashDecorator│  │MassageDecorator│
          └──────────────────┘  └────────────────┘
```

### 💻 Implementation

**Factory Pattern** (`patterns/factory.py`):
```python
class ServiceFactory:
    """Factory for creating services with decorators"""
    
    BASE_SERVICES = {
        "Haircut": {"price": 50000, "duration": 30},
        "Shave": {"price": 30000, "duration": 20},
        "Styling": {"price": 80000, "duration": 45},
        "Coloring": {"price": 150000, "duration": 90},
    }
    
    DECORATORS = {
        "Hair Wash": HairWashDecorator,
        "Hair Spa": HairSpaDecorator,
        "Massage": MassageDecorator,
        "Hot Towel": HotTowelDecorator,
        "Premium Products": PremiumProductDecorator,
    }
    
    @staticmethod
    def create_service(base_name: str, addons: List[str]) -> Service:
        """
        Create service with decorators
        
        Args:
            base_name: Name of base service
            addons: List of addon names to apply
            
        Returns:
            Service with all decorators applied
        """
        # Create base service
        info = ServiceFactory.BASE_SERVICES[base_name]
        service = BasicService(base_name, info["price"], info["duration"])
        
        # Apply decorators dynamically
        for addon in addons:
            if addon in ServiceFactory.DECORATORS:
                decorator_class = ServiceFactory.DECORATORS[addon]
                service = decorator_class(service)
        
        return service
```

### 🎯 Usage Example

```python
# Without factory (manual, complex)
service = BasicService("Haircut", 50000, 30)
service = HairWashDecorator(service)
service = MassageDecorator(service)
service = HotTowelDecorator(service)

# With factory (simple, clean)
service = ServiceFactory.create_service(
    "Haircut",
    ["Hair Wash", "Massage", "Hot Towel"]
)

# Easy to use in UI
base_service = st.selectbox("Service", ServiceFactory.BASE_SERVICES.keys())
addons = st.multiselect("Add-ons", ServiceFactory.DECORATORS.keys())
service = ServiceFactory.create_service(base_service, addons)

print(f"Service: {service.get_description()}")
print(f"Price: Rp {service.get_price():,}")
print(f"Duration: {service.get_duration()} min")
```

### ✨ Benefits

✅ **Encapsulation** - Hides decorator complexity  
✅ **Centralized Logic** - All creation in one place  
✅ **Easy Maintenance** - Add new services/decorators easily  
✅ **Consistent Creation** - Same way to create services  

---

## Integration - All Patterns Working Together

```python
def create_booking_flow():
    """Example of all patterns working together"""
    
    # 1. SINGLETON - Get database instance
    db = DatabaseManager()
    
    # 2. FACTORY + DECORATOR - Create service with add-ons
    service = ServiceFactory.create_service(
        base_service="Haircut",
        addons=["Hair Wash", "Massage"]
    )
    # service now has: Haircut + Hair Wash + Massage (Decorator Pattern)
    
    # 3. Create booking
    booking = Booking(
        booking_id="BK001",
        customer_id="C001",
        service=service,  # Decorated service
        ...
    )
    
    # 4. OBSERVER - Attach notification observer
    notification_observer = NotificationObserver()
    booking.attach(notification_observer)
    
    # 5. SINGLETON - Save to database
    db.bookings["BK001"] = booking
    db.save()  # Persist to JSON
    
    # 6. OBSERVER - Notify on status change
    booking.notify('confirmation', {
        'user_id': 'C001',
        'message': 'Booking confirmed!'
    })
    # → NotificationObserver automatically displays notification
```

## Summary

| Pattern | Purpose | Location | Key Benefit |
|---------|---------|----------|-------------|
| **Decorator** | Dynamic feature addition | `services/` | Flexible service combinations |
| **Singleton** | Single database instance | `patterns/singleton.py` | Data consistency |
| **Observer** | Auto-notifications | `patterns/observer.py` | Loose coupling |
| **Factory** | Simplified creation | `patterns/factory.py` | Encapsulated complexity |

All patterns work together to create a clean, maintainable, and extensible architecture.


### Struktur
```
Service (Interface)
    ├── get_price(): float
    ├── get_description(): str
    └── get_duration(): int

BasicService (Concrete Component)
    └── implements Service

ServiceDecorator (Base Decorator)
    ├── wrappedService: Service
    └── implements Service

Concrete Decorators:
    ├── HairWashDecorator
    ├── HairSpaDecorator
    ├── MassageDecorator
    ├── HotTowelDecorator
    └── PremiumProductDecorator
```

### Contoh Implementasi

**File:** `services/service_interface.py`
```python
from abc import ABC, abstractmethod

class Service(ABC):
    @abstractmethod
    def get_price(self) -> float:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_duration(self) -> int:
        pass
```

**File:** `services/basic_services.py`
```python
class BasicHaircut(Service):
    def get_price(self) -> float:
        return 50000
    
    def get_description(self) -> str:
        return "Haircut"
    
    def get_duration(self) -> int:
        return 30
```

**File:** `services/service_decorators.py`
```python
class ServiceDecorator(Service):
    def __init__(self, wrapped_service: Service):
        self.wrapped_service = wrapped_service
    
    def get_price(self) -> float:
        return self.wrapped_service.get_price()
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description()
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration()

class HairWashDecorator(ServiceDecorator):
    def get_price(self) -> float:
        return self.wrapped_service.get_price() + 15000
    
    def get_description(self) -> str:
        return self.wrapped_service.get_description() + " + Hair Wash"
    
    def get_duration(self) -> int:
        return self.wrapped_service.get_duration() + 10
```

### Penggunaan
```python
# Cara 1: Manual wrapping
service = BasicHaircut()
service = HairWashDecorator(service)
service = MassageDecorator(service)

print(service.get_description())  # "Haircut + Hair Wash + Massage"
print(service.get_price())         # 80000 (50000 + 15000 + 15000)
print(service.get_duration())      # 50 (30 + 10 + 10)

# Cara 2: Menggunakan Factory Pattern
from patterns.factory import ServiceFactory

service = ServiceFactory.create_service(
    "Haircut", 
    ["Hair Wash", "Massage"]
)
```

## 2. Singleton Pattern - Database Manager

### Implementasi

**File:** `patterns/singleton.py`
```python
class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.users = {}
        self.bookings = {}
        # ... other data
```

### Penggunaan
```python
# Instance pertama
db1 = DatabaseManager()
db1.users['user1'] = Customer(...)

# Instance kedua (sama dengan instance pertama)
db2 = DatabaseManager()
print(db2.users)  # Berisi data yang sama dengan db1

# Membuktikan singleton
print(db1 is db2)  # True
```

## 3. Observer Pattern - Notification System

### Struktur
```
Subject (Observable)
    ├── observers: List[Observer]
    ├── attach(observer)
    ├── detach(observer)
    └── notify(event, data)

Observer (Interface)
    └── update(subject, event, data)

Concrete Observers:
    └── NotificationObserver
```

### Implementasi

**File:** `patterns/observer.py`
```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, subject, event_type: str, data: dict):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(self, event_type, data)

class NotificationObserver(Observer):
    def update(self, subject, event_type: str, data: dict):
        notification = Notification(
            user_id=data.get('user_id'),
            notification_type=event_type,
            message=data.get('message')
        )
        st.success(f"📧 {notification.message}")
```

**File:** `models/booking.py`
```python
class Booking(Subject):
    def __init__(self, ...):
        Subject.__init__(self)
        # ... other init
    
    def cancel(self):
        self.status = BookingStatus.CANCELED
        self.notify('cancellation', {
            'user_id': self.customer_id,
            'message': f'Booking {self.booking_id} canceled'
        })
    
    def complete(self):
        self.status = BookingStatus.COMPLETED
        self.notify('completion', {
            'user_id': self.customer_id,
            'message': f'Booking {self.booking_id} completed'
        })
```

### Penggunaan
```python
# Setup observer
notification_observer = NotificationObserver()

# Create booking
booking = Booking(...)

# Attach observer
booking.attach(notification_observer)

# Trigger notification
booking.cancel()  # Akan trigger notifikasi otomatis
```

## 4. Factory Pattern - Service Creation

### Implementasi

**File:** `patterns/factory.py`
```python
class ServiceFactory:
    BASE_SERVICES = {
        "Haircut": {"price": 50000, "duration": 30},
        "Shave": {"price": 30000, "duration": 20},
        # ...
    }
    
    DECORATORS = {
        "Hair Wash": HairWashDecorator,
        "Hair Spa": HairSpaDecorator,
        # ...
    }
    
    @staticmethod
    def create_service(base_service_name: str, addons: List[str]) -> Service:
        # Create base service
        service_info = ServiceFactory.BASE_SERVICES[base_service_name]
        service = BasicService(base_service_name, ...)
        
        # Apply decorators dynamically
        for addon in addons:
            decorator_class = ServiceFactory.DECORATORS[addon]
            service = decorator_class(service)
        
        return service
```

### Penggunaan
```python
# Tanpa factory (manual)
service = BasicService("Haircut", 50000, 30)
service = HairWashDecorator(service)
service = MassageDecorator(service)

# Dengan factory (lebih mudah)
service = ServiceFactory.create_service(
    "Haircut",
    ["Hair Wash", "Massage"]
)

# Keuntungan: Tidak perlu tahu detail implementasi decorator
# Factory akan menangani pembuatan dan wrapping
```

## Integration - Semua Pattern Bekerja Bersama

```python
def create_booking_form(user):
    # 1. DECORATOR PATTERN - User memilih service dan add-ons
    base_service = st.selectbox("Service", ServiceFactory.BASE_SERVICES.keys())
    addons = st.multiselect("Add-ons", ServiceFactory.DECORATORS.keys())
    
    # 2. FACTORY PATTERN - Membuat service dengan decorators
    service = ServiceFactory.create_service(base_service, addons)
    
    # Display info (Decorator pattern in action)
    st.write(f"Service: {service.get_description()}")
    st.write(f"Price: Rp {service.get_price():,}")
    st.write(f"Duration: {service.get_duration()} min")
    
    if st.button("Book"):
        # 3. SINGLETON PATTERN - Access database
        db = DatabaseManager()
        
        # Create booking
        booking = Booking(...)
        
        # 4. OBSERVER PATTERN - Attach notification observer
        booking.attach(st.session_state.notification_observer)
        
        # Save to database (Singleton)
        db.bookings[booking_id] = booking
        
        # Trigger notification (Observer)
        booking.notify('confirmation', {...})
```

## Manfaat Setiap Pattern

### Decorator Pattern
✅ Menambah fitur tanpa mengubah class asli
✅ Kombinasi fitur yang fleksibel
✅ Mudah menambah decorator baru
✅ Single Responsibility Principle

### Singleton Pattern
✅ Hanya satu instance database
✅ Global access point
✅ Resource efficiency
✅ Consistent state

### Observer Pattern
✅ Loose coupling antara booking dan notification
✅ Mudah menambah observer baru
✅ Automatic notification
✅ Event-driven architecture

### Factory Pattern
✅ Encapsulation object creation
✅ Centralized service creation logic
✅ Mudah maintain dan extend
✅ Abstraction dari complexity
