import os
import base64
import smtplib
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
import google.oauth2.credentials
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv
import imaplib
import email
# Load environment variables from .env file
load_dotenv()

# Load email credentials from environment variables
email_address = os.getenv('EMAIL')


# Load Google OAuth credentials from environment variables


# Path to the token JSON file
token_path = 'token.json'

# Scopes required for sending email
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

def get_credentials():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(token_path, scopes=SCOPES)


    # Required, indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = 'http://127.0.0.1:5000/log_in'

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Recommended, enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',)

def send_email(subject, body, to):
    creds = get_credentials()
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {'raw': raw}

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = (service.users().messages().send(userId='me', body=message).execute())
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def read_emails_via_api():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    if not messages:
        print("No new messages.")
    else:
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            print(f"From: {sender}")
            print(f"Subject: {subject}")
            # 

            if any(specific_sender in sender for specific_sender in specific_senders):
                print(f"From: {sender}")
                print(f"Subject: {subject}")
                email_body = get_email_body(msg_data)
                print(f"Body: {email_body}")
                process_email_response(email_body)


def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()

def process_email_response(body):
    # PROCESSAR MAIL DATA, SPLITTA OCH LÄGG I DICT, BEHÖVER JOBBAS PÅ
    lines = body.split('\n')
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip().lower()] = value.strip()
    print(f"Processed data: {data}")
   

# Example usage
if __name__ == "__main__":
    subject = 'MOOD TRACKER: Automatiskt meddelande'
    message = 'Detta är ett automatiserat meddelande. Svara med:\nmood: \nsleep: \nappetite: '
    recipient = 'l.com'
    
    specific_senders = ['.com', os.getenv('EMAIL')] 
    
    send_email(subject, message, recipient) #SKICKAR OCH LÄSER
    read_emails_via_api()  
    