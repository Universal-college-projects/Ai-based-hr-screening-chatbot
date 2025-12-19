import requests
import json

def send_email_rest():
    # Use the new key provided by user
    api_key = "SG.8E_RVwWsSJSCd9Oyrk9rxg.ILTjnpJ_6EFFL6VFWdICnco1CECc1D9kxxHC6EF-BJg"
    from_email = "lalithasujala@gmail.com"
    to_email = "vivekmarapaka33.1@gmail.com" # Sending to self for testing

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
        "subject": "Test Email via REST API (New Key)",
        "content": [
            {
                "type": "text/plain",
                "value": "This is a test email sent using Python requests (Direct REST API) with the new key."
            }
        ]
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code in [200, 201, 202]:
            print("SUCCESS: Email sent successfully!")
        else:
            print("FAILURE: Failed to send email.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_email_rest()
