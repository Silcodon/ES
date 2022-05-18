import json
import boto3 

s3 = boto3.resource('s3') 
def lambda_handler(event, context): 
    #ugly solution with hard-coded names 
    obj = s3.Object('projetoes', 'carros.txt') 
    body = obj.get()['Body'].read() 
    result = [] 
    print(body) 
    elements = body.decode("utf-8").split('\n'); 
    for e in elements: 
        b, modelo, a, cor, reservado, vin = e.split(',') 
        id = int(b)
        preco = int(a) 
        if event["queryStringParameters"]:
            if event["queryStringParameters"]["modelo"].upper() == modelo.upper() and event["queryStringParameters"]["cor"].upper()==cor.upper() and reservado=="False":
                result.append({'id':id, 'modelo': modelo, 'preco':preco, 'cor':cor, 'reservado':reservado})   
          
        else :
            result.append({'id':id, 'modelo': modelo, 'preco':preco, 'cor':cor, 'reservado':reservado, 'vin':vin})   
        
    if not result:
        return {
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'http://cardealership-group4.s3-website-us-east-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': 'No cars available'
        }
    else:
        return { 
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'http://cardealership-group4.s3-website-us-east-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(result) 
            
    }