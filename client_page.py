from flask import render_template, session
from flask_session import Session
import boto3,oncehub
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def client_page():
    client=db.Table('client').get_item(Key={'email': session['email']})['Item']
    bookings=oncehub.client_bookings(client['email'])
    return render_template('client_page.html', 
                            name=client['first_name'], 
                            email=client['email'],
                            focus=client['certification'],
                            bookings=bookings)