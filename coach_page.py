from flask import render_template, session
from flask_session import Session
import boto3,oncehub
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def coach_page():
    coach=db.Table('coach').get_item(Key={'email': session['email']})['Item']
    bookings=oncehub.coach_bookings(coach['email'])
    return render_template('coach_page.html', 
                            name=coach['first_name'], 
                            email=coach['email'],
                            bookings=bookings)