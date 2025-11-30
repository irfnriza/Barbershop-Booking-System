# Barbershop Booking System

Sistem manajemen booking barbershop dengan implementasi 4 Design Patterns utama untuk menciptakan arsitektur yang scalable, maintainable, dan extensible.

## 🎯 Overview

Aplikasi ini adalah sistem booking untuk barbershop yang memungkinkan customer membuat booking, barber mengelola jadwal, dan owner memonitor bisnis. Sistem dibangun dengan mengimplementasikan design patterns untuk memastikan kode yang clean dan mudah dikembangkan.

## 🎨 Design Patterns Architecture

### 1. **Singleton Pattern** - Database Manager
Memastikan hanya ada satu instance database di seluruh aplikasi untuk konsistensi data.

**Implementation:** `patterns/singleton.py`
- Menjamin single source of truth untuk semua data
- Persistent storage menggunakan JSON
- Auto-save setiap perubahan data

### 2. **Decorator Pattern** - Service Enhancements
Menambahkan fitur tambahan (add-ons) ke layanan dasar secara dinamis tanpa mengubah class aslinya.

**Implementation:** `services/`
- Base services: Haircut, Shave, Styling, Coloring
- Decorators: Hair Wash, Hair Spa, Massage, Hot Towel, Premium Products
- Kombinasi fleksibel sesuai kebutuhan customer

### 3. **Observer Pattern** - Notification System
Sistem notifikasi otomatis ketika terjadi perubahan status booking.

**Implementation:** `patterns/observer.py`, `models/booking.py`
- Auto-notify saat booking dibuat, dicancel, atau diselesaikan
- Loose coupling antara booking dan notification
- Mudah menambah observer baru

### 4. **Factory Pattern** - Service Creation
Membuat service dengan kombinasi decorators secara otomatis.

**Implementation:** `patterns/factory.py`
- Centralized service creation logic
- Abstraksi kompleksitas decorator wrapping
- Mudah maintain dan extend

## 📁 Struktur Proyek

```
uas-apl/
├── main.py          # Entry point aplikasi
├── barbershop_data.json        # Data persistence (auto-generated)
│
├── models/                     # Domain Models
│   ├── user.py                # User, Customer, Barber, Owner
│   ├── booking.py             # Booking dengan Observer pattern
│   ├── payment.py             # Payment processing
│   ├── feedback.py            # Customer feedback & rating
│   └── notification.py        # Notification model
│
├── services/                   # Decorator Pattern
│   ├── service_interface.py   # Service interface (Component)
│   ├── basic_services.py      # Concrete components
│   └── service_decorators.py  # Concrete decorators
│
├── patterns/                   # Design Patterns
│   ├── singleton.py           # DatabaseManager (Singleton)
│   ├── observer.py            # Notification system (Observer)
│   └── factory.py             # ServiceFactory (Factory)
│
├── ui/                        # User Interface
│   ├── auth.py               # Login & Registration
│   ├── customer_dashboard.py # Customer interface
│   ├── barber_dashboard.py   # Barber interface
│   └── owner_dashboard.py    # Owner/Admin interface
│
└── utils/                     # Utilities
    └── enums.py              # Enumerations (Status, Roles, etc.)
```

## 🚀 Instalasi & Menjalankan

### Prerequisites
```bash
Python 3.8+
Streamlit
```

### Install Dependencies
```bash
pip install streamlit
```

### Menjalankan Aplikasi
```bash
cd uas-apl
streamlit run main.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## 👥 User Roles & Features

### 1. Customer
**Login:** Register akun baru

**Features:**
- 📅 **Create Booking**
  - Pilih base service (Haircut, Shave, Styling, Coloring)
  - Tambah add-ons (Hair Wash, Spa, Massage, dll)
  - Pilih tanggal, waktu, dan barber
  - Lihat total harga dan durasi (Decorator Pattern)
- 📋 **View Bookings** - Lihat semua booking (scheduled, completed, canceled)
- 💳 **Payment** - Bayar booking dengan e-wallet
- ❌ **Cancel Booking** - Cancel min 2 jam sebelum appointment
- ⭐ **Give Feedback** - Rating dan review setelah service selesai

### 2. Barber
**Login:** 
- Email: john@barber.com / jane@barber.com
- Password: 1234

**Features:**
- 📅 **My Schedule** - Lihat jadwal booking per tanggal
- 🔄 **Toggle Availability** - Set status available/unavailable
- ▶️ **Start Service** - Mulai service untuk customer
- ✅ **Complete Service** - Tandai service selesai
- 📊 **Statistics** - Total bookings, revenue, avg rating
- ⭐ **My Reviews** - Lihat semua feedback dari customer

### 3. Owner/Admin
**Login:**
- Email: admin@barber.com
- Password: admin

**Features:**
- 📊 **Business Overview** - Total bookings, revenue, avg rating
- 📅 **Today's Schedule** - Jadwal semua booking hari ini
- 💰 **Revenue Report** - Laporan pendapatan dengan filter tanggal
- ⭐ **All Feedbacks** - Lihat semua feedback & barber performance
- 🎯 **Manage Bookings** - Start/complete service dari admin panel

## 💰 Services & Pricing

### Base Services (Component)
| Service | Price | Duration |
|---------|-------|----------|
| Haircut | Rp 50,000 | 30 min |
| Shave | Rp 30,000 | 20 min |
| Styling | Rp 80,000 | 45 min |
| Coloring | Rp 150,000 | 90 min |

### Add-ons (Decorators)
| Add-on | Extra Price | Extra Duration |
|--------|-------------|----------------|
| Hair Wash | +Rp 15,000 | +10 min |
| Hair Spa | +Rp 30,000 | +20 min |
| Massage | +Rp 15,000 | +10 min |
| Hot Towel | +Rp 10,000 | +5 min |
| Premium Products | +Rp 25,000 | - |

**Contoh:** Haircut + Hair Wash + Massage = Rp 80,000 (50min)

## 🔄 Business Flow

1. **Customer Register/Login** → Masuk ke dashboard
2. **Create Booking** → Pilih service + add-ons (Factory Pattern)
3. **System Creates Service** → Decorator Pattern wraps base service
4. **Booking Confirmed** → Observer Pattern sends notification
5. **Customer Pay** → Payment recorded
6. **Barber Starts Service** → Status updated to in-progress
7. **Barber Completes** → Status completed, notification sent
8. **Customer Give Feedback** → Rating & review saved
9. **Owner View Reports** → Analytics & revenue

## 💾 Data Persistence

Data disimpan otomatis di `barbershop_data.json`:
- ✅ Auto-save setiap perubahan
- ✅ Auto-load saat aplikasi start
- ✅ Persistent meskipun restart
- ✅ Human-readable JSON format
- ✅ Mudah backup (copy file JSON)

**Auto-save triggered on:**
- User registration
- Booking creation/cancellation
- Payment processing
- Feedback submission
- Barber availability toggle
- Service status changes

## 🎯 Design Pattern Benefits

### Singleton Pattern
✅ Single database instance
✅ Consistent data state
✅ Centralized data management

### Decorator Pattern
✅ Flexible service combinations
✅ Easy to add new add-ons
✅ No modification to existing classes
✅ Dynamic pricing calculation

### Observer Pattern
✅ Automatic notifications
✅ Loose coupling
✅ Easy to add new observers
✅ Event-driven architecture

### Factory Pattern
✅ Simplified service creation
✅ Encapsulated complexity
✅ Centralized business logic
✅ Easy to maintain

## 🛠 Technologies

- **Python 3.8+**
- **Streamlit** - Web framework
- **JSON** - Data persistence
- **Design Patterns** - Clean architecture

## 📖 Documentation

- `DESIGN_PATTERNS.md` - Detailed design patterns implementation guide
- `classDiagramdocorator.mmd` - Decorator pattern class diagram

## 🔍 Key Features

✅ Multi-role authentication (Customer, Barber, Owner)
✅ Dynamic service pricing with Decorator Pattern
✅ Real-time notifications with Observer Pattern
✅ Centralized data management with Singleton Pattern
✅ Flexible service creation with Factory Pattern
✅ Payment processing system
✅ Rating & feedback system
✅ Revenue reporting & analytics
✅ Booking management with validation
✅ Persistent JSON storage

## 📝 Notes

- Data stored in `barbershop_data.json` (auto-generated)
- Minimum 2 hours for booking cancellation
- All prices in Indonesian Rupiah (IDR)
- Time in 24-hour format

