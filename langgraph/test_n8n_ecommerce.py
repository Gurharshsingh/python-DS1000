"""
E-Commerce Webhook Tester for n8n Example 1
===========================================
Usage:
  python test_n8n_ecommerce.py clean   -> Sends low-risk order (routes to Approved 200)
  python test_n8n_ecommerce.py fraud   -> Sends high-risk order (routes to Flagged 403)
"""

import sys
import json
import requests

WEBHOOK_URL = "http://localhost:5678/webhook-test/order-checkout"

# Scenario A: Clean, low-risk order (Matching countries, standard amount)
clean_order = {
    "customer_name": "Michael Scott",
    "customer_email": "m.scott@dundermifflin.com",
    "amount": 450.00,
    "billing_country": "US",
    "shipping_country": "US",
    "item": "Ergonomic Office Chair"
}

# Scenario B: High-risk order (Mismatched countries and high amount >= $3000)
fraud_order = {
    "customer_name": "Unknown Buyer",
    "customer_email": "temp99281@protonmail.com",
    "amount": 4200.00,
    "billing_country": "RU",
    "shipping_country": "US",
    "item": "5x MacBook Pro M3 Max"
}

def send_order(mode: str, url: str):
    payload = fraud_order if mode.lower() == "fraud" else clean_order

    print("==========================================")
    print(f">> Sending [{mode.upper()}] Order to n8n Webhook")
    print(f"Target URL: {url}")
    print("Order Payload:")
    print(json.dumps(payload, indent=2))
    print("==========================================\n")

    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )

        print(f"HTTP Status Code: {response.status_code}")
        print("\nResponse from n8n Workflow:")
        try:
            print(json.dumps(response.json(), indent=2))
        except Exception:
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("❌ Connection Failed:")
        print("Could not reach n8n at:", url)
        print("\nQuick Troubleshooting:")
        print("1. Is n8n running on http://localhost:5678?")
        print("2. In n8n, did you click 'Listen for test event' on the 'Order Webhook' node?")
        print("3. Is the webhook path set to 'order-checkout'?")

if __name__ == "__main__":
    test_mode = sys.argv[1] if len(sys.argv) > 1 else "clean"
    target_url = sys.argv[2] if len(sys.argv) > 2 else WEBHOOK_URL
    send_order(test_mode, target_url)
