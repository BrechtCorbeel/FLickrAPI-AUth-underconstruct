import flickrapi
import requests
from requests_oauthlib import OAuth1
from urllib.parse import urlparse, parse_qsl

# Replace with your own API key and secret
api_key = 'ff74e5e5a06b8f1ffe916d6f29bed921'
api_secret = 'ecd5964390cb76b8'

# Initialize the Flickr API client
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Get the request token
request_token_url = 'https://www.flickr.com/services/oauth/request_token'
oauth = OAuth1(api_key, client_secret=api_secret)
response = requests.post(request_token_url, auth=oauth, params={'oauth_callback': 'oob'})

print("Request token response:", response.text)  # Add this line
request_token = dict(parse_qsl(response.text))


# Get the authorization URL to open in a web browser
authorize_url = 'https://www.flickr.com/services/oauth/authorize'
authorization_url = f"{authorize_url}?oauth_token={request_token['oauth_token']}&perms=read"
print('Please go here and authorize:', authorization_url)

# Retrieve the verification code from the user and exchange the request token for an access token
verifier = input('Paste the verification code here: ')
access_token_url = 'https://www.flickr.com/services/oauth/access_token'
oauth = OAuth1(api_key, client_secret=api_secret,
               resource_owner_key=request_token['oauth_token'],
               resource_owner_secret=request_token['oauth_token_secret'],
               verifier=verifier)
response = requests.post(access_token_url, auth=oauth)
access_token_info = dict(parse_qsl(response.text))

# Call the 'flickr.groups.getInfo' method to retrieve information about a group
response = flickr.groups.getInfo(group_id='GROUP_ID')


# Get a list of all the groups that the authenticated user is a member of
groups = flickr.people.getGroups(format='parsed-json')

# Call the 'flickr.test.login' method to retrieve information about the authenticated user
response = flickr.test.login()
user_id = response['user']['id']
username = response['user']['username']['_content']

# Print the user ID and username
print('User ID:', user_id)
print('Username:', username)

# Call the 'flickr.auth.checkToken' method to confirm that the access token is valid
auth_info = flickr.auth.checkToken(format='parsed-json')
full_name = auth_info['auth']['user']['fullname']
print('Access token is valid for user:', full_name)

# Print some basic information about each group
for group in groups['groups']['group']:
    print('Group name:', group['name']['_content'])
    print('Group ID:', group['nsid'])
    print('Group description:', group['description']['_content'])
    print('---')

    # Get more detailed information about the group
    group_info = flickr.groups.getInfo(group_id=group['nsid'], format='parsed-json')
    print('Group members:', group_info['group']['members'])
    print('Group photos:', group_info['group']['pool_count'])
    print('---')

# Custom TokenCache class
class CustomTokenCache(flickrapi.TokenCache):
    def __init__(self, oauth_token, oauth_token_secret):
        self._token = (oauth_token, oauth_token_secret)

    def token(self):
        return self._token
    

# Set the access token and secret for the Flickr API client
custom_token_cache = CustomTokenCache(access_token_info['oauth_token'], access_token_info['oauth_token_secret'])
flickr.token_cache = custom_token_cache
