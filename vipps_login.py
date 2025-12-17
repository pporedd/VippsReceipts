import requests
import base64
import os
import json

# Configuration
CLIENT_ID = os.getenv("VIPPS_CLIENT_ID", "your_client_id")
CLIENT_SECRET = os.getenv("VIPPS_CLIENT_SECRET", "your_client_secret")
SUBSCRIPTION_KEY = os.getenv("VIPPS_SUBSCRIPTION_KEY", "your_subscription_key")
MERCHANT_SERIAL_NUMBER = os.getenv("VIPPS_MERCHANT_SERIAL_NUMBER", "your_msn")
REDIRECT_URI = os.getenv("VIPPS_REDIRECT_URI", "your_redirect_uri")
VIPPS_BASE_URL = "https://apitest.vipps.no"  # Use https://api.vipps.no for production

def get_access_token_client_credentials():
    """
    Obtains an access token using Client Credentials (for backend-to-backend calls).
    This is used for ePayment and Order Management APIs.
    """
    url = f"{VIPPS_BASE_URL}/accesstoken/get"
    headers = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Merchant-Serial-Number": MERCHANT_SERIAL_NUMBER
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def login_user(auth_code):
    """
    Exchanges the authorization code for an ID token and Access Token (Login API).
    This is the "Log in" part.
    """
    url = f"{VIPPS_BASE_URL}/access-management-1.0/access/oauth2/token"

    # Basic Auth for the token endpoint
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

def get_user_info(access_token):
    """
    Fetches the user's profile information using the access token.
    """
    url = f"{VIPPS_BASE_URL}/vipps-userinfo-api/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("This script demonstrates the Vipps Login flow.")
    print("In a real application, you would redirect the user to:")
    print(f"{VIPPS_BASE_URL}/access-management-1.0/access/oauth2/auth?client_id={CLIENT_ID}&response_type=code&scope=openid email name phoneNumber&state=some_state&redirect_uri={REDIRECT_URI}")

    # Simulated flow
    auth_code = input("Enter the Authorization Code received from the callback: ")
    if auth_code:
        try:
            tokens = login_user(auth_code)
            print("\nTokens received:")
            print(json.dumps(tokens, indent=2))

            user_info = get_user_info(tokens["access_token"])
            print("\nUser Info received:")
            print(json.dumps(user_info, indent=2))

            print("\nNow you have identified the user. You can use their 'sub' or 'phone_number' to look up their receipts in your local database.")
        except Exception as e:
            print(f"Error: {e}")
