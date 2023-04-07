import flickrapi
import requests
from requests_oauthlib import OAuth1Session
import platform

session = requests.Session()
session.headers.update({'User-Agent': 'Custom user agent'})

session.get('https://httpbin.org/headers')

# Replace with your own API key and secret
api_key = 'ff74e5e5a06b8f1ffe916d6f29bed921'
api_secret = 'ecd5964390cb76b8'

# Initialize the Flickr API client
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Use the 'requests_oauthlib' module to obtain a request token
request_token_url = 'https://www.flickr.com/services/oauth/request_token'
callback_url = 'http://localhost:8000/'
oauth = OAuth1Session(api_key, client_secret=api_secret)
user_agent = 'MyApp/1.0 ({}; {}) Python/{} Requests/{}'.format(
    platform.system(), platform.release(), platform.python_version(), requests.__version__)

headers = {'User-Agent': user_agent}
fetch_response = oauth.fetch_request_token(request_token_url, headers=headers)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

# Print the request token and secret
print('Request Token: {}'.format(resource_owner_key))
print('Request Token Secret: {}'.format(resource_owner_secret))

# Generate the authorization URL to open in a web browser
oauth = OAuth1Session(api_key, client_secret=api_secret)
base_authorization_url = 'https://www.flickr.com/services/oauth/authorize'
authorization_url = oauth.authorization_url(base_authorization_url)
print('Please go here and authorize: {}'.format(authorization_url))

# Retrieve the verification code from the user and exchange the request token for an access token
verifier = input('Paste the verification code here: ')
access_token_url = 'https://www.flickr.com/services/oauth/access_token'
callback_url = 'http://localhost:8000/'
oauth = OAuth1Session(api_key, client_secret=api_secret, callback_uri=callback_url, headers=headers)
oauth_tokens = oauth.fetch_access_token(access_token_url)
access_token = oauth_tokens.get('oauth_token')
access_token_secret = oauth_tokens.get('oauth_token_secret')


# Set the access token and secret for the Flickr API client
flickr.set_oauth_token(access_token, access_token_secret)

# Call the 'flickr.test.login' method to retrieve information about the authenticated user
response = flickr.test.login()
user_id = response['user']['id']
username = response['user']['username']['_content']

# Print the user ID and username
print('User ID: {}'.format(user_id))
print('Username: {}'.format(username))

# Call the 'flickr.auth.checkToken' method to confirm that the access token is valid
auth_info = flickr.auth.checkToken(format='parsed-json')
full_name = auth_info['auth']['user']['fullname']
print('Access token is valid for user: {}'.format(full_name))
