from flask import render_template, request, redirect,url_for, session
from flask_session import Session
import boto3
from hashlib import sha512
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def login():
    if request.method=="POST":
        if request.form['subject']=='client':
            try:
                client=db.Table('client').get_item(Key={'email': request.form['email']})['Item']
            except: return "There is no account using "+ request.form['email']
            if sha512(client['password'].encode()).hexdigest()==sha512(request.form['password'].encode()).hexdigest():
                session["email"] = request.form['email']
                session["subject"] = 'client'
                return redirect(url_for('client_page'))
            else: return "Wrong password!"
        
        if request.form['subject']=='coach':
            try:
                coach=db.Table('coach').get_item(Key={'email': request.form['email']})['Item']
            except: return "There is no account using "+ request.form['email']
            if sha512(coach['password'].encode()).hexdigest()==sha512(request.form['password'].encode()).hexdigest():
                session["email"] = request.form['email']
                session["subject"] = 'coach'
                return redirect(url_for('coach_page'))
            else: return "Wrong password!"
    return render_template('login.html')