import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

all_emails = False
creds_list = []

#TODO: create script that creates new token for gmail account


SCOPES = ['https://mail.google.com/']


def create_creds(token):
    creds = pickle.load(token)
    return build("gmail", "v1", credentials = creds)

def gmail_authenticate(email_to_add):


    creds = None
    #the file token.pickle stores the user's access and refresh tokens, and is
    #created automatically when the authorization flow completes for the first time

    if os.path.exists(f"tokens\\token{email_to_add}.pickle"):
        print("email already added")
        with open(f"tokens\\token{email_to_add}.pickle", "rb") as token:
            creds = pickle.load(token)
    #if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("token refresh")
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print("adding new gmail")
        # save the credentials for the next run
        with open(f"tokens\\token{email_to_add}.pickle", "wb") as token:
            pickle.dump(creds, token)



    # with open("token_edvards.pickle", "rb") as token:
    #     creds_edv = pickle.load(token)
    # with open("tokenvinsisr@gmail.com.pickle", 'rb') as token:
    #     creds_vins = pickle.load(token)
    #build('gmail', 'v1', credentials=creds_vins)]




    return build('gmail', 'v1', credentials=creds)
#
# if all_emails == True:
#     for file in os.listdir("C:\\Users\eerne\PycharmProjects\gmail_manager\\tokens"):
#         if file.endswith(".pickle"):
#             with open(f"C:\\Users\eerne\PycharmProjects\gmail_manager\\tokens\\{file}", "rb") as token:
#                 creds_list.append(pickle.load(token))
#     for creds in creds_list:
#         gmail_authenticate(creds)




