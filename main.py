import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

import account_manage
service_list = []

#TODO add multiple gmail accounts so can search trhough multiple at the same time


    # with open("token_edvards.pickle", "rb") as token:
    #     creds_edv = pickle.load(token)
    # with open("tokenvinsisr@gmail.com.pickle", 'rb') as token:
    #     creds_vins = pickle.load(token)
    # return [build('gmail', 'v1', credentials=creds_edv),
    #         build('gmail', 'v1', credentials=creds_vins)]

# get the Gmail API service
email_to_add = input("enter gmail(or 'all'): ")
if email_to_add == 'all':
    for file in os.listdir("C:\\Users\eerne\PycharmProjects\gmail_manager\\tokens"):
        if file.endswith(".pickle"):
            with open(f"C:\\Users\eerne\PycharmProjects\gmail_manager\\tokens\\{file}", "rb") as token:
                service_list.append(account_manage.create_creds(token))
else:
    service_list.append(account_manage.gmail_authenticate(email_to_add))
print(service_list)
#gmail_authenticate()

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def read_message(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()

    payload = msg['payload']
    headers = payload.get("headers")
    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                print("From:", value)
            if name.lower() == "to":
                print("To:", value)
            if name.lower() == "date":
                print("Date:", value)
    print("-"*50) #visual thingy lai istas nicer ;)

search_word = input("what to search:")

for service in service_list:
    results = search_messages(service, search_word)
    print(f"Found {len(results)} emails")
    for email in results:
        read_message(service, email)


