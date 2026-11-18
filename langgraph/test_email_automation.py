"""
Week 22: AI Document Processing & Email Automation Tester
=========================================================
This script simulates sending an incoming customer email with an attached 
disputed invoice document to your n8n workflow.

Usage:
  python test_email_automation.py [WEBHOOK_URL]
"""

import sys
import json
import requests

DEFAULT_URL = "http://localhost:5678/webhook-test/incoming-email"

payload = {
    "sender_name": "Sarah Connor",
    "sender_email": "sarah.connor@cyberdyne.org",
    "email_subject": "Disputed Charge on Invoice #INV-2026-881",
    "email_body": "Hello Support Team,\n\nPlease see the attached invoice statement. We noticed a $650 unscheduled maintenance surcharge that violates Section 4.2 of our SLA. Please review and credit this amount.\n\nRegards,\nSarah Connor",
    "document_filename": "sample_invoice.txt",
    "document_content": (
        "INVOICE #INV-2026-881\n"
        "Customer: Cyberdyne Defense Systems\n"
        "1. Dedicated Enterprise Cloud Cluster - $2,500.00\n"
        "2. Dedicated Support & SLA Monitoring - $800.00\n"
        "3. Emergency Unscheduled Maintenance Surcharge - $650.00 (Disputed)\n"
        "Subtotal: $3,950.00\n"
        "Total Due: $4,345.00"
    )
}

def send_test_email(url: str):
    print("==========================================")
    print(">> Sending Incoming Customer Email & Document to n8n")
    print(f"Target URL: {url}")
    print(f"Sender: {payload['sender_name']} <{payload['sender_email']}>")
    print(f"Subject: {payload['email_subject']}")
    print("==========================================\n")

    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=25
        )
        print(f"HTTP Status: {response.status_code}")
        print("\nResponse from n8n Workflow:")
        try:
            print(json.dumps(response.json(), indent=2))
        except Exception:
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to n8n at:", url)
        print("Tip: If running in manual test mode in n8n, make sure your Webhook node is listening!")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    send_test_email(target)
