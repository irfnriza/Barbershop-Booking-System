# ============================================================================
# CUSTOMER DASHBOARD UI
# ============================================================================

import streamlit as st
from datetime import date, time
from models.user import Barber
from models.booking import Booking
from models.payment import Payment
from models.feedback import Feedback
from utils.enums import BookingStatus, PaymentMethod, PaymentStatus
from patterns.factory import ServiceFactory

def customer_dashboard():
    """Customer dashboard"""
    user = st.session_state.current_user
    st.title(f"👤 Welcome, {user.name}")
    
    tab1, tab2, tab3 = st.tabs(["📅 New Booking", "📋 My Bookings", "⭐ Give Feedback"])
    
    with tab1:
        create_booking_form(user)
    
    with tab2:
        show_customer_bookings(user)
    
    with tab3:
        show_feedback_form(user)


def create_booking_form(user):
    """Create new booking form"""
    st.subheader("Create New Booking")
    
    db = st.session_state.db
    
    # Service selection
    st.write("### 1️⃣ Select Base Service")
    base_service = st.selectbox(
        "Choose a service",
        options=list(ServiceFactory.BASE_SERVICES.keys())
    )
    
    service_info = ServiceFactory.BASE_SERVICES[base_service]
    st.info(f"💰 Base Price: Rp {service_info['price']:,} | ⏱️ Duration: {service_info['duration']} min")
    
    # Add-ons selection
    st.write("### 2️⃣ Select Add-ons (Optional)")
    addons = st.multiselect(
        "Choose add-ons",
        options=list(ServiceFactory.DECORATORS.keys())
    )
    
    # Create service with decorators to show price
    service = ServiceFactory.create_service(base_service, addons)
    
    st.success(f"""
    **Selected Service:** {service.get_description()}
    
    💰 **Total Price:** Rp {service.get_price():,}
    
    ⏱️ **Total Duration:** {service.get_duration()} minutes
    """)
    
    # Date and time selection
    st.write("### 3️⃣ Select Date & Time")
    col1, col2 = st.columns(2)
    
    with col1:
        booking_date = st.date_input("Date", min_value=date.today())
    
    with col2:
        booking_time = st.time_input("Time", value=time(9, 0))
    
    # Barber selection
    st.write("### 4️⃣ Select Barber (Optional)")
    barbers = [u for u in db.users.values() if u.role.value == "barber" and u.is_available]
    barber_options = ["Any Available"] + [f"{b.name} - {b.specialization}" for b in barbers]
    selected_barber = st.selectbox("Choose barber", barber_options)
    
    barber_id = None
    if selected_barber != "Any Available":
        barber_id = barbers[barber_options.index(selected_barber) - 1].user_id
    
    # Submit button
    if st.button("🎯 Confirm Booking", type="primary", use_container_width=True):
        # Create booking
        booking_id = f"BK{len(db.bookings) + 1:04d}"
        final_service = ServiceFactory.create_service(base_service, addons)
        
        booking = Booking(
            booking_id=booking_id,
            customer_id=user.user_id,
            service=final_service,
            barber_id=barber_id,
            booking_date=booking_date,
            booking_time=booking_time,
            status=BookingStatus.SCHEDULED
        )
        
        # Attach observer
        booking.attach(st.session_state.notification_observer)
        
        db.bookings[booking_id] = booking
        
        # Save to JSON
        db.save()
        
        # Notify
        booking.notify('confirmation', {
            'user_id': user.user_id,
            'message': f'Booking {booking_id} confirmed for {booking_date} at {booking_time}'
        })
        
        st.success(f"✅ Booking created successfully! Booking ID: {booking_id}")
        st.balloons()


def show_customer_bookings(user):
    """Show customer's bookings"""
    st.subheader("My Bookings")
    
    db = st.session_state.db
    user_bookings = [b for b in db.bookings.values() if b.customer_id == user.user_id]
    
    if not user_bookings:
        st.info("No bookings yet. Create your first booking!")
        return
    
    for booking in sorted(user_bookings, key=lambda x: x.created_at, reverse=True):
        with st.expander(f"🎫 Booking {booking.booking_id} - {booking.status.value.upper()}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Service:** {booking.service.get_description()}")
                st.write(f"**Date:** {booking.booking_date}")
                st.write(f"**Time:** {booking.booking_time}")
                st.write(f"**Duration:** {booking.service.get_duration()} minutes")
                st.write(f"**Price:** Rp {booking.service.get_price():,}")
                
                if booking.barber_id:
                    barber = db.users.get(booking.barber_id)
                    st.write(f"**Barber:** {barber.name if barber else 'N/A'}")
            
            with col2:
                status_color = {
                    BookingStatus.SCHEDULED: "🟡",
                    BookingStatus.IN_PROGRESS: "🔵",
                    BookingStatus.COMPLETED: "🟢",
                    BookingStatus.CANCELED: "🔴"
                }
                st.write(f"### {status_color.get(booking.status, '⚪')} {booking.status.value.upper()}")
                
                if booking.status == BookingStatus.SCHEDULED:
                    if st.button(f"❌ Cancel", key=f"cancel_{booking.booking_id}"):
                        if booking.cancel():
                            db.save()  # Save after cancellation
                            st.success("Booking canceled")
                            st.rerun()
                
                # Check payment status
                payment = next((p for p in db.payments.values() 
                              if p.booking_id == booking.booking_id), None)
                if payment:
                    st.write(f"💳 Payment: {payment.payment_status.value}")
                elif booking.status != BookingStatus.CANCELED:
                    if st.button(f"💳 Pay Now", key=f"pay_{booking.booking_id}"):
                        process_payment(booking)


def process_payment(booking):
    """Process payment for booking"""
    db = st.session_state.db
    
    payment_id = f"PAY{len(db.payments) + 1:04d}"
    payment = Payment(
        payment_id=payment_id,
        booking_id=booking.booking_id,
        amount=booking.service.get_price(),
        payment_method=PaymentMethod.E_WALLET,
        payment_status=PaymentStatus.PENDING
    )
    
    if payment.process_payment():
        db.payments[payment_id] = payment
        db.save()  # Save payment to JSON
        st.success(f"✅ Payment successful! Transaction ID: {payment.transaction_id}")
        st.rerun()


def show_feedback_form(user):
    """Show feedback form for completed bookings"""
    st.subheader("Give Feedback")
    
    db = st.session_state.db
    completed_bookings = [b for b in db.bookings.values() 
                         if b.customer_id == user.user_id and b.status == BookingStatus.COMPLETED]
    
    # Filter bookings without feedback
    bookings_without_feedback = [b for b in completed_bookings 
                                 if not any(f.booking_id == b.booking_id for f in db.feedbacks.values())]
    
    if not bookings_without_feedback:
        st.info("No completed bookings to review.")
        return
    
    booking_options = [f"{b.booking_id} - {b.service.get_description()}" 
                      for b in bookings_without_feedback]
    selected_booking_str = st.selectbox("Select booking to review", booking_options)
    
    if selected_booking_str:
        booking_id = selected_booking_str.split(" - ")[0]
        booking = db.bookings[booking_id]
        
        rating = st.slider("Rating (1-5 stars)", 1, 5, 5)
        comment = st.text_area("Comment (optional)")
        
        if st.button("📤 Submit Feedback", type="primary"):
            feedback_id = f"FB{len(db.feedbacks) + 1:04d}"
            feedback = Feedback(
                feedback_id=feedback_id,
                booking_id=booking.booking_id,
                customer_id=user.user_id,
                barber_id=booking.barber_id or "",
                rating=rating,
                comment=comment
            )
            db.feedbacks[feedback_id] = feedback
            db.save()  # Save feedback to JSON
            st.success("✅ Thank you for your feedback!")
            st.balloons()
            st.rerun()
