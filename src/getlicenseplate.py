import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    # Create SQS client
    sqs = boto3.client('sqs')
    
    queue_url = 'https://sqs.us-east-1.amazonaws.com/832902263268/SQSqueue'
    
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageAttributes={
        
        },
        MessageBody=(
            event["queryStringParameters"]["vin"]
        )
    )
    
    queue_url2 = 'https://sqs.us-east-1.amazonaws.com/832902263268/receivequeue'
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url2,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=2
    )
    
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url2,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % message)
    
    
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'http://cardealership-group4.s3-website-us-east-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
        'body': json.dumps(message["Body"])
    }