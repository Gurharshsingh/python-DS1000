"""
=============================================================
 🖱️ Interactive PC File Picker & Uploader (No HTML)
=============================================================
This script opens the standard Windows File Explorer dialog 
on your PC so you can select real files and upload them to FastAPI!

How to run:
>>> python select_and_upload.py
=============================================================
"""

import tkinter as tk
from tkinter import filedialog
import requests

def choose_and_upload():
    # 1. Hide the root Tk window
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    print("📂 Opening Windows File Explorer on your screen...")
    
    # 2. Open native Windows file selector dialog (Multiple file selection)
    selected_paths = filedialog.askopenfilenames(
        title="Select files from your PC to upload to FastAPI",
        filetypes=[("All Files", "*.*")]
    )

    if not selected_paths:
        print("❌ No files selected. Cancelled.")
        return

    print(f"\n✅ You selected {len(selected_paths)} file(s):")
    for path in selected_paths:
        print(f"  - {path}")

    # 3. Prepare the multipart payload
    files_payload = []
    file_handles = []
    
    for path in selected_paths:
        f = open(path, "rb")
        file_handles.append(f)
        files_payload.append(("files", (path.split("/")[-1].split("\\")[-1], f)))

    url = "http://127.0.0.1:8000/upload/multiple"

    # 4. Send to FastAPI
    print("\n🚀 Uploading to FastAPI...")
    try:
        response = requests.post(url, files=files_payload)
    except requests.exceptions.ConnectionError:
        # Fallback to port 8005 if running on port 8005
        url = "http://127.0.0.1:8005/upload/multiple"
        response = requests.post(url, files=files_payload)

    # 5. Clean up file handles
    for f in file_handles:
        f.close()

    # 6. Display server response
    print("\n🎉 Server Response (HTTP", response.status_code, "):")
    print(response.json())


if __name__ == "__main__":
    choose_and_upload()
