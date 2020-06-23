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
    for i in field[1:]:
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
    for mail_addr in field[1:]:
        if len(mail_addr) <= 1:
            email_lst.append("[Email Not Provided]")
            no_email_count_ +=1
        else:
            email_lst.append(mail_addr)
    return email_lst, no_email_count_


@app.route('/')
def index():
    ss = ezs.Spreadsheet('1eoH7SiYnJKHvxMaubHRCGXtGoJY-oY9XUbxSTTbp7FY')
    hng_sheet = ss[0]
    if hng_sheet:
        try:
            full_name = hng_sheet.getColumn(1)
            user_name = hng_sheet.getColumn(2)
            email = hng_sheet.getColumn(3)
            # email_ = ["[Email Not Provided]" if len(mail_addr) <= 1 else mail_addr for mail_addr in email]
            email_= email_getter(email)
            points = hng_sheet.getColumn(4)
            int_points = point_getter(points)
            id_ = [x+1 for x in range(len(int_points))]
            highest_three = sorted(zip(int_points, full_name[1:]), reverse=True)[:3]
        except Exception as e:
            return str(e)
        else:
            board_data = zip(id_, full_name[1:], user_name[1:], email_[0], int_points)
            return render_template('home.html', board_data=board_data, no_email_count=email_[1], highest_three=highest_three)
    
    return render_template('home_template.html')



