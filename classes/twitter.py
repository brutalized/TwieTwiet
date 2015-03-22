#!/usr/bin/python3

# How to communicate via the twitter API.
# Untested.
#
# Steps:
#	- Obtain an access token and token secret as described here: https://dev.twitter.com/oauth/overview/application-owner-access-tokens
#	- Fill in your access token, access token secret, consumer secret and consumer key. You should be able to find all of those at https://dev.twitter.com/
#	- Try to run this program and see if it works.

import twitter.api as api
import twitter.oauth as oauth

token = 'test'
token_key = 'test'
con_secret = 'test'
con_secret_key = 'test'

auth = oauth.OAuth(token, token_key, con_secret, con_secret_key)
t = api.Twitter(auth=auth)

t.statuses.update(status="Fill in a twietwiet here if you can, because if it works it will actually post this message.")