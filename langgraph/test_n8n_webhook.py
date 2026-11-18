"""
Week 21: n8n Fundamentals - Webhook & HTTP Tester
==================================================
This script sends a mock POST request to test your n8n Webhook node.

Instructions for students:
1. Open n8n (http://localhost:5678 or your cloud n8n URL).
2. Open the workflow with the 'Webhook' node.
3. Click "Listen for test event" (Test URL mode) OR toggle workflow to Active (Production URL mode).
4. Run this script: python test_n8n_webhook.py
"""

import sys
import json
import requests

# Default n8n test webhook URL on local instance
# If testing in n8n editor, use 'webhook-test'
# If testing active production workflow, use 'webhook'
WEBHOOK_URL = "http://localhost:5678/webhook-test/lead-intake"

# Sample payload demonstrating user input to be processed by n8n
sample_payload = {
    "name": "Sarah Connor",
    "email": "sarah.connor@sky-resistance.org",
    "budget": 7500,
    "company": "Cyberdyne Systems",
    "notes": "Looking for automated multi-agent workflow integration."
}

def send_test_webhook(url: str, data: dict):
    print("==========================================")
    print(">> Sending Test Request to n8n Webhook")
    print(f"Target URL: {url}")
    print("Payload:")
    print(json.dumps(data, indent=2))
    print("==========================================\n")

    try:
        response = requests.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        print(f"Status Code: {response.status_code}")
        print("\nResponse from n8n:")
        try:
            print(json.dumps(response.json(), indent=2))
        except Exception:
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error:")
        print("Could not reach n8n at:", url)
        print("\nChecklist:")
        print("1. Is n8n running? (Check terminal or http://localhost:5678)")
        print("2. Did you click 'Listen for test event' in your n8n Webhook node?")
        print("3. Does the webhook path in n8n match '/lead-intake'?")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else WEBHOOK_URL
    send_test_webhook(target, sample_payload)
