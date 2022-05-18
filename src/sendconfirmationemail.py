import json
import smtplib, ssl
from email.mime.text import MIMEText

def lambda_handler(event, context):
    if event["queryStringParameters"]:
            modelo=event["queryStringParameters"]["modelo"]
            cor=event["queryStringParameters"]["cor"]
            vin=event["queryStringParameters"]["vin"]
            email=event["queryStringParameters"]["email"]
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "esawsteste@gmail.com"  # Enter your address
    receiver_email = email  # Enter receiver address
    password = "esaws222"
    msg = MIMEText("Hi there!\n\nHere are your order details.\nCar: "+modelo + "\nColor: " + cor + "\nVin: " +vin)

    msg['Subject'] = 'Order details'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
    return {
        'statusCode': 200,
        'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'http://cardealership-group4.s3-website-us-east-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
    }
