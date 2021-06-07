# import test2
import json
import requests
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

test_api_urls = [
    "https://sandbox.api.yodlee.com:443/ysl/institutions",
    "https://sandbox.api.yodlee.com:443/ysl/user",
    "https://sandbox.api.yodlee.com:443/ysl/statements",
    "https://sandbox.api.yodlee.com:443/ysl/accounts"
]


@app.route('/')
def student():
   return render_template('student.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():

    email = ""
    name = ""
    role = ""
    currency = ""
    token = ""
    statement_info = []
    account = []
    if request.method == 'POST':
       result = request.form
       #changes from here
       client_name = result["Name"]
       #client_name = "sbMem60l28ab4b29db1"
       auth_url = "https://sandbox.api.yodlee.com:443/ysl/auth/token"
       headers = {"loginName": client_name,"Api-Version": "1.1"}
       body = {"clientId": "2zDjThJ4A0drpo8Uw5UQmI4PmzsYOqVC","secret": "NLpRuj9TAKmc7c0f"}
       resp = requests.post(auth_url, headers=headers,data = body)
       if resp.status_code!=201:
           return resp.text

       token_string = json.loads(resp.text)
       token = token_string["token"]["accessToken"]
 

       headers = {"Authorization": "Bearer "+ token, "Api-Version": "1.1"}
       resp = requests.get("https://sandbox.api.yodlee.com:443/ysl/user", headers=headers)

       if resp.status_code==200:
                      
            data = json.loads(resp.text)
            #print ">>>>>>>>>>>>>>>>>>>>", data
            email = data['user']['email']
            name = data['user']['name']['first'] + data['user']['name']['last']
            role = data['user']['roleType']
            currency = data['user']['preferences']['currency']
      
                # For Statements
            resp = requests.get("https://sandbox.api.yodlee.com:443/ysl/statements", headers=headers)
            data = json.loads(resp.text)
            #print ">>>>>>>>>>>>>>>>>>>>", data
            statements =  data['statement']
     
            statement_info = [[statement['amountDue']['amount'],statement['amountDue']['currency'],statement['dueDate']] for statement in statements]

            try:
                #For Accounts
                resp = requests.get("https://sandbox.api.yodlee.com:443/ysl/accounts", headers=headers)
                data = json.loads(resp.text)
                #print ">>>>>>>>>>>>>>>>>>>>", data
                account_info =  data['account']
                account = [[account['CONTAINER'],account["balance"]["amount"],account["balance"]["currency"],account["accountNumber"],account['accountName']] for account in account_info]
            except:
                pass    
       status_code = resp.status_code

       return render_template('user.html',status_code = status_code, email=email,name=name,role=role,currency=currency,token = token,statement = statement_info, account = account)


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True, port=5000)

    
