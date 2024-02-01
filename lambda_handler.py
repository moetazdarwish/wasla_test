import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB 
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
dynamodb_table = dynamodb.Table('WASLA_Table')

allList_path = '/list'
product_path = '/product'

def lambda_handler(event, context):
    print('Request event: ', event)
    print(event.get('httpMethod'))
    response = None
   
    try:
        http_method = event.get('httpMethod')
        path = event.get('path')

        if http_method == 'GET' and path == product_path:
            prod_id = event['queryStringParameters']['id']
            response = get_product(prod_id)
        elif http_method == 'GET' and path == allList_path:
            response = get_ProductList()
        elif http_method == 'POST' and path == product_path:
            response = add_product(json.loads(event['body']))
        elif http_method == 'PUT' and path == product_path:
            body = json.loads(event['body'])
            response = update_product(body['id'], body['Key'], body['Value'])
        elif http_method == 'DELETE' and path == product_path:
            body = json.loads(event['body'])
            response = delete_product(body['id'])
        else:
            response = build_response(404, '404 Not Found Or Wrong method')

    except Exception as e:
        print('Error:', e)
        response = build_response(400, 'Error processing request')
   
    return response

def get_product(products_id):
    try:
        response = dynamodb_table.get_item(Key={'id': products_id})
        return build_response(200, response.get('Item'))
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])

def get_ProductList():
    try:
        obj = {
            'TableName': dynamodb_table.name
        }
       
        return build_response(200, get_records(obj, []))
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])

def get_records(tbl, item):
    response = dynamodb_table.scan(**tbl)
    print(response)
    item.extend(response.get('Items', []))
   
    if 'LastEvaluatedKey' in response:
        tbl['ExclusiveStartKey'] = response['LastEvaluatedKey']
        return get_records(tbl, item)
    else:
        return {'Products': item}

def add_product(request_body):
    try:
        dynamodb_table.put_item(Item=request_body)
        body = {
            'Operation': 'Add',
            'Message': 'SUCCESS',
            'Item': request_body
        }
        return build_response(200, body)
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])

def update_product(product_id, key, value):
    try:
        response = dynamodb_table.update_item(
            Key={'id': product_id},
            UpdateExpression=f'SET {key} = :value',
            ExpressionAttributeValues={':value': value},
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttributes': response
        }
        return build_response(200, body)
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])

def delete_product(product_id):
    try:
        response = dynamodb_table.delete_item(
            Key={'id': product_id},
            ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'Item': response
        }
        return build_response(200, body)
    except ClientError as e:
        print('Error:', e)
        return build_response(400, e.response['Error']['Message'])



def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
