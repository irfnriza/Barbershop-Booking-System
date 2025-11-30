# ============================================================================
# OWNER/ADMIN DASHBOARD UI
# ============================================================================

import streamlit as st
from datetime import date, timedelta
from utils.enums import BookingStatus, PaymentStatus

def owner_dashboard():
    """Owner/Admin dashboard"""
    user = st.session_state.current_user
    st.title(f"👔 Admin Dashboard - {user.name}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📅 Today's Schedule", "💰 Revenue", "⭐ Feedbacks"])
    
    with tab1:
        show_overview()
    
    with tab2:
        show_daily_schedule()
    
    with tab3:
        show_revenue_report()
    
    with tab4:
        show_all_feedbacks()


def show_overview():
    """Show overview statistics"""
    st.subheader("Business Overview")
    
    db = st.session_state.db
    
    # Calculate statistics
    total_bookings = len(db.bookings)
    completed_bookings = len([b for b in db.bookings.values() if b.status == BookingStatus.COMPLETED])
    total_revenue = sum(p.amount for p in db.payments.values() if p.payment_status == PaymentStatus.PAID)
    avg_rating = sum(f.rating for f in db.feedbacks.values()) / len(db.feedbacks) if db.feedbacks else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Bookings", total_bookings)
    
    with col2:
        st.metric("Completed", completed_bookings)
    
    with col3:
        st.metric("Revenue", f"Rp {total_revenue:,.0f}")
    
    with col4:
        st.metric("Avg Rating", f"{avg_rating:.1f} ⭐")


def show_daily_schedule():
    """Show today's schedule"""
    st.subheader(f"Today's Schedule - {date.today()}")
    
    db = st.session_state.db
    today_bookings = [b for b in db.bookings.values() 
                     if b.booking_date == date.today() and b.status != BookingStatus.CANCELED]
    
    if not today_bookings:
        st.info("No bookings for today.")
        return
    
    # Sort by time
    today_bookings.sort(key=lambda x: x.booking_time)
    
    for booking in today_bookings:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                st.write(f"**{booking.booking_time}**")
                st.write(f"🎫 {booking.booking_id}")
            
            with col2:
                customer = db.users.get(booking.customer_id)
                st.write(f"👤 {customer.name if customer else 'N/A'}")
                st.write(f"📞 {customer.phone if customer else 'N/A'}")
            
            with col3:
                st.write(f"✂️ {booking.service.get_description()}")
                st.write(f"⏱️ {booking.service.get_duration()} min")
            
            with col4:
                if booking.status == BookingStatus.SCHEDULED:
                    if st.button("▶️ Start", key=f"start_{booking.booking_id}"):
                        booking.status = BookingStatus.IN_PROGRESS
                        db.save()  # Save to JSON
                        st.rerun()
                elif booking.status == BookingStatus.IN_PROGRESS:
                    if st.button("✅ Done", key=f"done_{booking.booking_id}"):
                        booking.complete()
                        db.save()  # Save to JSON
                        st.rerun()
            
            st.divider()


def show_revenue_report():
    """Show revenue report"""
    st.subheader("Revenue Report")
    
    db = st.session_state.db
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("To", value=date.today())
    
    # Filter payments
    payments_in_range = [p for p in db.payments.values() 
                        if p.payment_status == PaymentStatus.PAID and 
                        p.payment_date and
                        start_date <= p.payment_date.date() <= end_date]
    
    if not payments_in_range:
        st.info("No revenue data for selected period.")
        return
    
    total_revenue = sum(p.amount for p in payments_in_range)
    total_transactions = len(payments_in_range)
    avg_transaction = total_revenue / total_transactions if total_transactions > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Revenue", f"Rp {total_revenue:,.0f}")
    
    with col2:
        st.metric("Transactions", total_transactions)
    
    with col3:
        st.metric("Avg per Transaction", f"Rp {avg_transaction:,.0f}")
    
    # Show payment details
    st.write("### Transaction Details")
    for payment in sorted(payments_in_range, key=lambda x: x.payment_date, reverse=True):
        booking = db.bookings.get(payment.booking_id)
        if booking:
            col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
            
            with col1:
                st.write(f"**{payment.payment_date.strftime('%Y-%m-%d %H:%M')}**")
            
            with col2:
                st.write(f"{booking.service.get_description()}")
            
            with col3:
                st.write(f"💳 {payment.payment_method.value}")
            
            with col4:
                st.write(f"**Rp {payment.amount:,.0f}**")
            
            st.divider()


def show_all_feedbacks():
    """Show all customer feedbacks"""
    st.subheader("Customer Feedbacks")
    
    db = st.session_state.db
    
    if not db.feedbacks:
        st.info("No feedbacks yet.")
        return
    
    # Calculate average rating per barber
    barber_ratings = {}
    for feedback in db.feedbacks.values():
        if feedback.barber_id:
            if feedback.barber_id not in barber_ratings:
                barber_ratings[feedback.barber_id] = []
            barber_ratings[feedback.barber_id].append(feedback.rating)
    
    # Show barber ratings
    if barber_ratings:
        st.write("### Barber Performance")
        for barber_id, ratings in barber_ratings.items():
            barber = db.users.get(barber_id)
            if barber:
                avg_rating = sum(ratings) / len(ratings)
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{barber.name}** - {barber.specialization}")
                
                with col2:
                    st.write(f"⭐ {avg_rating:.1f} / 5.0")
                
                with col3:
                    st.write(f"📊 {len(ratings)} reviews")
        
        st.divider()
    
    # Show all feedbacks
    st.write("### All Feedbacks")
    for feedback in sorted(db.feedbacks.values(), key=lambda x: x.created_at, reverse=True):
        with st.expander(f"⭐ {feedback.rating} stars - {feedback.created_at.strftime('%Y-%m-%d')}"):
            customer = db.users.get(feedback.customer_id)
            barber = db.users.get(feedback.barber_id)
            booking = db.bookings.get(feedback.booking_id)
            
            st.write(f"**Customer:** {customer.name if customer else 'N/A'}")
            st.write(f"**Barber:** {barber.name if barber else 'N/A'}")
            if booking:
                st.write(f"**Service:** {booking.service.get_description()}")
            
            if feedback.comment:
                st.write(f"**Comment:** {feedback.comment}")
