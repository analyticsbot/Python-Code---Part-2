#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generates refresh token for AdWords using the Installed Application flow."""


import argparse
import sys

from oauth2client import client

# Your OAuth 2.0 Client ID and Secret. If you do not have an ID and Secret yet,
# please go to https://console.developers.google.com and create a set.

## production account
CLIENT_ID = '585883628562-aa30lslm9054ut09ke8guk5aum82ak89.apps.googleusercontent.com'
CLIENT_SECRET = 'mUa3dIphJ5dOsvwRUkwD1-oj'

#test account
CLIENT_ID = '535819312718-bvduhadaeouvk4sofkofe9ar1efvj1u5.apps.googleusercontent.com'
CLIENT_SECRET = 'EVX7Y-q2XPfT7MZlgsmDFWEI'

# The AdWords API OAuth 2.0 scope.
SCOPE = u'https://www.googleapis.com/auth/adwords'

def main(client_id, client_secret, scopes):
  """Retrieve and display the access and refresh token."""
  flow = client.OAuth2WebServerFlow(
      client_id=client_id,
      client_secret=client_secret,
      scope=scopes,
      user_agent='Ads Python Client Library',
      redirect_uri='urn:ietf:wg:oauth:2.0:oob')

  authorize_url = flow.step1_get_authorize_url()

  print ('Log into the Google Account you use to access your AdWords account'
         'and go to the following URL: \n%s\n' % (authorize_url))
  print 'After approving the token enter the verification code (if specified).'
  code = raw_input('Code: ').strip()

  try:
    credential = flow.step2_exchange(code)
  except client.FlowExchangeError, e:
    print 'Authentication has failed: %s' % e
    sys.exit(1)
  else:
    print ('OAuth 2.0 authorization successful!\n\n'
           'Your access token is:\n %s\n\nYour refresh token is:\n %s'
           % (credential.access_token, credential.refresh_token))


if __name__ == '__main__':
  main(CLIENT_ID, CLIENT_SECRET, SCOPE)
