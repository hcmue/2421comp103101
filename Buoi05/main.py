from typing import Union
from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

DATA_FILE = "students.json"
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

from pydantic import BaseModel
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
    students.append({"id": model.id, "name": model.name, "gpa": model.gpa})
    with open(DATA_FILE, "w", encoding="utf8") as f:
        json.dump(students, f)
    return {"success": True, "data": model}