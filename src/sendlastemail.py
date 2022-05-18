import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import timedelta, date

def lambda_handler(event, context):
    if event["queryStringParameters"]:
            platenumber=event["queryStringParameters"]["platenumber"]
            vin=event["queryStringParameters"]["vin"]
            email=event["queryStringParameters"]["email"]
    deliverydate = str(date.today() + timedelta(days=10))
    url="https://0nhqek24j8.execute-api.us-east-1.amazonaws.com/ProjetoTeste/nomes"
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "esawsteste@gmail.com"  # Enter your address
    receiver_email = email  # Enter receiver address
    password = "esaws222"
    msg = MIMEMultipart('alternative')
    text = ("Hi there!\n\nHere are your delivery details.\nDelivery Date: "+deliverydate + "\nVin: " + vin + "\nPlate Number: " +platenumber+"\nPlease scan this QR Code when you receive the car\n")
    html = """\
    <html>
    <head>
        <title>Testing QR code</title>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script type="text/javascript">
            function generateBarCode()
            {
                var nric = $('#text').val();
                var url = 'https://api.qrserver.com/v1/create-qr-code/?data=' """+ url +""" '&amp;size=250x250';
                $('#barcode').attr('src', url);
            }
        </script>
    </head>
    <body>
            <p>Hi there!<br><br>Here are your delivery details.<br>Delivery Date: """+deliverydate + """<br>Vin: """+ vin +"""<br>Plate Number: """ +platenumber+"""<br><br>Please scan this QR Code when you receive the car<br></p>
        <script>generateBarCode(); </script> 

      <img id='barcode' 
            src="https://api.qrserver.com/v1/create-qr-code/?data="""+ url +"""&amp;size=250x250" 
            alt="" 
            title="HELLO" 
            width="250" 
            height="250" />
    </body>
</html>
    """
    msg['Subject'] = 'Delivery details'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    
    
    
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
