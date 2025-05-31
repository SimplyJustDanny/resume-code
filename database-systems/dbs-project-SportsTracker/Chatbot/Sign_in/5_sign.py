import requests
import streamlit as st 
import pandas as pd
from dao.users import UserDAO
# import streamlit_authenticator as stauth
import datetime
import re

dao = UserDAO()

def sign_up_ui():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':red[Sign Up]')
        email = st.text_input('Email', placeholder='Enter your email')
        username = st.text_input('Username', placeholder='Enter your username')
        password1 = st.text_input('Password', placeholder='Enter your password', type='password')
        password2 = st.text_input('Confirm Password', placeholder='Confrim your password', type='password')

        date_joined = str(datetime.datetime.now())

     
        if email:
            verified, err_string = sign_in_verfication(email, username, password1, password2)
            if verified:
                dao.insertUser(email, username, password1, date_joined)
                # state loged in should be here, after the user is inserted in the db
                created = 1
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.warning(err_string)

        st.form_submit_button('Sign up')


def log_in_ui():
    with st.form(key='Log in', clear_on_submit=True):
        st.subheader(':red[Log in]')
        email = st.text_input('Email', placeholder='Enter your email')
        username = st.text_input('Username', placeholder='Enter your username')
        password = st.text_input('Password', placeholder='Enter your password', type='password')


        if email:
            verified, err_string = log_in_verfication(email, username, password)
            if not verified:
                st.warning(err_string)
            else:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
                
   
        st.form_submit_button('Log in')

           
            
        

def sign_in_verfication(email, username, password1, password2):
    """
    Check validity of sign-in credentials
    :param email:
    :param username:
    :param password1:
    :param password2:
    :return True if credentials are valid else False:
    """
    if not validate_email(email):
        return (False, 'Invalid Email - Does not appear to be a handle at a domain')
    if query_email(email):
        return (False, 'Invalid Email - An account with that email already exists')
    if not validate_username(username):
        return (False, 'Invalid Username - Only alphanumeric characters are allowed')
    if len(username) < 2:
        return (False, 'Invalid Username - Name must be at least two characters long')
    if query_username(username):
        return (False, 'Invalid Username - An account with that name already exists')
    if len(password1) < 6:
        return (False, 'Invalid Password - Password must be at least six characters long')
    if password1 != password2:
        return (False, 'Invalid Confirmation - Confirmation does not match password')
    return (True, 'Account successfully created')

def log_in_verfication(email, username, password):
    """
    Check validity of log-in credentials
    :param email:
    :param username:
    :param password1:
    :param password2:
    :return True if credentials are valid else False:
    """
    if not validate_email(email):
        return (False, 'Invalid Email - Does not appear to be a handle at a domain')
    if not query_email(email):
        return (False, 'Invalid Email - No account exists with that email')
    if not validate_username(username):
        return (False, 'Invalid Username - Only alphanumeric characters are allowed')
    if len(username) < 2:
        return (False, 'Invalid Username - Name must be at least two characters long')
    if not query_username(username):
        return (False, 'Invalid Username - No account exists with that username')
    if len(password) < 6:
        return (False, 'Invalid Password - Password must be at least six characters long')
    return query_password(email, username, password)

def validate_email(email):
    """
    Check validity of email
    :param email:
    :return True if email is valid else False:
    """
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    if re.match(pattern, email):
        return True
    return False

def query_email(email):
    """
    Check presence of email in database
    :param email:
    :return True if email is in database else False:
    """
    dao = UserDAO()
    # TODO: Replace this with a handler
    email_exists = dao.emailInDB(email)
    return email_exists

def validate_username(username):
    """
    Check validity of username
    :param username:
    :return True if username is valid
    """
    pattern = "^[a-zA-Z0-9]*$"

    if re.match(pattern, username):
        return True
    return False

def query_username(username):
    """
    Check presence of username in database
    :param username:
    :return True if username is in database else False:
    """
    dao = UserDAO()
    # TODO: Replace this with a handler
    name_exists = dao.nameInDB(username)
    return name_exists

def query_password(email, username, password):
    """
    Check if password matches universe
    :param email:
    :param username:
    :param password:
    :return True if password and username matches email account else False:
    """
    # TODO: Replace this with a handler
    dao = UserDAO()
    user_data = dao.getUserByEmail(email)
    if user_data[2] != username:
        return (False, 'Wrong Username - Username is not linked to that email')
    if user_data[3] != password:
        return (False, 'Wrong Password - Password is not linked to that email')
    return (True, 'Account successfully logged in')

# page ui
option = st.selectbox("Sign up / Log in", ("Sign up", "Log in"))

if option == "Sign up":
    sign_up_ui()
else:
    log_in_ui()

base_url = "https://group-abcd-6cd3d84eb4d5.herokuapp.com"



