from flask import request, render_template
import boto3
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def reset_password(subject,email,id):
    if request.method=="POST":
        if subject=='client':
            client=db.Table('client').get_item(Key={'email': email})['Item']
            if str(client['client_id'])==id:
                db.Table('client').update_item(
                    Key={'email': email},
                    UpdateExpression="set password=:p",
                    ExpressionAttributeValues={':p': request.form['password1']},
                )
                return "Successfully changed password."
        if subject=='coach':
            coach=db.Table('coach').get_item(Key={'email': email})['Item']
            if str(coach['coach_id'])==id:
                db.Table('coach').update_item(
                    Key={'email': email},
                    UpdateExpression="set password=:p",
                    ExpressionAttributeValues={':p': request.form['password1']},
                )
                return "Successfully changed password."
    return render_template('reset_password.html',subject=subject, email=email,id=id)