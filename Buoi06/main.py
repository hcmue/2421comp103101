from fastapi import FastAPI, UploadFile, File, Depends, Query, HTTPException
import os
import shutil
from typing import List
from fastapi.responses import HTMLResponse, FileResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated

app = FastAPI()
DIRECTORY = os.getcwd()

# PyMySQL
engine = create_engine("mysql+pymysql://root:@localhost/2421comp103101")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str
    role: int = Field(default=None)
    is_active: bool | None = Field(default=True)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/users/", tags=["user"])
def create_user(model: User, session: SessionDep) -> User:
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


@app.get("/users/", tags=["user"])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    users = session.exec(
        select(User).offset(offset).limit(limit)
    ).all()
    return users

@app.get("/users/{user_id}", tags=["user"])
def read_user(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )
    return user

@app.delete("/users/{user_id}", tags=["user"])
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )
    try:
        session.delete(user)
        session.commit()
        return {"success": True}
    except Exception as ex:
        print(ex)
        return {"success": False}


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
