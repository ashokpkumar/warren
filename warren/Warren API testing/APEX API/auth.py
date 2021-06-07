#!/usr/bin/python

"""
Sample class to generate an Authorization token.
The Client Credentials authentication flow follows these steps:
1) an application encodes its username, entity and shared secret into a JSON Web Signature (JWS)
2) an application makes a POST request to the legit/v1/cc/token endpoint to exchange its JWS for a JSON Web Token (JWT)
3) an application uses the JWT to authenticate when accessing the REST APIs
Tokens are valid for 24 hours.
Note: In the interest of succinct code, very little error checking (actually none) is included.
"""

""" Before running, replace the correspondent code and shared secret
	in APICredentials.json with the correspondent code and shared secret
	received from Apex.
"""

import base64
from datetime import datetime

import jws
from tzlocal import get_localzone

import json
import requests
import sys

import hashlib
import base64


class APEXToken:

	token = ""

	# Change this to "https://api.apexclearing.com" for production
	baseURL = "https://uat-api.apexclearing.com"


	def __init__(self, credential_file):
		self.token = self.getToken(credential_file)

	# Helper functions
	def to_base64(self, s):
		# This statement is more complicated than otherwise need be in 
		# order to be capatible with both python 2 and 3 . 
		# Note that the jws library is not compatible with python 3 as of Jan 2017.
		return base64.b64encode(s.encode('utf-8')).decode('utf-8').replace("=","")

	def loadCredentials(self, credentialFile):
		""" Credentials consist of a username, entity and shared secret
			username = Apex-given user name. Typically "sentinel" or "atlas"
			entity = 4-character correspondent identifier = correspondent.[Correspondent code]
			sharedSecret = secret password supplied by APEX
			Example:
			{
				"username": "atlas",
				"entity": "correspondent.apx1", # apx1 is APEX's test correspondent code. Substiture yours
				"sharedSecret": "[YOUR SECRET KEY]"
			}
		"""
		with open(credentialFile, 'r') as data_file:
			credentials = json.load(data_file)
		return credentials
	############### End of helper functions

	def getToken(self, credential_file):
		""" Reads client's credentials from a JSON-formatted file and returns a Legit Token.
			Return type is streaming text (not JSON)."""

		credentials = self.loadCredentials(credential_file)
		jws = self.jws(credentials)
		request = requests.get(self.baseURL + '/legit/api/v1/cc/token?jws=%s' % jws)

		return request.content

	def jws(self, credentials):
		"""Encode and return the username, entity and shared secret in a JSON web signature (JWS)"""
		dt =  datetime.now(get_localzone()).isoformat('T')
		signature_header = {'alg': 'HS512'}
		signature_body = {'username': credentials['username'], 'entity': credentials['entity'], 'datetime': dt}

		h = json.dumps(signature_header)
		encoded_header = self.to_base64(h)

		sb = json.dumps(signature_body)
		encoded_body = self.to_base64(sb)

		# signature is already encoded
		signature = jws.sign(h, sb, credentials["sharedSecret"],is_json=True)
		
		# The JWS Pthon library is unusual in that it only returns the signed/hashed
		# string. Libraries in other languages return the entire jws
		# (e.g 'encoded_header.encoded_body.signature') so the concatentation
		# is not necessary.

		return encoded_header + "." + encoded_body + "." + signature

	def release(self):
		""" Tokens do not need to be explicitly released.
			There may be instances where a client wants to invalidate a token so
			this method was included for completeness."""

		headers = {'Authorization'	: self.token}
		requests.get(self.baseURL + '/legit/api/v1/logout', headers=headers)
		token = ""

if __name__ == "__main__":

	T = APEXToken("APICredentials.json")
	print ("Token is: %s" % T.token)

	# Ask legit to verify our Atlas token...
	headers = {'Authorization': T.token}
	request = requests.get(T.baseURL + '/legit/api/v2/verify', headers=headers)
	print ("\nVerification Results: ") 
	print (request.content)

	T.release()