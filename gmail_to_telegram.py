from __future__ import print_function
import pickle
import json
import requests
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

dir_path = os.path.dirname(os.path.realpath(__file__))

######### Telegram ###############################
TOKEN = "0123456789:aBcDeEsflkjslkjLKJSFSF"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

#text, chat = get_last_chat_id_and_text(get_updates())
#send_message("Yeho-ho", "-1001351834980")


########## Google Gmail API ###################
# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    tknpickle = dir_path + '/token.pickle'
    clientsecret = dir_path + '/client_secret_0123456789-asKLkjhKF:LkjLKj8d.apps.googleusercontent.com.json'
    if os.path.exists(tknpickle):
        with open(tknpickle, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                clientsecret, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tknpickle, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
#    results = service.users().labels().list(userId='me').execute()
    results = service.users().messages().list(userId='me', labelIds = ['UNREAD']).execute()
    messages = results.get('messages', [])

    if not messages:
        #print("No messages found.")
        exit()
    else:
        print(str(datetime.datetime.now()) + " - New alert:")
        for message in messages:
            msg = service.users().messages().get(userId='me', format='full', id=message['id']).execute()
            body = msg['snippet']
            headers = msg['payload']['headers']
            subject= [json.dumps(i['value']) for i in headers if i["name"]=="Subject"]
            #print(subject)
            #print(body)
            alert = str(subject) + "\n" + body
            print(alert)
            send_message(alert, "-98798724987")
            service.users().messages().trash(userId='me', id=message['id']).execute()
        	
if __name__ == '__main__':
    main()
