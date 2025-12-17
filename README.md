# Vipps Receipts Integration

This project demonstrates how to "grab receipts" and identify users using the Vipps MobilePay APIs.

## Overview

The user request "parse through the api such that we can immediately grab receipts when people log in for us through vipps pay on their phone" involves two distinct concepts in the Vipps ecosystem:

1.  **"Log in ... through Vipps Pay"**: This refers to the **Login API**, which allows you to authenticate users and retrieve their profile information (Name, Phone, Email).
2.  **"Grab receipts"**: This refers to retrieving transaction details. Since Vipps does not provide a "Get All Receipts" API for privacy reasons, this usually means fetching the details of a specific payment using the **ePayment API** or **Order Management API**.

## Scripts

### 1. `store_receipts.py` (Main Storage Script)
This is the main utility for fetching and storing receipt data.
*   **Function**: Fetches receipt data from **both** the ePayment API (checking for "pre-built" order details) and the Order Management API.
*   **Storage**: Saves the data to a local JSON file (`receipts.json`). This JSON file serves as a temporary storage before migrating to SQLite.
*   **Usage**: `python3 store_receipts.py` -> Enter Order ID.

### 2. `vipps_login.py` (User Identification)
Demonstrates the Login flow:
1.  Redirects user to Vipps Login.
2.  Exchanges the returned `code` for an `access_token`.
3.  Fetches **User Info** (Name, Phone Number, etc.).
*Use this to identify WHO is logging in.*

### 3. `vipps_payment_receipt.py` (Payment Link Demo)
Demonstrates how to fetch payment details using just the **ePayment API**:
1.  Uses a payment reference (Order ID).
2.  Returns the `receiptUrl` if one was provided during payment creation.

### 4. `vipps_order_details.py` (Receipt Data Demo)
Demonstrates how to fetch the full structured receipt data using just the **Order Management API**:
1.  Uses an Order ID.
2.  Returns the `orderLines` and `bottomLine` (items, tax, total).

## Data Storage (`receipts.json`)

The `store_receipts.py` script saves data in the following format:

```json
[
  {
    "orderId": "12345",
    "fetchedAt": "2023-10-27T10:00:00Z",
    "source": ["epayment_api", "order_management_api"],
    "receipt": {
      "orderLines": [...],
      "bottomLine": {...}
    },
    "receiptUrl": "https://example.com/receipt.pdf"
  }
]
```

## Usage

1.  **Set Environment Variables**:
    You need to set the following environment variables with your credentials from the [Vipps Portal](https://portal.vippsmobilepay.com/):
    ```bash
    export VIPPS_CLIENT_ID="your_client_id"
    export VIPPS_CLIENT_SECRET="your_client_secret"
    export VIPPS_SUBSCRIPTION_KEY="your_subscription_key"
    export VIPPS_MERCHANT_SERIAL_NUMBER="your_msn"
    export VIPPS_REDIRECT_URI="your_redirect_uri" # Only for Login
    ```

2.  **Run the Scripts**:
    ```bash
    # To identify a user
    python3 vipps_login.py

    # To fetch and store a receipt
    python3 store_receipts.py
    ```

## Prerequisites

*   Python 3
*   `requests` library (`pip install requests`)
