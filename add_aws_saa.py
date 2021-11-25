from flask import render_template,request,redirect,session
import boto3,datetime
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def add_aws_saa():
    if request.method == 'POST':
        
        if 'aws_saa_questions' not in [table.name for table in db.tables.all()]:
            db.create_table(
                TableName='aws_saa_questions',
                KeySchema=[
                    {'AttributeName': 'id',   'KeyType': 'HASH'},
                ],
                
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
        from lsh import generateID #my function for LSH
        id=generateID(request.form['question'])
        try:
            question=db.Table('aws_saa_questions').get_item(Key={'id': id})['Item']
            return "Similar question exists in our database:/n" + question['question']
        except:
            db.Table('aws_saa_questions').put_item(
                Item={
                'id':id,
                'question':request.form['question'].strip(),
                'answer':request.form['answer'].replace(" ", ""),
                'contributor':session['email'] if session['email'] else "guest",
                'time_added':str(datetime.datetime.utcnow()),
                'explain':request.form['explain']
                }
            )
            return redirect('/add_aws_saa')

    return render_template('add_aws_saa.html')