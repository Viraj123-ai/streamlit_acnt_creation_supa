import streamlit as st
import requests
import re
from typing import Dict, Optional

class SignupApp:
    def __init__(self):
        self.API_URL = "https://auth-service-101415335665.asia-south1.run.app"  
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_password(password: str) -> tuple[bool, str]:
        """
        Validate password strength
        Returns: (is_valid, message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        return True, "Password is valid"

    def create_account(self, user_data: Dict) -> Optional[Dict]:
        """Send signup request to API"""
        try:
            response = requests.post(f"{self.API_URL}/signup", json=user_data)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error occurred')}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def render(self):
        """Render the signup form"""
        st.title("Create Account")
        
        with st.form("signup_form"):
            # Personal Information
            st.subheader("Personal Information")
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Email Address")
                full_name = st.text_input("Full Name")
                profile_pic_url = st.text_input("Profile Picture URL")
            
            with col2:
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
            
            # Professional Information
            st.subheader("Professional Information")
            col3, col4 = st.columns(2)
            with col3:
                job_role = st.text_input("Job Role")
                company_name = st.text_input("Company Name")
            
            with col4:
                location = st.text_input("Location")
            
            # Password strength indicators
            if password:
                is_valid, message = self.is_valid_password(password)
                if not is_valid:
                    st.warning(message)
                else:
                    st.success("Strong password!")

            submitted = st.form_submit_button("Create Account")

            if submitted:
                # Validate inputs
                if not email or not password or not confirm_password:
                    st.error("Please fill in all required fields (Email and Password)")
                    return
                
                # if not self.is_valid_email(email):
                #     st.error("Please enter a valid email address")
                #     return
                
                if password != confirm_password:
                    st.error("Passwords do not match")
                    return
                
                is_valid_pwd, pwd_message = self.is_valid_password(password)
                if not is_valid_pwd:
                    st.error(pwd_message)
                    return

                # Create user data dictionary
                user_data = {
                    "email": email,
                    "full_name": full_name,
                    "profile_pic_url": profile_pic_url,
                    "job_role": job_role,
                    "company_name": company_name,
                    "location": location,
                    "password": password
                }

                # Send signup request
                result = self.create_account(user_data)
                if result:
                    st.success("Account created successfully!")
                    st.json(result)  # Display the created user data

def main():
    app = SignupApp()
    app.render()

if __name__ == "__main__":
    main()