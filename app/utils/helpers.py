import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import streamlit as st

def send_email(to_email, subject, body):
    # 1. Try SendGrid First
    sendgrid_key = "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"
    sendgrid_from = "lalithasujala@gmail.com"

    if sendgrid_key and sendgrid_from:
        try:
            message = Mail(
                from_email=sendgrid_from,
                to_emails=to_email,
                subject=subject,
                plain_text_content=body)
            sg = SendGridAPIClient(sendgrid_key)
            response = sg.send(message)
            print(f"SendGrid Status: {response.status_code}")
            print(f"SendGrid Body: {response.body}")
            print(f"SendGrid Headers: {response.headers}")
            
            if response.status_code in [200, 201, 202]:
                return True, "Email sent successfully via SendGrid."
            else:
                 error = f"SendGrid Error: {response.status_code} -Body: {response.body}"
                 print(error)
                 return False, error
        except Exception as e:
            error = f"SendGrid Exception: {str(e)}"
            print(error)
            return False, error
            
    # # 2. Fallback to Standard SMTP (Works locally, blocked on Railway Free)
    # smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    # smtp_port = int(os.getenv("SMTP_PORT", 587))
    # smtp_password = os.getenv("SMTP_PASSWORD")
    # smtp_user = os.getenv("SMTP_EMAIL")

    # if not smtp_user or not smtp_password:
    #     msg = f"MOCK EMAIL TO {to_email}: {body}"
    #     print(msg)
    #     return False, "SMTP Credentials missing (Check .env). Mock email printed to console."

    # try:
    #     msg = MIMEMultipart()
    #     msg['From'] = smtp_user
    #     msg['To'] = to_email
    #     msg['Subject'] = subject
    #     msg.attach(MIMEText(body, 'plain'))

    #     server = smtplib.SMTP(smtp_server, smtp_port)
    #     server.starttls()
    #     server.login(smtp_user, smtp_password)
    #     server.sendmail(smtp_user, to_email, msg.as_string())
    #     server.quit()
    #     return True, "Email sent successfully via SMTP."
    # except Exception as e:
    #     error_msg = f"Failed to send email: {e}"
    #     print(error_msg)
    # If we reach here, everything failed
    return False, "Failed to send email (SendGrid failed and SMTP is disabled)."

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
