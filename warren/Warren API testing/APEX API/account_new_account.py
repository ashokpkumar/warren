#!/usr/bin/python

"""
Sample python code to create a request for a new account in Apex Account Management API.
    Before running, replace the correspondent code and shared secret
    in APICredentials.json with the correspondent code and shared secret
    received from Apex.
"""

import json
import requests
import sys

import hashlib
import base64

from auth import APEXToken

# Change this to "https://api.apexclearing.com" for production
baseURL = "https://uat-api.apexclearing.com"
# Change this to your 4-character correspondent code
correspondentCode = "APX1"
# Apex's test environment has a lot of traffic so the highWaterMark is set high.
# MOst correspondents can set this to 1 to start.
highWaterMark     = 929350

# First step is always to get a JWT.
Tok = APEXToken('APICredentials.json')
headers = {'Authorization': Tok.token}

# Get a form:

# Determine the latest version
versions = requests.get(baseURL + '/atlas/api/v1/forms/new_account_form/versions', headers=headers).json()
latestVersion = max(versions)

# The (V1) API enpoint for retrieving Forms is
# atlas/api/v1/forms/[FORM_NAME]/versions/[VERSION]
#
# FORM_NAME = name of the form -type you wish to receive
#   (i.e new_account_form, joint_tenants_in_common_form, foreign_due_diligence_form, etc.)
# VERSION = Version # of the form to receive. Note that the
#   version number ONLY changes when there's a schema change,
#   which is not very often.
#
# The returned form is in JSON and contains the text of the form in the 'document' field,
# and a schema for all the required & optional fields.

form = requests.get(baseURL + '/atlas/api/v1/forms/new_account_form/versions/%d' % latestVersion, headers=headers)

# Generate a hash:

# The hash ensures Apex, the correspondent and the customer are working off the exact same form.
# Text changes happen relatively often and do NOT affect the version #, but do change the hash.
#
# The hash value must be sent to ATLAS along with the form data. Apex keeps a database of forms
# keyed by hash, and will return an error if the hash is invalid or outdated.
#
# ATLAS always expects the latest version of the hash. 
# So you should either retrieve a hash each time you display/submit or form,
# or be sure to handle the error if you get an invalid hash.
#
# You must hash the entire return value of the form retrieval.

# Get the form HASH
hash_algorithm = hashlib.sha256()
hash_algorithm.update(form.text.encode('UTF-8'))

digest = hash_algorithm.digest()
form_hash = base64.b64encode(digest)
print ("\nFORM HASH: %s") % form_hash

# Load some sample account data.
# dataMinBD.json contains the minimal number of fields required for BD to open a cash-only customer account.
fName = "dataMinBD.json"

with open(fName, 'r') as data_file:
    request = json.load(data_file)

# Set the version number.
request['forms'][0]['formId']['version'] = latestVersion

# Set the hash code inside the form data.
request['forms'][0]['formSchemaHash'] = {'algorithm': 'SHA-256', 'hash': form_hash}


appResult = requests.post(baseURL + '/atlas/api/v2/account_requests', data=json.dumps(request), headers={'Authorization': Tok.token, 'Content-Type': 'application/json'})

print (appResult.content)

if appResult.status_code == 200:
    appResult = appResult.json()
    print ("Success! New application created. Account number %s; Status %s; RequestID %s") % (appResult['account'], appResult['status'], appResult['id'])

    # Get ALE messages related to account status
    # The format for the URL is as follows:
    #    /ale/api/v1/read/[topic]/[partition]/highWaterMark=###
    # topic = atlas-account_request-status
    # partition = correspondent ID (not documented, but needed)
    # highWaterMark = # of the highest ale message number received so far. New correspondents who are just starting to test can start with 1.

    # (more on ALE in a different code sample)
    aleMessages = requests.get(baseURL + '/ale/api/v1/read/atlas-account_request-status/%s?highWaterMark=%d' % (correspondentCode, highWaterMark), headers=headers).json()
    print ("Found %d ale messages." % len(aleMessages))

    for m in aleMessages:
        p = json.loads(m['payload'])
        if p['requestId'] == appResult['id']:
            print (m)

else:
    print ("ERROR: %d" % appResult.status_code)
    print (appResult.text)

Tok.release()