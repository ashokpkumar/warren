import base64
import os
import datetime
import plaid
import json
import time

PLAID_CLIENT_ID = '6042059bec77930010caf9ee'
PLAID_SECRET = '748beb56b09de36bf05af24d53f38a'
PLAID_ENV = 'sandbox'
PLAID_PRODUCTS  = ['transactions']
PLAID_COUNTRY_CODES = ['US']
PLAID_REDIRECT_URI = 'http://localhost:3000/'