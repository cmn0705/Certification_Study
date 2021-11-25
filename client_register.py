from flask import request, render_template,redirect,session
import datetime,boto3,binascii
from hashlib import sha512
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def client_register():
    if request.method == 'POST':
        
        if 'client' not in [table.name for table in db.tables.all()]:
            db.create_table(
                TableName='client',
                KeySchema=[
                    {'AttributeName': 'email',   'KeyType': 'HASH'},
                ],
                
                AttributeDefinitions=[
                    {'AttributeName': 'email', 'AttributeType': 'S'},
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )

        try:
            client=db.Table('client').get_item(Key={'email': request.form['email']})['Item']
            return "An account with this email already exists."
        except:
            db.Table('client').put_item(
                Item={
                'client_id':binascii.crc32(request.form['email'].encode()) & 0xffffffff,
                'email':request.form['email'],
                'password':sha512(request.form['password1'].encode()).hexdigest(),
                'first_name':request.form['first_name'],
                'middle_name':request.form['middle_name'],
                'last_name':request.form['last_name'],
                'phone':request.form['phone'],
                'gender':request.form['gender'],
                'birthday':request.form['birthday'],
                'mailing_address':request.form['mailing_address'],
                'apt_ste_bldg':request.form['apt_ste_bldg'],
                'city':request.form['city'],
                'state':request.form['state'],
                'zip_code':request.form['zip_code'],
                'country':request.form['country'],
                'signup_date':str(datetime.datetime.utcnow()),
                'certification':request.form['certification'],
                }
            )
            session['email']=request.form['email']
            session['subject']='client'
            return redirect('/client_page')
    return render_template('client_register.html')