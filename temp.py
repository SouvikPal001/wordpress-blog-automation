import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = "https://public-api.wordpress.com/oauth2/token"

data = {
    "client_id": os.getenv("WP_CLIENT_ID"),
    "client_secret": os.getenv("WP_CLIENT_SECRET"),
    "redirect_uri": "https://localhost",
    "grant_type": "authorization_code",
    "code": os.getenv("WP_AUTH_CODE")
}

response = requests.post(TOKEN_URL, data=data)

if response.status_code == 200:
    token_info = response.json()
    print("✅ Access Token:", token_info['access_token'])
else:
    print("❌ Failed to get token:", response.status_code)
    print(response.text)
