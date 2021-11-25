from flask import request, render_template,session,redirect
import datetime,boto3,binascii
import shar256 #check shar256.py
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def coach_register():
    if request.method == 'POST':

        if 'coach' not in [table.name for table in db.tables.all()]:
            db.create_table(
                TableName='coach',
                KeySchema=[
                    {'AttributeName': 'email',   'KeyType': 'HASH'},
                ],
                
                AttributeDefinitions=[
                    {'AttributeName': 'email', 'AttributeType': 'S'},
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )

        try:
            coach=db.Table('coach').get_item(Key={'email': request.form['email']})['Item']
            return "An account with this email already exists."
        except:
            db.Table('coach').put_item(
                Item={
                'coach_id':binascii.crc32(request.form['email'].encode()) & 0xffffffff,
                'email':request.form['email'],
                'password':shar256.shar256(request.form['password1']),
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
                'aws_cp':request.form.get('aws_cp'),
                'aws_saa':request.form.get('aws_saa'),
                }
            )
            session['email']=request.form['email']
            session['subject']='coach'
            return redirect('/coach_page')
    return render_template('coach_register.html')