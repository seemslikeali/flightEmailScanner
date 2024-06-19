from dotenv import load_dotenv
import os
from exchangelib import DELEGATE, Account, Credentials
import re
import requests
import time

# Load environment variables from .env file
load_dotenv()

# Function to connect to Outlook account
def connect_to_outlook():
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    creds = Credentials(email, password)
    account = Account(email, credentials=creds, autodiscover=True, access_type=DELEGATE)
    return account

# Function to get emails from a specific folder
def get_emails(account, folder_name='inbox'):
    folder = getattr(account, folder_name)
    return folder.all()

# Function to search emails based on various criteria
def search_emails(emails, search_string=None, search_range=None, notified_subjects=None):
    matched_emails = []
    for email in emails:
        subject = email.subject
        
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

account = connect_to_outlook()

search_string = "800$"
search_range = (0, 1200)

notified_subjects = load_notified_subjects(matches_filename)

print("Script is running...")

while True:
    try:
        emails = get_emails(account)
        matched_emails = search_emails(emails, search_string, search_range, notified_subjects)
        
        new_matches = [email for email in matched_emails if email.subject not in notified_subjects]
        
        if new_matches:
            print(f"Found {len(new_matches)} new matched email(s).")
            for email in new_matches:
                content = f"Matched Email: {email.subject}"
                send_discord_notification(content)
                notified_subjects.append(email.subject)
        else:
            print("No new matches found.")
        
        save_notified_subjects(matches_filename, notified_subjects)
        
        time.sleep(10)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(10)
