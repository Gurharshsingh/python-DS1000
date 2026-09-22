from fastapi import APIRouter,HTTPException,status,UploadFile,Form,File
from typing import List


router=APIRouter(prefix="/file",tags=["File Uploads"])

@router.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    content=await file.read()
    file_path=f"uploads/{file.filename}"
    with open(file_path,"wb") as f:
        f.write(content)
    return {"message":"File uploaded successfully","Size of the content":len(content),}

@router.get("/readcontent")
def read_content(filename: str):
    try:
        with open(f"uploads/{filename}", "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File content could not be decoded as UTF-8 text. It might be a binary or non-UTF-8 file."
        )

# multiple files upload 

@router.post("/multiple-files")
async def upload_multiple_files(files:List[UploadFile]=File(...)):
    for file in files:
        content=await file.read()
        file_path=f"uploads/{file.filename}"
        with open(file_path,"wb") as f:
            f.write(content)
    return {"message":"Files uploaded successfully"}


# Form data 

@router.post("/student-data")
async def student(
    name:str=Form(...),
    age:int=Form(...),
    course:str=Form(...),
    file:UploadFile=File(),
):
    if file.content_type not in ["application/pdf","application/docx"]:
        raise HTTPException(status_code=400,detail="Invalid file type")
    else:

        content =await file.read()

        file_path=f"uploads/{file.filename}"

    
        return {"message":"File uploaded successfully","Size of the content":len(content),}


