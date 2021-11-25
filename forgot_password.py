from flask import render_template,request
import boto3
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service
def forgot_password():
    if request.method=="POST":
        if request.form['subject']=='client':
            try:
                client=db.Table('client').get_item(Key={'email': request.form['email']})['Item']
            except: return "There is no account using "+ request.form['email']
            return "Link to reset password had sent to "+request.form['email'] + " /reset_password/client/"+ client['email']+"/"+str(client['client_id'])
        if request.form['subject']=='coach':
            try:
                coach=db.Table('coach').get_item(Key={'email': request.form['email']})['Item']
            except: return "There is no account using "+ request.form['email']
            return "Link to reset password had sent to "+request.form['email'] + " /reset_password/coach/"+ coach['email']+"/"+str(coach['coach_id'])
        return "We had sent you an email to reset your password"       
    return render_template('forgot_password.html')