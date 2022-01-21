from flask import render_template,request, redirect,url_for
import boto3
from boto3.dynamodb.conditions import Attr
db = boto3.resource('dynamodb',region_name='us-east-1') # Real AWS service

def scan():
    items=None
    count=None 
    
    if request.method=='POST':
        table=db.Table(request.form['table'])
        attribute=request.form['attribute']
        
        operations={
            "begins_with":  lambda value : table.scan(FilterExpression=Attr(attribute).begins_with(value)),
            "eq":           lambda value : table.scan(FilterExpression=Attr(attribute).eq(value)),
            "gt":           lambda value : table.scan(FilterExpression=Attr(attribute).gt(value)),
            "gte":          lambda value : table.scan(FilterExpression=Attr(attribute).gte(value)),
            "lt":           lambda value : table.scan(FilterExpression=Attr(attribute).lt(value)),
            "lte":          lambda value : table.scan(FilterExpression=Attr(attribute).lte(value)),
            "contains":     lambda value : table.scan(FilterExpression=Attr(attribute).contains(value)),
            "ne":           lambda value : table.scan(FilterExpression=Attr(attribute).ne(value)),
        } # Leave value as variable here so it do not scan yet

        operationsc={
            "begins_with":  lambda value : table.scan(FilterExpression=Attr(attribute).begins_with(value), ExclusiveStartKey=response['LastEvaluatedKey']),
            "eq":           lambda value : table.scan(FilterExpression=Attr(attribute).eq(value), ExclusiveStartKey=response['LastEvaluatedKey']),
            "gt":           lambda value : table.scan(FilterExpression=Attr(attribute).gt(value), ExclusiveStartKey=response['LastEvaluatedKey']),
            "gte":          lambda value : table.scan(FilterExpression=Attr(attribute).gte(value), ExclusiveStartKey=response['LastEvaluatedKey']),
            "lt":           lambda value : table.scan(FilterExpression=Attr(attribute).lt(value), ExclusiveStartKey=response['LastEvaluatedKey']),
            "lte":          lambda value : table.scan(FilterExpression=Attr(attribute).lte(value), ExclusiveStartKey=response['LastEvaluatedKey']),
            "contains":     lambda value : table.scan(FilterExpression=Attr(attribute).contains(value), ExclusiveStartKey=response['LastEvaluatedKey']),
            "ne":           lambda value : table.scan(FilterExpression=Attr(attribute).ne(value), ExclusiveStartKey=response['LastEvaluatedKey']),
        }
        
        items = []
        response = operations[request.form['operation']](request.form['value'])
        items.extend(response['Items'])

        # bypass the 1M scan limit - pagination, this is not necessary for small table
        while 'LastEvaluatedKey' in response: 
            response = operationsc[request.form['operation']](request.form['value'])
            items.extend(response['Items'])
        # bypass end

        count=len(items)

    return render_template('scan.html', items=items, count=count)

def delete():
    if request.method=='POST':
        table=db.Table(request.form['table'])
        table.delete_item(Key={'id': request.form['id']})
    return redirect(url_for('scan'))