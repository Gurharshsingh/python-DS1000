"""
=============================================================
 FastAPI Tutorial - Chapter 5: File Uploads & Handling
=============================================================
 TOPICS COVERED:
   1. Difference between `bytes = File()` and `UploadFile`
   2. Single file upload & inspecting metadata
   3. Saving uploaded files to disk
   4. Multiple file uploads (`list[UploadFile]`)
   5. Uploading files with Form fields (Form + File)
   6. File validation (extension & size)
   7. In-memory file processing (CSV, JSON)
   8. Serving and downloading files (`FileResponse`)
   9. Deleting uploaded files

 PREREQUISITE:
   pip install python-multipart

 HOW TO RUN:
   uvicorn 05_file_uploads:app --reload --port 8005

 THEN VISIT:
   http://127.0.0.1:8005/docs -> Test uploads interactively!
=============================================================
"""

import shutil
import csv
import io
import json
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse

app = FastAPI(
    title="FastAPI File Uploads",
    description="Simple guide for uploading, saving, and handling files in FastAPI."
)

# Folder to store uploaded files
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================
# 1. Single File Uploads (bytes vs UploadFile)
# ==============================================================

@app.post("/upload/bytes", summary="1. Upload as raw bytes (Small files)")
def upload_bytes(file: bytes = File(...)):
    """Reads the entire file directly into memory as raw bytes."""
    return {
        "upload_type": "bytes",
        "file_size_bytes": len(file)
    }


@app.post("/upload/file", summary="2. Upload using UploadFile (Recommended)")
def upload_file(file: UploadFile = File(...)):
    """UploadFile handles files efficiently and gives access to metadata."""
    contents = file.file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents)
    }


# ==============================================================
# 2. Saving Files to Disk
# ==============================================================

@app.post("/upload/save", summary="3. Save uploaded file to disk")
def save_file(file: UploadFile = File(...)):
    """Saves the uploaded file to the 'uploaded_files' directory."""
    destination_path = UPLOAD_DIR / file.filename

    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File saved successfully",
        "filename": file.filename,
        "saved_path": str(destination_path)
    }


# ==============================================================
# 3. Multiple File Uploads
# ==============================================================

@app.post("/upload/multiple", summary="4. Upload multiple files at once")
def upload_multiple(files: list[UploadFile] = File(...)):
    """Accepts multiple files in a single request."""
    uploaded_files = []

    for file in files:
        contents = file.file.read()
        uploaded_files.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents)
        })

    return {
        "total_files": len(files),
        "files": uploaded_files
    }


# ==============================================================
# 4. Form Data + File Upload
# ==============================================================

@app.post("/upload/profile-with-avatar", summary="5. Upload file with form fields")
def upload_profile(
    username: str = Form(...),
    email: str = Form(...),
    bio: str = Form("No bio provided"),
    avatar: UploadFile = File(...)
):
    """Combines form text fields with a file upload."""
    avatar_path = UPLOAD_DIR / avatar.filename
    with open(avatar_path, "wb") as buffer:
        shutil.copyfileobj(avatar.file, buffer)

    return {
        "message": "Profile created successfully",
        "username": username,
        "email": email,
        "bio": bio,
        "avatar_filename": avatar.filename
    }


# ==============================================================
# 5. File Validation (Extension & Size)
# ==============================================================

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf", ".txt", ".csv", ".json", ".xlsx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@app.post("/upload/validated-image", summary="6. Validate file extension and size")
def validate_file(file: UploadFile = File(...)):
    """Checks extension and size before accepting the file."""
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file extension: {file_ext}")

    contents = file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large! Max allowed size is 5MB.")

    return {
        "message": "Validation passed",
        "filename": file.filename,
        "size_bytes": len(contents)
    }


# ==============================================================
# 6. In-Memory Processing (CSV & JSON)
# ==============================================================

@app.post("/upload/process-csv", summary="7. Read and parse CSV in memory")
def process_csv(file: UploadFile = File(...)):
    """Parses a CSV file directly in memory without saving to disk."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv file")

    text_data = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(text_data))
    rows = list(reader)

    return {
        "filename": file.filename,
        "total_rows": len(rows),
        "headers": reader.fieldnames,
        "rows": rows
    }


@app.post("/upload/process-json", summary="8. Read and parse JSON in memory")
def process_json(file: UploadFile = File(...)):
    """Parses a JSON file directly in memory without saving to disk."""
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="File must be a .json file")

    try:
        data = json.loads(file.file.read().decode("utf-8"))
        return {
            "filename": file.filename,
            "data": data
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")


# ==============================================================
# 7. Serving, Viewing & Downloading Files
# ==============================================================

@app.get("/files", summary="9. List all saved files")
def list_files():
    """Lists all files stored in the upload directory."""
    files = [f.name for f in UPLOAD_DIR.iterdir() if f.is_file()]
    return {"total_files": len(files), "files": files}


@app.get("/files/{filename}", summary="10. View a file in browser")
def view_file(filename: str):
    """Returns the file to be viewed inline in the browser."""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


@app.get("/files/{filename}/download", summary="11. Force download a file")
def download_file(filename: str):
    """Forces the browser to download the file as an attachment."""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)


@app.delete("/files/{filename}", summary="12. Delete a saved file")
def delete_file(filename: str):
    """Deletes a file from the upload directory."""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    file_path.unlink()
    return {"message": f"'{filename}' deleted successfully"}


# ==============================================================
# 8. Entrypoint
# ==============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("05_file_uploads:app", host="127.0.0.1", port=8005, reload=True)
