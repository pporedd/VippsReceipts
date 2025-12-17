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

def get_order_details(order_id, access_token):
    """
    Fetches the full order details (receipt) from Order Management API.
    """
    # Note: paymentType is usually 'ecom' for ePayment and eCom API payments.
    url = f"{VIPPS_BASE_URL}/order-management/v2/ecom/{order_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Merchant-Serial-Number": MERCHANT_SERIAL_NUMBER
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("This script demonstrates fetching full order details (receipt data) from Vipps Order Management API.")

    order_id = input("Enter the Order ID (transactionId): ")
    if order_id:
        try:
            token = get_access_token()
            print(f"Access Token obtained: {token[:10]}...")

            order_details = get_order_details(order_id, token)
            print("\nOrder Details (Receipt):")
            print(json.dumps(order_details, indent=2))

            # Parsing the receipt info
            if "receipt" in order_details:
                receipt = order_details["receipt"]
                print("\n--- Receipt Summary ---")
                if "bottomLine" in receipt:
                    print(f"Total Amount: {receipt['bottomLine'].get('totalAmount', 0) / 100} {receipt['bottomLine'].get('currency', 'NOK')}")
                if "orderLines" in receipt:
                    print(f"Items: {len(receipt['orderLines'])}")
                    for item in receipt["orderLines"]:
                        print(f"- {item['name']}: {item['totalAmount']/100}")
            else:
                print("\nNo 'receipt' object found in order details.")

        except Exception as e:
            print(f"Error: {e}")
