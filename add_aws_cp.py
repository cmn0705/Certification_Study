from flask import render_template,request,redirect,session
import boto3,datetime
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def add_aws_cp():
    if request.method == 'POST':
        
        if 'aws_cp_questions' not in [table.name for table in db.tables.all()]:
            db.create_table(
                TableName='aws_cp_questions',
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
            question=db.Table('aws_cp_questions').get_item(Key={'id': id})['Item']
            return "Similar question exists in our database:" + question['question']
        except:
            db.Table('aws_cp_questions').put_item(
                Item={
                'id':id,
                'question':request.form['question'].strip(),
                'answer':request.form['answer'].replace(" ", ""),
                'contributor':session['email'] if session['email'] else "guest",
                'time_added':str(datetime.datetime.utcnow()),
                'explain':request.form['explain']
                }
            )
            return redirect('/add_aws_cp')

    return render_template('add_aws_cp.html')