import json
import boto3 

s3 = boto3.resource('s3') 
bucket_name = "projetoes"
file_name = "carros.txt"
def lambda_handler(event, context): 
    
    return { 
        'statusCode': 200, 
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'https://logisticreader.s3.amazonaws.com',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': 'The delivery was confirmed!' 
        
    }