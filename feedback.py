from flask import render_template,request,redirect,session
import boto3,datetime, random
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def feedback():
    if request.method == 'POST':
        
        if 'feedback' not in [table.name for table in db.tables.all()]:
            db.create_table(
                TableName='feedback',
                KeySchema=[
                    {'AttributeName': 'id',   'KeyType': 'HASH'},
                ],
                
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'N'},
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
        db.Table('feedback').put_item(
            Item={
            'id':random.randint(10000,99999),
            'email':request.form['email'],
            'tittle':request.form['tittle'],
            'feedback':request.form['feedback'],
            'time': str(datetime.datetime.utcnow()),
            }
        )
        return "Thank you for your feedback."

    return render_template('feedback.html')