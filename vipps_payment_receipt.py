import requests
import os
import json

# Configuration
CLIENT_ID = os.getenv("VIPPS_CLIENT_ID", "your_client_id")
CLIENT_SECRET = os.getenv("VIPPS_CLIENT_SECRET", "your_client_secret")
SUBSCRIPTION_KEY = os.getenv("VIPPS_SUBSCRIPTION_KEY", "your_subscription_key")
MERCHANT_SERIAL_NUMBER = os.getenv("VIPPS_MERCHANT_SERIAL_NUMBER", "your_msn")
VIPPS_BASE_URL = "https://apitest.vipps.no"  # Use https://api.vipps.no for production

def get_access_token():
    """
    Obtains an access token using Client Credentials.
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

def get_payment_details(reference, access_token):
    """
    Fetches payment details from ePayment API.
    Includes 'receiptUrl' if available.
    """
    url = f"{VIPPS_BASE_URL}/epayment/v1/payments/{reference}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Merchant-Serial-Number": MERCHANT_SERIAL_NUMBER
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("This script demonstrates fetching payment details (receipt link) from Vipps ePayment API.")

    reference = input("Enter the Payment Reference (orderId): ")
    if reference:
        try:
            token = get_access_token()
            print(f"Access Token obtained: {token[:10]}...")

            payment_details = get_payment_details(reference, token)
            print("\nPayment Details:")
            print(json.dumps(payment_details, indent=2))

            if "receiptUrl" in payment_details:
                print(f"\nReceipt URL: {payment_details['receiptUrl']}")
            else:
                print("\nNo 'receiptUrl' found in the payment details.")

        except Exception as e:
            print(f"Error: {e}")
