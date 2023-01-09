from __future__ import print_function
from flask import Flask, request, redirect
from google.oauth2.credentials import Credentials
import google.auth.transport.requests
import requests



import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.message import EmailMessage

import google.auth

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
flow = Flow.from_client_secrets_file(
      'credential1.json', SCOPES,redirect_uri='http://34.93.119.62.nip.io:8000/callback')

@app.route('/')
def cool():
    return("HI")

@app.route('/authorize')
def authorize():
   
   auth_url, _ = flow.authorization_url(access_type='offline')
   return redirect(auth_url)


@app.route('/callback')
def callback():

  creds = None
  if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          code = request.args.get('code')
          flow.fetch_token(code=code)
          creds = flow.credentials

  with open('token.json', 'w') as token:
            token.write(creds.to_json())

  return("Success")

if __name__ == '__main__':
  app.run(debug=True, port=8000)




