import streamlit as st
import json
import os
from hashlib import sha256

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'users' not in st.session_state:
    st.session_state.users = {}

# Load existing users from file if it exists
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

# Save users to file
def save_users():
    with open('users.json', 'w') as f:
        json.dump(st.session_state.users, f)

# Hash password
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Initialize users
st.session_state.users = load_users()

def main():
    st.title("User Profile Manager")
    
    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.header("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login"):
                if login_username in st.session_state.users:
                    if st.session_state.users[login_username]['password'] == hash_password(login_password):
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.rerun()
                    else:
                        st.error("Incorrect password!")
                else:
                    st.error("Username not found!")
        
        with tab2:
            st.header("Sign Up")
            new_username = st.text_input("Username", key="new_username")
            new_password = st.text_input("Password", type="password", key="new_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.button("Sign Up"):
                if new_username in st.session_state.users:
                    st.error("Username already exists!")
                elif new_password != confirm_password:
                    st.error("Passwords don't match!")
                else:
                    st.session_state.users[new_username] = {
                        'password': hash_password(new_password),
                        'profile': {}
                    }
                    save_users()
                    st.success("Account created successfully! Please login.")
    
    else:
        st.header(f"Welcome, {st.session_state.username}!")
        
        # Profile Information Form
        st.subheader("Your Profile")
        user_data = st.session_state.users[st.session_state.username]['profile']
        
        name = st.text_input("Name", value=user_data.get('name', ''))
        age = st.number_input("Age", min_value=0, max_value=150, value=int(user_data.get('age', 0)))
        city = st.text_input("City", value=user_data.get('city', ''))
        phone = st.text_input("Phone Number", value=user_data.get('phone', ''))
        
        if st.button("Save Profile"):
            st.session_state.users[st.session_state.username]['profile'] = {
                'name': name,
                'age': age,
                'city': city,
                'phone': phone
            }
            save_users()
            st.success("Profile updated successfully!")
        
        # Download Profile
        if st.button("Download Profile"):
            profile_data = st.session_state.users[st.session_state.username]['profile']
            profile_text = f"""User Profile
-------------------
Name: {profile_data.get('name', 'Not provided')}
Age: {profile_data.get('age', 'Not provided')}
City: {profile_data.get('city', 'Not provided')}
Phone: {profile_data.get('phone', 'Not provided')}
"""
            st.download_button(
                label="Download Profile as Text",
                data=profile_text,
                file_name=f"profile_{st.session_state.username}.txt",
                mime="text/plain"
            )
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ''
            st.rerun()

if __name__ == "__main__":
    main()