# ============================================================================
# BARBER DASHBOARD UI
# ============================================================================

import streamlit as st
from datetime import date
from utils.enums import BookingStatus

def barber_dashboard():
    """Barber dashboard"""
    user = st.session_state.current_user
    st.title(f"✂️ Barber Dashboard - {user.name}")
    
    tab1, tab2, tab3 = st.tabs(["📅 My Schedule", "📊 My Stats", "⭐ My Reviews"])
    
    with tab1:
        show_barber_schedule(user)
    
    with tab2:
        show_barber_stats(user)
    
    with tab3:
        show_barber_reviews(user)


def show_barber_schedule(barber):
    """Show barber's schedule"""
    st.subheader("My Schedule")
    
    db = st.session_state.db
    
    # Toggle availability
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Status:** {'🟢 Available' if barber.is_available else '🔴 Unavailable'}")
    with col2:
        if st.button("Toggle Status"):
            barber.is_available = not barber.is_available
            db.save()  # Save to JSON
            st.rerun()
    
    st.divider()
    
    # Select date
    selected_date = st.date_input("Select Date", value=date.today())
    
    # Get bookings for this barber on selected date
    barber_bookings = [b for b in db.bookings.values() 
                      if b.barber_id == barber.user_id and 
                      b.booking_date == selected_date and
                      b.status != BookingStatus.CANCELED]
    
    if not barber_bookings:
        st.info(f"No bookings for {selected_date}")
        return
    
    barber_bookings.sort(key=lambda x: x.booking_time)
    
    for booking in barber_bookings:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.write(f"**{booking.booking_time}**")
                status_emoji = {
                    BookingStatus.SCHEDULED: "🟡",
                    BookingStatus.IN_PROGRESS: "🔵",
                    BookingStatus.COMPLETED: "🟢"
                }
                st.write(f"{status_emoji.get(booking.status, '⚪')} {booking.status.value}")
            
            with col2:
                customer = db.users.get(booking.customer_id)
                st.write(f"**Customer:** {customer.name if customer else 'N/A'}")
                st.write(f"**Service:** {booking.service.get_description()}")
                st.write(f"**Duration:** {booking.service.get_duration()} min")
            
            with col3:
                if booking.status == BookingStatus.SCHEDULED:
                    if st.button("▶️ Start", key=f"start_barber_{booking.booking_id}"):
                        booking.status = BookingStatus.IN_PROGRESS
                        db.save()  # Save to JSON
                        st.rerun()
                elif booking.status == BookingStatus.IN_PROGRESS:
                    if st.button("✅ Complete", key=f"complete_barber_{booking.booking_id}"):
                        booking.complete()
                        db.save()  # Save to JSON
                        st.rerun()
            
            st.divider()


def show_barber_stats(barber):
    """Show barber statistics"""
    st.subheader("My Statistics")
    
    db = st.session_state.db
    
    # Get all bookings for this barber
    all_bookings = [b for b in db.bookings.values() if b.barber_id == barber.user_id]
    completed = [b for b in all_bookings if b.status == BookingStatus.COMPLETED]
    
    # Get feedbacks
    feedbacks = [f for f in db.feedbacks.values() if f.barber_id == barber.user_id]
    avg_rating = sum(f.rating for f in feedbacks) / len(feedbacks) if feedbacks else 0
    
    # Calculate revenue
    revenue = sum(b.service.get_price() for b in completed)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Bookings", len(all_bookings))
    
    with col2:
        st.metric("Completed", len(completed))
    
    with col3:
        st.metric("Avg Rating", f"{avg_rating:.1f} ⭐")
    
    with col4:
        st.metric("Total Revenue", f"Rp {revenue:,.0f}")
    
    # Show recent activity
    st.write("### Recent Bookings")
    recent_bookings = sorted(all_bookings, key=lambda x: x.created_at, reverse=True)[:5]
    
    for booking in recent_bookings:
        customer = db.users.get(booking.customer_id)
        col1, col2, col3 = st.columns([2, 3, 2])
        
        with col1:
            st.write(f"**{booking.booking_date}**")
        
        with col2:
            st.write(f"{customer.name if customer else 'N/A'} - {booking.service.get_description()}")
        
        with col3:
            status_color = {
                BookingStatus.SCHEDULED: "🟡",
                BookingStatus.IN_PROGRESS: "🔵",
                BookingStatus.COMPLETED: "🟢",
                BookingStatus.CANCELED: "🔴"
            }
            st.write(f"{status_color.get(booking.status, '⚪')} {booking.status.value}")
        
        st.divider()


def show_barber_reviews(barber):
    """Show reviews for this barber"""
    st.subheader("My Reviews")
    
    db = st.session_state.db
    feedbacks = [f for f in db.feedbacks.values() if f.barber_id == barber.user_id]
    
    if not feedbacks:
        st.info("No reviews yet.")
        return
    
    # Calculate rating distribution
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for feedback in feedbacks:
        rating_counts[feedback.rating] += 1
    
    st.write("### Rating Distribution")
    for rating in range(5, 0, -1):
        count = rating_counts[rating]
        percentage = (count / len(feedbacks) * 100) if feedbacks else 0
        st.write(f"{'⭐' * rating} ({rating}) - {count} reviews ({percentage:.1f}%)")
        st.progress(percentage / 100)
    
    st.divider()
    
    # Show individual reviews
    st.write("### Customer Comments")
    for feedback in sorted(feedbacks, key=lambda x: x.created_at, reverse=True):
        customer = db.users.get(feedback.customer_id)
        booking = db.bookings.get(feedback.booking_id)
        
        with st.expander(f"⭐ {feedback.rating} stars - {feedback.created_at.strftime('%Y-%m-%d')}"):
            st.write(f"**Customer:** {customer.name if customer else 'N/A'}")
            if booking:
                st.write(f"**Service:** {booking.service.get_description()}")
            if feedback.comment:
                st.write(f"**Comment:** {feedback.comment}")
