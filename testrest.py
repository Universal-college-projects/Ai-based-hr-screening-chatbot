import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email_rest():
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("SENDGRID_FROM_EMAIL") or os.getenv("SMTP_EMAIL")
    to_email = "lalithasujala@gmail.com" # Hardcoded for test, or change as needed

    if not api_key:
        print("Error: SENDGRID_API_KEY not found in .env")
        return

    url = "https://api.sendgrid.com/v3/mail/send"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "personalizations": [
            {
                "to": [{"email": to_email}]
            }
        ],
        "from": {"email": from_email},
        "subject": "Test Email via REST API",
        "content": [
            {
                "type": "text/plain",
                "value": "This is a test email sent using Python requests (Direct REST API)."
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code in [200, 201, 202]:
            print("Email sent successfully!")
        else:
            print("Failed to send email.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_email_rest()
