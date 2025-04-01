from fastapi import FastAPI, UploadFile, File
import os
import shutil
from typing import List
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()
DIRECTORY = os.getcwd()

@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = f"./data/{file_name}"
    if os.path.isfile(file_path):
        print(f"Downloading file: {file_path}")
        return FileResponse(
            path=file_path,
            filename=file_name,
            headers={
                "Content-Disposition": f"attachment; filename={file_name}"
            }
        )
    else:
        return {"error": "File not found"}
    
@app.get("/response/html", response_class=HTMLResponse)
def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/images", tags=["UPLOAD"])
def upload_single_file(image: UploadFile = File(...)):
    try:
        file_save = os.path.join(DIRECTORY, "data", image.filename)
        with open(file_save, "wb") as tmp:
            shutil.copyfileobj(image.file, tmp)
        return {"filename": image.filename}
    except Exception as e:
        print(e)
        return {"success": False}
    

@app.post("/images/multiple", tags=["UPLOAD"])
def upload_single_file(images: List[UploadFile] = File(...)):
    try:
        result = []
        for image in images:            
            file_save = os.path.join(DIRECTORY, "data", image.filename)
            with open(file_save, "wb") as tmp:
                shutil.copyfileobj(image.file, tmp)
                result.append(image.filename)
        return {"success": True, "data": result}
    except Exception as e:
        print(e)
        return {"success": False}
