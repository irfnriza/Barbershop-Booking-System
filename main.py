# ============================================================================
# BARBERSHOP BOOKING SYSTEM - MAIN APPLICATION
# Design Patterns Implementation:
# 1. Singleton Pattern - DatabaseManager
# 2. Decorator Pattern - Service Decorators
# 3. Observer Pattern - Notification System
# 4. Factory Pattern - Service Factory
# ============================================================================

import streamlit as st
from patterns import DatabaseManager, NotificationObserver
from ui import login_page, register_page, customer_dashboard, barber_dashboard, owner_dashboard
from utils.enums import UserRole

def init_session_state():
    """Initialize session state"""
    if 'db' not in st.session_state:
        st.session_state.db = DatabaseManager()
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'notification_observer' not in st.session_state:
        st.session_state.notification_observer = NotificationObserver()


def main():
    """Main application"""
    st.set_page_config(
        page_title="Barbershop Booking System",
        page_icon="🪒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    init_session_state()
    
    # Check if user is logged in
    if st.session_state.current_user is None:
        if 'show_register' in st.session_state and st.session_state.show_register:
            register_page()
        else:
            login_page()
    else:
        user = st.session_state.current_user
        
        # Sidebar
        with st.sidebar:
            st.title("🪒 Barbershop")
            st.write(f"**Logged in as:**")
            st.write(f"👤 {user.name}")
            st.write(f"📧 {user.email}")
            st.write(f"🎭 Role: {user.role.value}")
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.current_user = None
                st.rerun()
            
            st.divider()
            
            st.write("### 🎨 Design Patterns Used:")
            st.info("""
            1. **Singleton Pattern**
               - DatabaseManager
            
            2. **Decorator Pattern**
               - Service add-ons
            
            3. **Observer Pattern**
               - Notifications
            
            4. **Factory Pattern**
               - Service creation
            """)
        
        # Main content based on user role
        if user.role.value == "customer":
            customer_dashboard()
        elif user.role.value == "barber":
            barber_dashboard()
        elif user.role.value == "owner":
            owner_dashboard()
        else:
            st.error(f"Unknown user role: {user.role}")


if __name__ == "__main__":
    main()
