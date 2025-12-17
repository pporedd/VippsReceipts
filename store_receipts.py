import requests
import os
import json
import time

# Configuration
CLIENT_ID = os.getenv("VIPPS_CLIENT_ID", "your_client_id")
CLIENT_SECRET = os.getenv("VIPPS_CLIENT_SECRET", "your_client_secret")
SUBSCRIPTION_KEY = os.getenv("VIPPS_SUBSCRIPTION_KEY", "your_subscription_key")
MERCHANT_SERIAL_NUMBER = os.getenv("VIPPS_MERCHANT_SERIAL_NUMBER", "your_msn")
VIPPS_BASE_URL = "https://apitest.vipps.no"  # Use https://api.vipps.no for production
STORAGE_FILE = "receipts.json"

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

def get_epayment_details(reference, access_token):
    """
    Fetches payment details from ePayment API.
    Checks for 'receipt' (pre-built order lines) and 'receiptUrl'.
    """
    url = f"{VIPPS_BASE_URL}/epayment/v1/payments/{reference}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Merchant-Serial-Number": MERCHANT_SERIAL_NUMBER
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Warning: Could not fetch ePayment details: {e}")
        return None

def get_order_management_details(order_id, access_token):
    """
    Fetches the full order details from Order Management API.
    """
    url = f"{VIPPS_BASE_URL}/order-management/v2/ecom/{order_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Merchant-Serial-Number": MERCHANT_SERIAL_NUMBER
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return None # No separate order management data found
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Warning: Could not fetch Order Management details: {e}")
        return None

def save_receipt(data):
    """
    Saves the receipt data to a JSON file.
    """
    existing_data = []
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {STORAGE_FILE} was corrupted. Starting fresh.")

    # Check if record already exists (update it)
    updated = False
    for i, record in enumerate(existing_data):
        if record.get("orderId") == data.get("orderId"):
            existing_data[i] = data
            updated = True
            break

    if not updated:
        existing_data.append(data)

    with open(STORAGE_FILE, "w") as f:
        json.dump(existing_data, f, indent=2)

    print(f"Receipt saved to {STORAGE_FILE}")

def main():
    print("Vipps Receipt Storage Tool")
    order_id = input("Enter the Order ID (transactionId/reference): ")

    if not order_id:
        print("Order ID is required.")
        return

    try:
        token = get_access_token()
        print("Authenticated.")

        # 1. Try ePayment API (covers Pre-built integration)
        epayment_data = get_epayment_details(order_id, token)

        # 2. Try Order Management API (covers separate integration)
        om_data = get_order_management_details(order_id, token)

        # Combine data
        combined_record = {
            "orderId": order_id,
            "fetchedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source": [],
            "receipt": None,
            "receiptUrl": None
        }

        if epayment_data:
            combined_record["source"].append("epayment_api")
            # Check for pre-built receipt data
            if "receipt" in epayment_data:
                 combined_record["receipt"] = epayment_data["receipt"]
            if "receiptUrl" in epayment_data:
                 combined_record["receiptUrl"] = epayment_data["receiptUrl"]

        if om_data:
            combined_record["source"].append("order_management_api")
            # Order Management API usually returns the receipt object directly or wrapped
            if "receipt" in om_data:
                 combined_record["receipt"] = om_data["receipt"] # Overwrite/enrich if newer
            if "category" in om_data and "orderDetailsUrl" in om_data["category"]:
                 combined_record["receiptUrl"] = om_data["category"]["orderDetailsUrl"]

        if not combined_record["receipt"] and not combined_record["receiptUrl"]:
             print("No receipt data or URL found for this order.")
        else:
             save_receipt(combined_record)
             print("\nCaptured Data:")
             print(json.dumps(combined_record, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
