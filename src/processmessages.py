console.log('Loading function');
const https = require('https')

exports.handler = async (event) => {
    
    //console.log('Received event:', JSON.stringify(event, null, 2));
    for (const { messageId, body } of event.Records) {
        
        var message=JSON.stringify(body);
        console.log('SQS message %s: %s', messageId, message);
        console.log(makeid(6));
        if (validateVin(message)!=null){
          let url = "https://sqs.us-east-1.amazonaws.com/832902263268/receivequeue?Action=SendMessage&MessageBody="+makeid(6)+"&Expires=2022-05-05T22%3A52%3A43PST&Version=2012-11-05&AUTHPARAMS"
            const promise = new Promise(function(resolve, reject) {
            https.get(url, (res) => {
                resolve(res.statusCode)
              }).on('error', (e) => {
                reject(Error(e))
              })
            })
          return promise
        }
        else{
            let url = "https://sqs.us-east-1.amazonaws.com/832902263268/receivequeue?Action=SendMessage&MessageBody=Vin not valid!&Expires=2022-05-05T22%3A52%3A43PST&Version=2012-11-05&AUTHPARAMS"
            const promise = new Promise(function(resolve, reject) {
            https.get(url, (res) => {
                resolve(res.statusCode)
              }).on('error', (e) => {
                reject(Error(e))
              })
            })
          return promise
        }
        
    }
    return `Successfully processed ${event.Records.length} messages.}`;
};


function validateVin(vin) {
    var re = new RegExp("[A-HJ-NPR-Z0-9]{17}");
    return vin.match(re);
}


function makeid(length) {
    var result           = [];
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    var numbers          = '0123456789';
    var charactersLength = characters.length;
    var numbersLength    = numbers.length;
    for ( var i = 0; i < length; i++ ) {
        if(i<2 || i>3){
            result.push(characters.charAt(Math.floor(Math.random() * charactersLength)));   
        }
        else{
            result.push(numbers.charAt(Math.floor(Math.random() * numbersLength)));  
        }
   }
   return result.join('');
}


function httpGet(options) {
  console.log(options)
  const https = require('https');
  return new Promise(((resolve, reject) => {
    const request = https.request(options, (response) => {
      response.setEncoding('utf8');
      let returnData = '';
      if (response.statusCode < 200 || response.statusCode >= 300) {
        return reject(new Error(`${response.statusCode}: ${response.req.getHeader('host')} ${response.req.path}`));
      }
      response.on('data', (chunk) => {
        returnData += chunk;
      });
      response.on('end', () => {
        resolve(response.statusCode); //Fill response with status code
      });
      response.on('error', (error) => {
        reject(error);
      });
    });
    request.end();
  }));
}