# Vipps Receipts Integration

This project demonstrates how to "grab receipts" and identify users using the Vipps MobilePay APIs.

## Overview

The user request "parse through the api such that we can immediately grab receipts when people log in for us through vipps pay on their phone" involves two distinct concepts in the Vipps ecosystem:

1.  **"Log in ... through Vipps Pay"**: This refers to the **Login API**, which allows you to authenticate users and retrieve their profile information (Name, Phone, Email).
2.  **"Grab receipts"**: This refers to retrieving transaction details. Since Vipps does not provide a "Get All Receipts" API for privacy reasons, this usually means fetching the details of a specific payment using the **ePayment API** or **Order Management API**.

## Scripts

### 1. `vipps_login.py` (User Identification)
Demonstrates the Login flow:
1.  Redirects user to Vipps Login.
2.  Exchanges the returned `code` for an `access_token`.
3.  Fetches **User Info** (Name, Phone Number, etc.).
*Use this to identify WHO is logging in.*

### 2. `vipps_payment_receipt.py` (Payment Link)
Demonstrates how to fetch payment details using the **ePayment API**:
1.  Uses a payment reference (Order ID).
2.  Returns the `receiptUrl` if one was provided during payment creation.
*Use this to get a link to the receipt hosted by the merchant.*

### 3. `vipps_order_details.py` (Receipt Data)
Demonstrates how to fetch the full structured receipt data using the **Order Management API**:
1.  Uses an Order ID.
2.  Returns the `orderLines` and `bottomLine` (items, tax, total).
*Use this to "grab" the actual content of the receipt if it was stored in Vipps.*

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
    python3 vipps_login.py
    # Follow prompts

    python3 vipps_payment_receipt.py
    # Enter a Payment Reference

    python3 vipps_order_details.py
    # Enter an Order ID
    ```

## Prerequisites

*   Python 3
*   `requests` library (`pip install requests`)
