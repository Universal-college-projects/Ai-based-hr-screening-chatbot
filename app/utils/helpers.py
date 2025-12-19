import os
import streamlit as st
import requests
import json

def send_email(to_email, subject, body):
    # 1. Try SendGrid REST API (Proven working)
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    sendgrid_from = os.getenv("SENDGRID_FROM_EMAIL") or os.getenv("SMTP_EMAIL")

    if sendgrid_key and sendgrid_from:
        url = "https://api.sendgrid.com/v3/mail/send"
        
        headers = {
            "Authorization": f"Bearer {sendgrid_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "personalizations": [
                {
                    "to": [{"email": to_email}]
                }
            ],
            "from": {"email": sendgrid_from},
            "subject": subject,
            "content": [
                {
                    "type": "text/plain",
                    "value": body
                }
            ]
        }
        
        try:
            # Using verify=True by default which is safe.
            response = requests.post(url, headers=headers, data=json.dumps(data))
            
            if response.status_code in [200, 201, 202]:
                print(f"Email sent successfully via REST to {to_email}")
                return True, "Email sent successfully."
            else:
                 error = f"SendGrid Error: {response.status_code} - Body: {response.text}"
                 print(error)
                 return False, error
                 
        except Exception as e:
            error = f"SendGrid Exception: {str(e)}"
            print(error)
            return False, error
            
    return False, "SendGrid API Key or From Email is missing in .env"

def logout_button():
    # Top right Logout button using columns
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.role = None
            st.session_state.user_id = None
            st.session_state.wizard_step = 1
            st.switch_page("Home.py")

def get_job_options(db_conn):
    # Retrieve jobs from snowflake to populate dropdown
    # Returns list of tuples (id, title)
    if db_conn:
        query = "SELECT JOB_ID, TITLE FROM JOBS"
        df = db_conn.fetch_data(query)
        if not df.empty:
            return list(zip(df['JOB_ID'], df['TITLE']))
    
    # Fallback for demo
    return [("DEMO_001", "Software Engineer (Demo)")]

def hide_sidebar():
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)
