from fastapi import FastAPI, UploadFile, File
import json
import os
import shutil
from typing import List
from pydantic import BaseModel

DIRECTORY = os.getcwd()
DATA_FILE = "students.json"

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

def read_student_data():
    try:
        with open(DATA_FILE, encoding="utf8") as f:
            return json.load(f)
    except Exception as ex:
        print(ex)
        return []

@app.get("/students")
def get_all_students():
    return read_student_data()
 
@app.get("/students/{id}")
def get_student_by_id(id: int):
    students = read_student_data()
    for student in students:
        if student["id"] == id:
            print(f"Found student id={id}")
            return student
    return {}

@app.get("/students/search")
def search_students(name):
    return {"query_by": name, data: []}

class Student(BaseModel):
    id: int
    name: str
    gpa: float


@app.post("/students")
def insert_new_student(model: Student):
    students = read_student_data()
    for student in students:
        if student["id"] == model.id:
            print(f"Student id={id} existed")
            return {
                "success": False,
                "message": f"Student id={id} existed"
            }
    students.append(
        {
            "id": model.id,
            "name": model.name,
            "gpa": model.gpa
        }
    )
    with open(DATA_FILE, "w", encoding="utf8") as f:
        json.dump(students, f)
    return {"success": True, "data": model}


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


@ app.post("/images/multiple", tags=["UPLOAD"])
def upload_multiple_file(images: List[UploadFile] = File(...)):
    try:
        uploaded_files = []
        for image in images:
            uploaded_files.append(image.filename)
            file_save = os.path.join(DIRECTORY, "data", image.filename)
            with open(file_save, "wb") as tmp:
                shutil.copyfileobj(image.file, tmp)

        return {"files": uploaded_files}
    except Exception as e:
        print(e)
        return {"success": False}