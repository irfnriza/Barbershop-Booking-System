# ============================================================================
# AUTHENTICATION UI - Login and Registration
# ============================================================================

import streamlit as st
from models.user import Customer
from utils.enums import UserRole

def login_page():
    """Login page"""
    st.title("🪒 Barbershop Booking System")
    st.subheader("Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        col_login, col_register = st.columns(2)
        
        with col_login:
            if st.button("🔐 Login", use_container_width=True):
                db = st.session_state.db
                user = next((u for u in db.users.values() 
                           if u.email == email and u.password == password), None)
                if user:
                    st.session_state.current_user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        with col_register:
            if st.button("📝 Register", use_container_width=True):
                st.session_state.show_register = True
                st.rerun()
        
        # Demo accounts info
        with st.expander("🔑 Demo Accounts"):
            st.info("""
            **Customer:** (Register new account)
            
            **Barber:**
            - Email: john@barber.com
            - Password: 1234
            
            **Owner/Admin:**
            - Email: admin@barber.com
            - Password: admin
            """)

def register_page():
    """Registration page"""
    st.title("📝 Register New Account")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        col_back, col_submit = st.columns(2)
        
        with col_back:
            if st.button("⬅️ Back to Login", use_container_width=True):
                st.session_state.show_register = False
                st.rerun()
        
        with col_submit:
            if st.button("✅ Register", use_container_width=True):
                if password != confirm_password:
                    st.error("Passwords don't match")
                elif not all([name, email, phone, password]):
                    st.error("All fields are required")
                else:
                    db = st.session_state.db
                    # Check if email exists
                    if any(u.email == email for u in db.users.values()):
                        st.error("Email already registered")
                    else:
                        user_id = f"C{len([u for u in db.users.values() if u.role.value == 'customer']) + 1:03d}"
                        customer = Customer(user_id, name, email, password, phone)
                        db.users[user_id] = customer
                        db.save()  # Save to JSON
                        st.success("Registration successful! Please login.")
                        st.session_state.show_register = False
                        st.rerun()
