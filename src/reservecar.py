import json
import boto3 

s3 = boto3.resource('s3') 
bucket_name = "projetoes"
file_name = "carros.txt"
def lambda_handler(event, context): 
    #ugly solution with hard-coded names 
    obj = s3.Object('projetoes', 'carros.txt') 
    body = obj.get()['Body'].read() 
    result = [] 
    print(body) 
    strfinal=""
    elements = body.decode("utf-8").split('\n'); 
    for e in elements: 
        b, modelo, a, cor, reservado, vin = e.split(',') 
        id = int(b)
        preco = int(a) 
        if event["queryStringParameters"]:
            if event["queryStringParameters"]["id"] == b and reservado=="False":
                y={'id':id, 'modelo': modelo, 'preco':preco, 'cor':cor, 'reservado':"True", 'vin':vin}
                result.append({'id':id, 'modelo': modelo, 'preco':preco, 'cor':cor, 'reservado':"True", 'vin':vin})
                strfinal += str(y["id"]) + "," + y["modelo"]+"," + str(y["preco"]) + "," + y["cor"] + "," + y["reservado"] + "," + y["vin"] + "\n"
                
            else:
                strfinal+= (e+"\n")
    strfinal=strfinal[:len(strfinal)-1]
    obj.put(Body=strfinal)
    if not result:
        return {
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'http://cardealership-group4.s3-website-us-east-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': 'Car already reserved or does not exist'
        }
    else:
        return { 
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'http://cardealership-group4.s3-website-us-east-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(result[0]["vin"][:len(result[0]["vin"])-1]) 
            
    }