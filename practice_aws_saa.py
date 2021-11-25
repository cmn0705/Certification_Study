from flask import render_template,request,session
import boto3,random
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def practice_aws_saa():
    if session.get('answered_total')==None: session['answered_total']=0
    if session.get('answered_correct')==None: session['answered_correct']=0
    if session.get('num_aws_saa')==None: session['num_aws_saa']=''
    if session.get('question')==None: session['question']=''
    if session.get('answer')==None: session['answer']=''
    if session.get('explain')==None: session['explain']=''
    notice=''
    explain=''
               
    if request.method=='GET':
        list_id=db.Table('aws_saa_questions').scan(ProjectionExpression="id")['Items']
        random_id=random.choice(list_id)['id']
        random_question=db.Table('aws_saa_questions').get_item(Key={'id': random_id})['Item']
        session['question']=random_question['question']
        session['answer']=random_question['answer']
        try: session['explain']=random_question['explain'] 
        except: session['explain']=''
        session['num_aws_saa']=len(list_id)
        notice,explain='',''
        return render_template('practice_aws_saa.html', notice=notice, explain=explain)
        
    if request.method=='POST':   
        if set(request.form['answer'].lower().replace(' ','').split(','))==set(session['answer'].lower().replace(' ','').split(',')):
            notice='CORRECT! The answer is '+session['answer']
            session['answered_correct']+=1
        else: notice="WRONG! The correct answer is: "+session['answer']
        session['answered_total']+=1
        explain=session['explain']
        return render_template('practice_aws_saa.html', notice=notice, explain=explain)
    
    else: return render_template('practice_aws_saa.html', notice=notice, explain=explain)