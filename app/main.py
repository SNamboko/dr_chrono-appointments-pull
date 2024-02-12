# main.py

import urllib.parse
import requests
from config import DRCHRONO_CONFIG

# Step 1: Build Authorization URL
authorization_url = (
    f"{DRCHRONO_CONFIG['authorization_base_url']}?redirect_uri="
    f"{urllib.parse.quote(DRCHRONO_CONFIG['redirect_uri'], safe='')}&response_type=code&client_id="
    f"{urllib.parse.quote(DRCHRONO_CONFIG['client_id'], safe='')}&scope="
    f"{urllib.parse.quote(DRCHRONO_CONFIG['scope'], safe=' ')}"
)

print(f"Visit the following URL to authorize your application:\n{authorization_url}")

# Step 2: Get Authorization Code from User Input
authorization_code = input("Enter the authorization code from the redirect URL: ")

# Step 3: Exchange Authorization Code for Tokens
token_url = DRCHRONO_CONFIG['token_url']
token_data = {
    'code': authorization_code,
    'grant_type': 'authorization_code',
    'redirect_uri': DRCHRONO_CONFIG['redirect_uri'],
    'client_id': DRCHRONO_CONFIG['client_id'],
    'client_secret': DRCHRONO_CONFIG['client_secret'],
}

# Step 4: Make a POST request to the token URL

response = requests.post(token_url, data=token_data)

# Check if the request was successful
response.raise_for_status()

# Step 5: Parse the Response JSON

token_info = response.json()

# Extract tokens
access_token = token_info['access_token']
refresh_token = token_info['refresh_token']
expires_in = token_info['expires_in']

print(f"Access Token: {access_token}")
print(f"Refresh Token: {refresh_token}")
print(f"Expires In: {expires_in} seconds")

# Step 6: Refresh Token (Optional)
refresh_token_data = {
    'refresh_token': refresh_token,
    'grant_type': 'refresh_token',
    'client_id': DRCHRONO_CONFIG['client_id'],
    'client_secret': DRCHRONO_CONFIG['client_secret'],
}

refresh_response = requests.post(token_url, data=refresh_token_data)

# Check if the refresh request was successful
refresh_response.raise_for_status()

# Parse the refreshed token response JSON
refresh_token_info = refresh_response.json()

# Extract refreshed tokens
new_access_token = refresh_token_info['access_token']
new_refresh_token = refresh_token_info['refresh_token']
new_expires_in = refresh_token_info['expires_in']

print(f"Refreshed Access Token: {new_access_token}")
print(f"New Refresh Token: {new_refresh_token}")
print(f"Expires In: {new_expires_in} seconds")
