"""
Quick script to test Section 3 (Multiple File Uploads)
Run this while uvicorn is running:
>>> python test_upload.py
"""
import requests
from pathlib import Path

# Create a couple of small sample files to test upload
Path("sample1.txt").write_text("Hello from file 1! 🎉", encoding="utf-8")
Path("sample2.txt").write_text("Hello from file 2! 🚀", encoding="utf-8")

url = "http://127.0.0.1:8000/upload/multiple"
# If running on port 8005: url = "http://127.0.0.1:8005/upload/multiple"

# Prepare files for multipart/form-data
files = [
    ("files", ("sample1.txt", open("sample1.txt", "rb"), "text/plain")),
    ("files", ("sample2.txt", open("sample2.txt", "rb"), "text/plain")),
]

print("Sending multiple files to Section 3 (/upload/multiple)...")
try:
    response = requests.post(url, files=files)
    print("\n✅ Server Response (Status Code:", response.status_code, "):")
    print(response.json())
except requests.exceptions.ConnectionError:
    # Try port 8005 if 8000 fails
    url = "http://127.0.0.1:8005/upload/multiple"
    response = requests.post(url, files=files)
    print("\n✅ Server Response (Status Code:", response.status_code, "):")
    print(response.json())
