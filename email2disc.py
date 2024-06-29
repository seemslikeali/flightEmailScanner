from dotenv import load_dotenv
import os
from exchangelib import DELEGATE, Account, Credentials
import re
import requests
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Load environment variables from .env file
load_dotenv()

# Function to connect to Outlook account
def connect_to_outlook():
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    creds = Credentials(email, password)
    account = Account(email, credentials=creds, autodiscover=True, access_type=DELEGATE)
    return account

# Function to get emails from a specific folder in Outlook
def get_outlook_emails(account, folder_name='inbox'):
    folder = getattr(account, folder_name)
    return list(folder.all())  # Convert QuerySet to list

# Function to connect to Gmail account
def connect_to_gmail():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

# Function to get emails from Gmail
def get_gmail_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        subject = ''
        for header in msg['payload']['headers']:
            if header['name'] == 'Subject':
                subject = header['value']
        emails.append({'id': msg['id'], 'subject': subject})
    return emails

# Function to search emails based on various criteria
def search_emails(emails, search_string=None, search_range=None, notified_subjects=None):
    matched_emails = []
    for email in emails:
        subject = email.subject if hasattr(email, 'subject') else email['subject']
        
        # Check if subject has already been notified
        if subject in notified_subjects:
            continue
        
        # Match based on search_string
        if search_string and search_string in subject:
            matched_emails.append(email)
        
        # Match based on search_range
        elif search_range:
            range_pattern = rf"\b(?:\d{{1,3}},{{0,1}}\d{{1,3}}|\d{{1,3}})\b"
            for match in re.finditer(range_pattern, subject):
                price = int(match.group().replace(',', ''))
                if search_range[0] <= price <= search_range[1]:
                    matched_emails.append(email)
                    break
        
        # Match based on notified_subjects
        elif notified_subjects:
            if subject not in notified_subjects:
                matched_emails.append(email)
    
    return matched_emails

# Function to send notification to Discord webhook
def send_discord_notification(content):
    webhook_url = os.getenv('WEBHOOK_URL')
    data = {
        "content": content
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")

# Function to load notified subjects from a file
def load_notified_subjects(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            notified_subjects = file.read().splitlines()
    except FileNotFoundError:
        notified_subjects = []
    return notified_subjects

# Function to save notified subjects to a file
def save_notified_subjects(filename, notified_subjects):
    with open(filename, 'w', encoding='utf-8') as file:
        for subject in notified_subjects:
            file.write(subject + '\n')

# Replace these with your actual credentials and webhook URL
matches_filename = "matches.txt"

# Connect to both Outlook and Gmail
outlook_account = connect_to_outlook()
gmail_service = connect_to_gmail()

search_string = "800$"
search_range = (0, 1200)

notified_subjects = load_notified_subjects(matches_filename)

print("Script is running...")

while True:
    try:
        outlook_emails = get_outlook_emails(outlook_account)
        gmail_emails = get_gmail_emails(gmail_service)
        
        all_emails = outlook_emails + gmail_emails
        matched_emails = search_emails(all_emails, search_string, search_range, notified_subjects)
        
        new_matches = [email for email in matched_emails if (email['subject'] if isinstance(email, dict) else email.subject) not in notified_subjects]
        
        if new_matches:
            print(f"Found {len(new_matches)} new matched email(s).")
            for email in new_matches:
                content = f"Matched Email: {email['subject'] if isinstance(email, dict) else email.subject}"
                send_discord_notification(content)
                notified_subjects.append(email['subject'] if isinstance(email, dict) else email.subject)
        else:
            print("No new matches found.")
        
        save_notified_subjects(matches_filename, notified_subjects)
        
        time.sleep(1000)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(10)
