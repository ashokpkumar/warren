from flask import Flask, jsonify,render_template
import base64
import os
import datetime
import plaid
import json
import time
#import jsonify
import json
PLAID_CLIENT_ID = '6042059bec77930010caf9ee'
PLAID_SECRET = '748beb56b09de36bf05af24d53f38a'
PLAID_ENV = 'sandbox'
PLAID_COUNTRY_CODES = ['US']
PLAID_REDIRECT_URI = 'http://localhost:3000'

app = Flask(__name__)
client = plaid.Client(client_id=PLAID_CLIENT_ID,
                      secret=PLAID_SECRET,
                      environment=PLAID_ENV,
                      api_version='2019-05-29')

configs = {
                'user': {
                    'client_user_id': '6042059bec77930010caf9ee',
                },
                'products': ['auth', 'transactions'],
                'client_name': "Plaid Test App",
                'country_codes': ['GB'],
                'language': 'en',
                'webhook': 'https://sample-webhook-uri.com',
                'link_customization_name': 'default',
                'account_filters': {
                    'depository': {
                        'account_subtypes': ['checking', 'savings'],
                    },
                },
                }

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/linktoken')
def linktoken():
    global response 
    response = client.LinkToken.create(configs) # this is link token
    return response


@app.route('/institutions')
def institutions():
    response = client.Institutions.get(500, offset=0)
    institutions = response['institutions']
    return render_template("institutions.html",data = institutions)


@app.route('/instiution/<insid>')
def institution(insid):
    response = client.LinkToken.create(configs)
    link_token = response['link_token']
    res = client.Sandbox.public_token.create(
        insid,    # This is bank of america chase
        ['transactions']
      )
    publicToken = res['public_token']
    res = client.Item.public_token.exchange(publicToken)
    access_token = res['access_token']

    transaction_response = client.Transactions.get(access_token,start_date='2016-01-01',end_date='2021-02-01')
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TRANSACTION>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #print(transaction_response)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>BALANCE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    balance_response = client.Accounts.balance.get(access_token)
    #print(balance_response)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ACCOUNTS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    accounts_response = client.Accounts.get(access_token)
    #print(accounts_response)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #https://plaid.com/docs/investments/add-to-app/
    # response = client.Holdings.get(access_token)
    # print(response)
    return render_template("transactions.html",transactions = transaction_response.get('transactions'),balances = balance_response.get('accounts'),accounts = accounts_response.get('accounts'))



if __name__ == '__main__':
    app.run(debug=True)