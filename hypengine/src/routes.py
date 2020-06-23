from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from sqlalchemy.dialects import mysql
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from flask import Flask, jsonify, request, make_response, render_template
from functools import wraps
# from src.models import db, LeaderBoardTable
import ezsheets as ezs
from flask import current_app as app
# from views import home_template



def point_getter(field):
    sampler = 1
    int_points = []
    for i in field:
        if len(i) < 1:
            continue
        int_points.append(float(i))
    #     if type(float(i)) == type(float(sampler)):
    #         print("...",i)
    #         continue
    #     else:
    #         print("====>",i)
    #         int_points.append(float(i))
    return int_points


def email_getter(field):
    email_lst = []
    no_email_count_ = 0
    for mail_addr in field:
        if len(mail_addr) <= 1:
            email_lst.append("[Email Not Provided]")
            no_email_count_ +=1
        else:
            email_lst.append(mail_addr)
    return email_lst, no_email_count_

def name_getter(field):
    name_lst = []
    no_name_count_ = 0
    for name in field:
        if len(name) <= 1:
            name_lst.append("[Name Not Provided]")
            no_name_count_ +=1
        else:
            name_lst.append(name)
    return name_lst, no_name_count_


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

#ID and range of a sample spreadsheet respectively.
SAMPLE_SPREADSHEET_ID = '1eoH7SiYnJKHvxMaubHRCGXtGoJY-oY9XUbxSTTbp7FY'
SAMPLE_RANGE_NAME = 'E:H4'

@app.route('/')
def index():
    full_name = []
    user_name = []
    email = []
    points = []
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    # print("values: ", values)

    if not values:
        return 'No data found.'
    else:
        for row in values:
            full_name.append(row[0])
            user_name.append(row[1])
            email.append(row[2])
            # email_ = ["[Email Not Provided]" if len(mail_addr) <= 1 else mail_addr for mail_addr in email]
            email_= email_getter(email)
            points.append(row[3])
            int_points = point_getter(points)
            id_ = [x+1 for x in range(len(int_points))]
            highest_three = sorted(zip(int_points, full_name), reverse=True)[:3]


        board_data = zip(id_, full_name, user_name, email_[0], int_points)
        return render_template('home.html', board_data=board_data, no_email_count=email_[1], highest_three=highest_three)
    
    return render_template('home_template.html')



