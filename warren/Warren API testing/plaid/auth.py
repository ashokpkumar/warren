'''
Obtain a link_token by calling /link/token/create.
Initialize Link by passing in the link_token. When your user completes the Link flow, Link will pass back a public_token. For more information on initializing and receiving data back from Link, see the Link documentation.
Exchange the public_token for an access_token by calling /item/public_token/exchange.
'''


import base64
import os
import datetime
import plaid
import json
import time


PLAID_CLIENT_ID = '6042059bec77930010caf9ee'
PLAID_SECRET = '748beb56b09de36bf05af24d53f38a'
PLAID_ENV = 'sandbox'
PLAID_COUNTRY_CODES = ['US']
PLAID_REDIRECT_URI = 'http://localhost:3000'
PLAID_PRODUCTS = ['transactions']
client = plaid.Client(client_id=PLAID_CLIENT_ID,
                      secret=PLAID_SECRET,
                      environment=PLAID_ENV,
                      api_version='2019-05-29')
#Plaid Test App
configs = {
  'user': {
      'client_user_id': '6042059bec77930010caf9ee',
  },
  'products': ['auth', 'transactions'],
  'client_name': "Plaid Quickstart",
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

response = client.LinkToken.create(configs)

print(response)
link_token = response['link_token']

print(link_token)


response = client.Institutions.get(5, offset=0)
institutions = response['institutions']
#print(institutions)

res = client.Sandbox.public_token.create(
        'ins_116580',
        ['transactions']
      )
# The generated public_token can now be
# exchanged for an access_token
publicToken = res['public_token']
res = client.Item.public_token.exchange(publicToken)
print(res)
access_token = res['access_token']

response = client.Transactions.get(access_token,
                                   start_date='2016-01-01',
                                   end_date='2021-02-01')
        
print(response)
transactions = response['transactions']

print(transactions)