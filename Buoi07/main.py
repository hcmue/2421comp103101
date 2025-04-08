from fastapi import FastAPI, UploadFile, File, Depends, Query, HTTPException, status
import os
import shutil
from typing import List
from fastapi.responses import HTMLResponse, FileResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, ValidationError
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class Customer(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

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
    model.password = get_password_hash(model.password)
    print('Sau mã hóa', model)
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


def authenticate_user(session: SessionDep, username: str, password: str):
    users = session.exec(select(User)).all() # optimize
    # Check username
    user = None
    for u in users:
        if u.username == username:
            user = u
            break
    print('Authen found user: ', user)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> Token:
    user = authenticate_user(
        session, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")